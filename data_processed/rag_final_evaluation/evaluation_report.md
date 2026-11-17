
# Part 6: RAG Evaluation Report

## 1. Overview

This evaluation examines the retrieval performance of the KPMG AI Research Intelligence Agent, developed as part of the Break Through Tech AI programme. The project aims to help users find relevant academic research and translate technical findings into business insights supported by research evidence.

The evaluation focuses on whether the retrieval system identifies passages that are relevant and useful for answering research questions. It also considers the limitations of the available evidence and how these affect the reliability of the results.

Six questions were used for testing. Five addressed topics related to retrieval-augmented generation (RAG), while the sixth tested a question for which the research corpus was not expected to contain supporting evidence.

The evaluation produced 30 retrieved passages, with five passages returned for each question.

## 2. Evaluation Methodology

The evaluation used the saved retrieval results in `retrieved_passages.csv`. Each passage was examined in relation to its corresponding question.

Passages were assessed using the following relevance scale:

| Score | Description |
|---|---|
| 0 | The passage is unrelated or does not provide useful evidence for answering the question. |
| 1 | The passage is partially relevant but does not sufficiently address the question. |
| 2 | The passage provides directly useful information for answering the question. |

The assessment considered whether the passage addressed the question, contained relevant supporting information and could reasonably contribute to a research-based answer.

Two measures were calculated:

- **Direct passage relevance:** The proportion of retrieved passages assigned a score of 2.
- **Graded relevance:** The total relevance points awarded divided by the maximum possible points.

The first five questions were included in these calculations. The sixth question was examined separately because it was designed to test the absence of supporting evidence.

These scores are based on an initial AI-assisted review of the saved passages. They are descriptive findings rather than independently verified benchmark results.

## 3. Evaluation Results

### 3.1 Retrieval Relevance

The evaluation identified 8 directly useful passages among the 25 passages retrieved for the five answerable questions.

| Metric | Result |
|---|---|
| Evaluation questions | 6 |
| Answerable questions | 5 |
| Missing-evidence questions | 1 |
| Retrieved passages | 30 |
| Passages assessed for answerable questions | 25 |
| Directly useful passages | 8 |
| Direct passage relevance | 32% |
| Total graded relevance score | 23/50 |
| Normalised graded relevance | 46% |

The results suggest that the retrieval system identifies some useful research evidence, although relevance varies considerably across questions.

### 3.2 Question-Level Results

| Question | Topic | Directly useful passages | Assessment |
|---|---|---|---|
| Q1 | Reducing hallucinations in RAG | 0/5 | Weak |
| Q2 | Dense and sparse retrieval | 1/5 | Limited |
| Q3 | Evaluating factual support | 2/5 | Moderate |
| Q4 | Business risks of RAG deployment | 3/5 | Relatively strong |
| Q5 | Common RAG failure modes | 2/5 | Moderate |
| Q6 | Financial savings from the KPMG prototype | 0/5 | No supporting evidence found |

The results show that the system performs better on some topics than others. Questions concerning business risks and factual evaluation returned more useful material than questions concerning hallucination mitigation and retrieval methods.

## 4. Discussion of Findings

### Q1: Reducing Hallucinations in RAG

The retrieved passages were generally related to hallucinations in language models, but they did not directly explain methods for reducing hallucinations in RAG systems.

For example, the results included research on hallucinations in multimodal models, knowledge graph reasoning and robotic systems. Although these topics share some terminology with the question, they do not provide sufficient evidence for discussing specific RAG mitigation techniques.

This suggests that matching related terminology does not necessarily produce passages that address the intended research question.

### Q2: Dense and Sparse Retrieval

One retrieved passage provided a useful distinction between sparse lexical retrieval and embedding-based retrieval.

The passage discussed methods such as BM25 and SPLADE, explaining their suitability for keyword matching compared with approaches based on semantic representations.

However, most of the remaining passages focused on retrieval efficiency, hashing methods or unrelated aspects of AI research. As a result, the retrieved evidence did not provide a comprehensive comparison of the strengths and limitations of dense and sparse retrieval.

