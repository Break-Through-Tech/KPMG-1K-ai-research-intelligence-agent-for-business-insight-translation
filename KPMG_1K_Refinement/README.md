# KPMG-1K | Retrieval refinement

This extension builds on the Part 6 passage evaluation and the existing arXiv RAG pipeline. It adds evidence-aware ranking, source diversity and a revised prompt for business-facing research answers.

## Files

| File | Description |
|---|---|
| `Retrieval_Refinement.ipynb` | Offline ranking comparison and optional live experiments |
| `retrieval_refinement.py` | Ranking, filtering and prompt functions |
| `evaluation_prompts.csv` | Eight sample user prompts and one missing-evidence question |
| `preliminary_relevance_labels.csv` | AI-assisted relevance labels for the saved passages |
| `review_template.csv` | Template for independent review |
| `refinement_outputs/` | Saved offline results |
| `REFINEMENT_REPORT.md` | Method, results and limitations |

## Running the notebook

Use Python 3.11 with pandas and a Jupyter kernel. Keep the Python module beside the notebook. Obtain `questions.csv` and `retrieved_passages.csv` from the Part 6 evaluation directory (`data_processed/rag_final_evaluation/`); adjust `BASE` if needed. These input files are not included here.

Run the notebook with both live flags set to `False` to reproduce the offline comparison. Results are written to `refinement_outputs/`.

For live testing, initialise the existing Part 5 `fusion_retriever` in the same kernel and enable `RUN_LIVE_RETRIEVAL`. The cross-encoder requires the relevant LlamaIndex and sentence-transformers dependencies. The default loop uses the original questions; use `evaluation_prompts.csv` for the expanded test. Enable `RUN_LIVE_GENERATION` only after initialising `llm`; this may consume API quota.

## Results

Mean nDCG@5 increased from 0.669 to 0.907 on the fixed candidate sets using preliminary labels. Live retrieval and answer quality have not been validated. See the report for the per-question comparison.
