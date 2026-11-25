# Prompt, Retrieval Ranking and Relevance Refinement

## Objective
The refinement addresses the main issue identified in the October evaluation: retrieved passages sometimes mention relevant terminology without providing evidence that directly answers the question. The changes focus on evidence selection and source-grounded responses using the existing arXiv corpus.

## Changes

### Prompt design
The revised prompt asks for a concise answer, relevant research findings, possible business implications, limitations and verifiable source references. It separates findings from interpretation and explicitly prevents unsupported claims about KPMG outcomes. Missing evidence must be acknowledged rather than filled with an estimate.

### Retrieval ranking
The ranking component uses the existing BM25/vector fusion retrieval as its candidate source. It can apply a Hugging Face cross-encoder to compare each candidate passage against the question and combine that ordering with a lightweight relevance score. It also limits repeated passages from one paper to improve source variety. These changes are intended to prioritise useful evidence; improvement is not assumed until independently tested.

### Relevance checks
The relevance mechanism penalises bibliography-like passages, checks whether a passage contains question-relevant evidence, and records paper metadata for review. It does not treat keyword overlap or model similarity as proof of factual accuracy.

## Evaluation design
Eight exact prompts were selected from Break Through Tech's sample prompt library to test hallucination mitigation, client risk, evaluation methods, retrieval architecture, reranking, groundedness, source scrutiny and traceability. The October missing-evidence question is retained as a separate abstention check. For business relevance, reviewers should consider whether the evidence helps an advisor prepare for a client discussion and verify the research claims.

Each prompt should be run against the original and refined retrieval approaches using the same arXiv index and top-five limit. Reviewers should assess retrieval relevance, business relevance and source support on a 0–2 scale and record the paper and page. Compare directly useful passages at five, ranking quality (such as nDCG@5) when graded labels are available, source variety and whether paraphrased prompts produce materially consistent results. Answer faithfulness and citation accuracy require actual generated answers and separate review.

## Offline evaluation results
The saved October results were reranked locally using the lightweight relevance mechanism. The same five candidate passages per question were retained; no new papers were retrieved. The diagnostic uses preliminary AI-assisted relevance labels (0–2), not independent ground truth.

| Question | Original nDCG@5 | Refined nDCG@5 | Directly useful candidates |
|---|---:|---:|---:|
| Q1 — Hallucinations | 0.431 | 1.000 | 0/5 |
| Q2 — Dense versus sparse retrieval | 0.659 | 0.945 | 1/5 |
| Q3 — Factual support | 0.803 | 0.958 | 2/5 |
| Q4 — Business risks | 0.906 | 0.994 | 3/5 |
| Q5 — Failure modes | 0.548 | 0.640 | 2/5 |
| Mean (Q1–Q5) | 0.669 | 0.907 | 8/25 total |

Mean nDCG@5 increased by 0.238 points (35.6% relative). All five questions improved on this diagnostic. Q1 nevertheless has no directly useful candidate: its perfect ranking score reflects ordering of weak evidence, not a correct answer. The number of directly useful candidates remains unchanged at eight of 25. Q6 is excluded from the ranking mean; abstention behaviour was not tested through generation.

The exported results are available in [offline_ranking_diagnostic.csv](refinement_outputs/offline_ranking_diagnostic.csv) and [offline_reranked_passages.csv](refinement_outputs/offline_reranked_passages.csv). The expanded prompt set is prepared but not evaluated live. Cross-encoder performance, new-document retrieval, answer faithfulness and citation accuracy remain unmeasured.

## Limitations and next steps
The offline comparison does not establish improved retrieval on the full index. Independent relevance judgements and a live comparison on unseen questions are needed before drawing that conclusion. The current labels are diagnostic rather than validated benchmark data.

Review generated claims and citations before using the results in client-facing work.