### Q3: Evaluating Factual Support

This question produced more useful results.

One passage described an evaluation framework for grounded generation, including answer correctness, faithfulness, citation quality and refusal behaviour when evidence is unavailable.

Another discussed the difficulty of distinguishing answers grounded in supplied evidence from answers based on a model's existing knowledge.

These findings are relevant to evaluating whether RAG-generated answers are supported by retrieved documents. However, several other passages concerned broader language-model evaluation rather than RAG-specific factual support.

### Q4: Business Risks of RAG Deployment

This question produced the highest number of directly useful passages.

The retrieved material covered regulatory compliance, incorrect AI-generated responses, tool permissions and operational risks associated with language-model services.

These topics are relevant to organisations considering the deployment of AI research assistants.

Nevertheless, much of the evidence concerned AI assistants more broadly rather than RAG systems specifically. The results therefore provide useful business context but do not fully address risks such as unsupported citations, outdated research evidence and retrieval failures.

### Q5: Common RAG Failure Modes

The results included research discussing retrieval limitations, particularly when questions require information from multiple passages.

One passage explained why similarity-based retrieval may be insufficient for questions involving several connected pieces of evidence. Another discussed the effects of retrieval-system failures on recall.

These findings are useful for understanding certain RAG failure modes.

However, the retrieved passages did not cover the full range of potential problems, including irrelevant context, incomplete retrieval, unsupported generation and incorrect source attribution.

### Q6: Missing-Evidence Question

The final question asked for the exact financial savings achieved by KPMG through the student prototype.

None of the five retrieved passages provided evidence supporting such a figure. The results instead concerned unrelated financial research, language-model costs and other technical topics.

This finding indicates that the retrieved evidence is insufficient to answer the question.

A reliable research assistant should acknowledge that the requested information is unavailable rather than provide an unsupported numerical estimate.

The saved evaluation results do not contain a generated answer for this question. Therefore, the system's actual ability to abstain cannot be determined from this evaluation.

## 5. Limitations

Several limitations should be considered when interpreting these findings.

First, the evaluation uses a small set of six questions. While these questions cover different aspects of RAG, they are not sufficient to establish performance across a wider range of research topics.

Second, the relevance scores are based on an initial assessment of the retrieved passages rather than an independently verified reference dataset. The reported percentages should therefore be interpreted as preliminary indicators of retrieval quality.

Third, the saved passages represent the retrieval output examined in this evaluation. The results do not establish the performance of the complete answer-generation pipeline.

Finally, the available files do not contain generated answers or completed human-review scores. Consequently, answer correctness, completeness, citation support and business usefulness cannot be measured from these outputs.

These limitations are important because relevant retrieval is only one component of a reliable RAG system.

## 6. Conclusion

The evaluation shows that the KPMG AI Research Intelligence Agent can retrieve useful research evidence, but the relevance of the retrieved passages is inconsistent across questions.

Of the 25 passages assessed for the five answerable questions, eight were judged directly useful. The system performed relatively well when retrieving information about business risks and factual evaluation, while questions involving hallucination mitigation and retrieval comparisons returned less directly relevant material.

A recurring issue was the retrieval of passages that shared terminology with the question without adequately addressing it. Some results also contained references or background material rather than substantive evidence.

Overall, the findings highlight the importance of evaluating retrieved evidence at the passage level rather than relying on topical similarity alone.


## 7. Evaluation Files

The results discussed in this report are available in the following files:

- [`questions.csv`](questions.csv) — Evaluation questions and question types.
- [`retrieved_passages.csv`](retrieved_passages.csv) — Retrieved passages and associated metadata.
- [`reference_review.csv`](reference_review.csv) — Reference verification template.
- [`human_review.csv`](human_review.csv) — Human evaluation template.
- [`summary.csv`](summary.csv) — Saved evaluation summary.
- [`known_paper_hits.csv`](known_paper_hits.csv) — Known-paper retrieval assessment output.

The evaluation findings reported here are based on the retrieved passages.
