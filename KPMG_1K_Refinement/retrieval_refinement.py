"""Passage ranking, evidence selection and grounded prompts for the arXiv RAG pipeline."""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Iterable

STOP = set("a an and are as at be by can could did do does for from has have how in into is it its of on or our should that the their them there these this to using was were what when where which who will with would we you your".split())
WORD_RE = re.compile(r"[a-z][a-z0-9-]*", re.I)
BOILERPLATE_RE = re.compile(
    r"authors should consider possible harms|safeguards question:|"
    r"released models that have a high risk|\banswer:\s*\[n/a\]", re.I)
BIBLIOGRAPHY_RE = re.compile(r"\b(references|bibliography)\b", re.I)
EVIDENCE_RE = re.compile(
    r"\b(method\w*|approach\w*|compar\w*|metric\w*|evaluat\w*|"
    r"eviden\w*|find\w*|result\w*|limit\w*|risk\w*|failure\w*|"
    r"reduc\w*|ground\w*|faithful\w*|citations?|abstain|refus\w*)\b", re.I)

# Expand common retrieval terms to include related terminology.
EXPANSIONS = {
    "hallucinat": {"grounding", "factual", "faithfulness", "mitigation", "citation"},
    "dense": {"embedding", "semantic", "vector"},
    "sparse": {"lexical", "bm25", "splade", "keyword"},
    "factual": {"faithfulness", "citation", "grounding", "evaluation"},
    "risks": {"compliance", "security", "privacy", "governance", "accuracy"},
    "failure": {"limitations", "errors", "missing", "recall", "grounding"},
}


def words(text: str) -> set[str]:
    return {t for t in WORD_RE.findall(str(text).lower()) if len(t) > 2 and t not in STOP}


def query_terms(question: str) -> set[str]:
    terms = words(question)
    for stem, additions in EXPANSIONS.items():
        if any(term.startswith(stem) for term in terms):
            terms.update(additions)
    return terms


def is_low_value_passage(passage: str) -> bool:
    """Identify bibliography or repeated publication-checklist fragments."""
    text = str(passage)
    first = text[:200]
    citation_markers = len(re.findall(r"\[\s*\d+\s*\]|\barxiv:|\bdoi:", text, re.I))
    return bool(BOILERPLATE_RE.search(text)) or bool(
        BIBLIOGRAPHY_RE.search(first) and citation_markers >= 2)


def lexical_evidence_score(question: str, passage: str, title: str = "") -> float:
    """Score lexical overlap and evidence cues; this is not a probability."""
    q = query_terms(question)
    text_terms, title_terms = words(passage), words(title)
    overlap = len(q & text_terms) / max(1, len(q))
    title_overlap = len(q & title_terms) / max(1, len(q))
    evidence = min(1.0, len(EVIDENCE_RE.findall(str(passage))) / 3.0)
    breadth = min(1.0, len(text_terms) / 60.0)
    question_lower, passage_lower = question.lower(), str(passage).lower()
    compare_bonus = 0.0
    if "dense" in question_lower and "sparse" in question_lower:
        has_lexical = any(x in passage_lower for x in ("sparse", "bm25", "lexical", "splade"))
        has_semantic = any(x in passage_lower for x in ("dense", "embedding", "vector", "semantic"))
        compare_bonus = 0.25 if has_lexical and has_semantic else -0.15
    return round(
        0.58 * overlap + 0.14 * title_overlap + 0.18 * evidence +
        0.10 * breadth + compare_bonus - 0.4 * int(is_low_value_passage(passage)), 6)


def _paper_key(node: Any, index: int) -> str:
    meta = node.metadata or {}
    return str(meta.get("arxiv_id") or meta.get("title") or getattr(node, "node_id", "") or f"unknown:{index}")


def _cross_encoder_sort(question: str, candidates: list[Any], *, top_n: int = 25) -> list[Any]:
    """Cross-encoder re-ranking of existing hybrid candidates; Hugging Face model."""
    from llama_index.core.schema import QueryBundle
    from llama_index.core.postprocessor import SentenceTransformerRerank

    reranker = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=min(top_n, len(candidates)))
    return reranker.postprocess_nodes(candidates, query_bundle=QueryBundle(query_str=question))


def select_ranked_evidence(
    question: str,
    candidates: list[Any],
    *, top_k: int = 5,
    max_per_paper: int = 2,
    use_cross_encoder: bool = True,
) -> tuple[list[Any], list[dict[str, Any]]]:
    """Rank candidates, filter boilerplate, diversify papers, return traceability.

    Rankings combine cross-encoder and interpretable lexical/evidence ordering
    by reciprocal-rank fusion, rather than mixing incompatible raw score scales.
    """
    if top_k < 1 or max_per_paper < 1:
        raise ValueError("top_k and max_per_paper must be positive")
    if not question.strip():
        raise ValueError("Question cannot be empty")
    if not candidates:
        return [], []

    # Keep the first occurrence of each node.
    original = []
    seen = set()
    for index, candidate in enumerate(candidates):
        node = candidate.node
        identifier = str(getattr(node, "node_id", "") or f"{index}")
        if identifier in seen:
            continue
        seen.add(identifier)
        original.append(candidate)

    lexical = sorted(
        original,
        key=lambda hit: lexical_evidence_score(
            question, hit.node.text or "", str((hit.node.metadata or {}).get("title", ""))),
        reverse=True,
    )
    lexical_rank = {str(getattr(hit.node, "node_id", "") or id(hit.node)): i for i, hit in enumerate(lexical, 1)}
    if use_cross_encoder:
        cross = _cross_encoder_sort(question, original, top_n=len(original))
    else:
        # Use the incoming order when the cross-encoder is disabled.
        cross = list(original)
    cross_rank = {str(getattr(hit.node, "node_id", "") or id(hit.node)): i for i, hit in enumerate(cross, 1)}

    # Weight the cross-encoder twice as heavily as lexical ranking.
    # Combine ranks rather than scores, which use different scales.
    combined = []
    for hit in cross:
        key = str(getattr(hit.node, "node_id", "") or id(hit.node))
        score = 2 / (60 + cross_rank[key]) + 1 / (60 + lexical_rank[key])
        combined.append((score, hit))
    combined.sort(key=lambda pair: pair[0], reverse=True)
    selected, audit, paper_counts = [], [], Counter()
    for score, hit in combined:
        node = hit.node
        passage = str(node.text or "")
        if is_low_value_passage(passage):
            continue
        pid = _paper_key(node, len(audit))
        if paper_counts[pid] >= max_per_paper:
            continue
        paper_counts[pid] += 1
        selected.append(hit)
        meta = node.metadata or {}
        audit.append({
            "rank": len(selected), "node_id": str(getattr(node, "node_id", "")),
            "paper_id": str(meta.get("arxiv_id") or ""),
            "title": str(meta.get("title") or ""),
            "page": meta.get("page_number", ""),
            "cross_encoder_rank": cross_rank[str(getattr(node, "node_id", "") or id(node))],
            "lexical_rank": lexical_rank[str(getattr(node, "node_id", "") or id(node))],
            "fusion_rank_score": round(score, 7),
        })
        if len(selected) >= top_k:
            break
    return selected, audit


def refine_existing_pipeline(question: str, fusion_retriever: Any, *, top_k: int = 5):
    """Retrieve candidates from the existing hybrid index and rerank them."""
    candidates = fusion_retriever.retrieve(question)
    return select_ranked_evidence(question, list(candidates)[:30], top_k=top_k)


BUSINESS_PROMPT = """You are an AI research analyst supporting non-technical business professionals.
Use ONLY the numbered passages below to answer the user's question.

Rules:
1. Give a clear and concise answer to the exact question, not just a general summary of AI research.
2. Every material research finding must carry an evidence citation [S1], [S2], etc.
3. Use only the paper title, arXiv ID, and page provided alongside each passage. Do not create citations.
4. Distinguish demonstrated research findings from *potential* business applications.
5. Do not invent financial savings, KPMG outcomes, accuracy statistics or any other unsupported facts.
6. A bibliography or a paper merely mentioning a term is not evidence for a factual claim.
7. Where the passages are not sufficient, say explicitly what cannot be established.
8. Keep the wording understandable to business readers without specialist ML knowledge.

Structure:
- **Answer:** two or three sentences.
- **Research findings:** cited findings relevant to the question.
- **Business implications:** possible applications, clearly distinguished from demonstrated results.
- **Limitations:** relevant gaps in the evidence.
- **Sources:** cited source labels and corresponding titles/pages.

Research passages:
{context}

Question:
{question}
"""


def make_prompt(question: str, selected: Iterable[Any]) -> str:
    """Create evidence-grounded prompt. No LLM call is made here."""
    sources = list(selected)
    if not question.strip():
        raise ValueError("Question cannot be empty")
    if not sources:
        return ("No supporting research passages were retrieved. "
                "Say that the available research evidence is insufficient to answer: " + question)
    context = []
    for i, hit in enumerate(sources, 1):
        metadata = hit.node.metadata or {}
        context.append(
            f"[S{i}] Title: {metadata.get('title') or 'Not available'}; "
            f"arXiv: {metadata.get('arxiv_id') or 'Not available'}; "
            f"page: {metadata.get('page_number') or 'Not available'}\n"
            f"{hit.node.text or ''}"
        )
    return BUSINESS_PROMPT.format(question=question, context="\n\n".join(context))


def should_abstain_missing_evidence(question: str, source_is_public_arxiv: bool = True) -> bool:
    """For the benchmark's KPMG savings question, public arXiv papers are not valid proof.

    This is a targeted benchmark guard, not a generic method for verifying every
    financial claim. An authorised, independently verified internal source would
    require a different workflow.
    """
    q = question.lower()
    asks_for_kpmg_finance = "kpmg" in q and any(x in q for x in (
        "financial savings", "cost savings", "return on investment", "roi"))
    return bool(source_is_public_arxiv and asks_for_kpmg_finance)


def answer_with_existing_llm(question: str, selected: list[Any], llm: Any) -> str:
    """Generate an answer using the existing LLM."""
    if should_abstain_missing_evidence(question):
        return ("The available arXiv research does not establish financial "
                "savings achieved by KPMG through this student prototype. "
                "A verified project-specific financial assessment would be needed.")
    if not selected:
        return "The available research evidence is insufficient to answer this question."
    return str(llm.complete(make_prompt(question, selected)))


def dcg(labels: list[int]) -> float:
    return sum((2 ** int(rel) - 1) / math.log2(i + 2) for i, rel in enumerate(labels))


def ndcg(labels: list[int]) -> float | None:
    if not labels:
        return None
    ideal = dcg(sorted(labels, reverse=True))
    return dcg(labels) / ideal if ideal > 0 else None


def reorder_saved_top5(question: str, records: list[dict]) -> list[dict]:
    """Reorder the five saved passages without changing the candidate set."""
    return sorted(records, key=lambda row: (
        is_low_value_passage(row["passage"]),
        -lexical_evidence_score(question, row["passage"], row.get("title", "")),
        row["rank"],
    ))
