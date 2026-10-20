# AI Studio Challenge Project Title

> 💡 **Note for the team:** This is just a template. Update the above title with your AI Studio Challenge Project name. Remove all guidance notes and example text in this template and populate this README with your own content. You can work on this README throughout AI Studio, and get feedback from your AI Studio Coach and Challenge Advisor before finalizing it.  

---

### 👥 **Team Members**

**Example:**

| Name             | GitHub Handle | Contribution                                                             |
|------------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Anya Vasetskaya  | @AnyaVasetskaya | Retrieval-Augmented Generation (RAG) architecture, baseline prototyping, research retrieval and summarisation integration                   |
| Eiman Sherzada   | @chimaevv       | Research data assessment and preparation; end-to-end retrieval and summarisation workflow development and testing                           |
| Fidel Torres     | @Ochoa667       | Research text extraction and preprocessing; prompt engineering for accessible, business-oriented insights                                   |
| Janhavi Beley    | @JanhaviBeley   | Retrieval evaluation, benchmark design, assessment of relevance, accuracy and completeness, and documentation of improvement opportunities. |

---

## 🎯 **Project Highlights**

**Example:**

- Developed a machine learning model using `[model type/technique]` to address `[challenge project task]`.
- Achieved `[key metric or result]`, demonstrating `[value or impact]` for `[host company]`.
- Generated actionable insights to inform business decisions at `[host company or stakeholders]`.
- Implemented `[specific methodology]` to address industry constraints or expectations.
- 
- Developed a RAG-based workflow to retrieve relevant AI research from arXiv in response to natural-language questions.
- Used a large language model to turn complex academic findings into concise, business-relevant explanations.
- Preserve paper metadata and provide citations so users can verify claims against original sources.
- Assess retrieval relevance, citation correctness, summary fidelity and stakeholder usefulness.
- Treat generated insights as a research support rather than a replacement for professional judgement.

**Project is being developed** 
**Estimated Date: November end**

---

## 👩🏽‍💻 **Setup and Installation**

**Provide step-by-step instructions so someone else can run your code and reproduce your results. Depending on your setup, include:**

* How to clone the repository
* How to install dependencies
* How to set up the environment
* How to access the dataset(s)
* How to run the notebook or scripts


### 1. Clone the repository

```bash
git clone https://github.com/Break-Through-Tech/KPMG-1K-ai-research-intelligence-agent-for-business-insight-translation.git
cd KPMG-1K-ai-research-intelligence-agent-for-business-insight-translation
```

### 2. Create and activate a virtual environment

```bash
python3 -m vent .venv
source .venv/bin/activate  #macOS/Linux
#Windows (PowerShell): .venv\Scripts\Activate.psl
```

### 3. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Explore the project
```bash
- `data/` - project research data and related resources.
- `notebooks/` - exploratory work and prototype notebook.
- Challenge-project-Overview.md - challenge background and objectives.
- Challenge-Project-Setup.md and `Getting-Started-for-Fellows.md` - programme setup guidance
```


---

## 🏗️ **Project Overview**

**Describe:**

This project is being developed through the **Break Through Tech AI Studio**, in collaboration with **KPMG**, a global professional services organisation. It addresses the challenge of keeping pace with a growing volume of AI research and understanding its relevance to real-world business decisions.

Academic papers often contain valuable advances, but translating technical methods, results and limitations into accessible business implications require substantial time and domain expertise. The proposed agent aims to shorten that process without losing the link to the original evidence.

(Pointers that were originally present in the section to help us write this bit)
- How this project is connected to the Break Through Tech AI Program
- Your AI Studio host company and the project objective and scope
- The real-world significance of the problem and the potential impact of your work

### Proposed workflow

flowchart TD
    A[AI research papers and metadata from arXiv] --> B[Text extraction and preprocessing]
    B --> C[Chunking and metadata preservation]
    C --> D[Embedding and retrieval index]
    Q[Business question] --> E[Relevant research retrieval]
    D --> E
    E --> F[LLM-based summarisation and insight translation]
    F --> G[Business-oriented response with citations]
    G --> H[Evaluation and human review]

### Project milestones

| Phase | Target | Focus |
| --- | --- | --- |
| Foundation and baseline RAG | 30 September 2026 | Research exploration, preprocessing, benchmark queries and baseline retrieval. |
| Pipeline development and evaluation | 31 October 2026 | Retrieval and summarisation integration, business-focused prompting and initial quality assessment. |
| Refinement and final delivery | 30 November 2026 | Improve relevance and outputs, develop a lightweight interaction layer, document findings and prepare final presentation. |



---

## 📊 **Data Exploration**

**You might consider describing the following (as applicable):**

* The dataset(s) used: origin, format, size, type of data
* Data exploration and preprocessing approaches
* Insights from your Exploratory Data Analysis (EDA)
* Challenges and assumptions when working with the dataset(s)

**Potential visualizations to include:**

* Plots, charts, heatmaps, feature visualizations, sample dataset images


**Primary source:** [arXiv](https://arxiv.org/), particularly its artificial intelligence research collection.

The project works with research-paper text and associated metadata. Potential metadata fields include titles, authors, publication information and source identifiers. The arXiv API can provide Atom/XML metadata, while paper content requires appropriate retrieval and text extraction.

The team's data exploration and preparation plan includes:

- Inspecting paper formats, available fields, missing metadata and data quality.
- Identifying duplicate papers and different versions of the same work.
- Cleaning extracted text, including artefacts from academic formatting and mathematical notation.
- Analysing paper length, structure, topic coverage and publication patterns to guide chunking.
- Splitting documents into retrievable passages while retaining source metadata for citation generation.

---

## 🧠 **Model Development**

**You might consider describing the following (as applicable):**

* Model(s) used (e.g., CNN with transfer learning, regression models)
* Feature selection and Hyperparameter tuning strategies
* Training setup (e.g., % of data for training/validation, evaluation metric, baseline performance)

The proposed approach combines **Retrieval-Augmented Generation (RAG)** with **large language model summarisation**. Rather than asking an LLM to answer solely from its internal knowledge, the system is intended to retrieve relevant source material and use that evidence to construct its response.

### Core components

1. **Ingestion and preprocessing:** Acquire research content, clean extracted text and retain paper metadata.
2. **Document representation:** Divide papers into meaningful chunks and generate embeddings for semantic retrieval.
3. **Research retrieval:** Match natural-language questions to relevant passages and source documents.
4. **Insight generation:** Summarise findings and explain their possible business significance using evidence-grounded prompts.
5. **Citation handling:** Connect claims to identifiable papers or passages.
6. **Evaluation:** Compare outputs with benchmark questions and original research to identify errors, omissions and improvement opportunities.


---

## 📈 **Results & Key Findings**

**You might consider describing the following (as applicable):**

* Performance metrics (e.g., Accuracy, F1 score, RMSE)
* How your model performed
* Insights from evaluating model fairness

**Potential visualizations to include:**

* Confusion matrix, precision-recall curve, feature importance plot, prediction distribution, outputs from fairness or explainability tools




---

## 🚀 **Next Steps**

**You might consider addressing the following (as applicable):**

* What are some of the limitations of your model?
* What would you do differently with more time/resources?
* What additional datasets or techniques would you explore?

---

## 📝 **License**

Specify how your project can be used by others. Choose an appropriate license and link it here (e.g., MIT, Apache 2.0). Make sure your Challenge Advisor approves of the selected license type. 

**Example:**
This project is licensed under the MIT License.

---

## 📄 **References** (Optional but encouraged)

Cite relevant papers, articles, or resources that supported your project.


- [Break Through Tech](https://www.breakthroughtech.org/) — AI Studio programme.
- [KPMG](https://kpmg.com/) — industry challenge host.
- [arXiv](https://arxiv.org/) — research-paper repository.
- [arXiv API documentation](https://info.arxiv.org/help/api/index.html) — programme interface for research metadata and discovery.
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — foundational RAG research.
- [Project challenge overview](Challenge-Project-Overview.md) — repository-specific challenge context.

---

## 🙏 **Acknowledgements** (Optional but encouraged)

Thank your Challenge Advisor, host company representatives, TA, and others who supported your project.

We thank **KPMG** and **Break Through Tech AI Studio** for the opportunity to work on an applied AI research challenge. We are grateful to **Lauren Fang**, our KPMG Challenge Advisor, and **Deanna DiMonte**, our AI Studio Coach, for their guidance and support throughout the project.

*Developed as part of Break Through Tech AI Studio, Fall 2026.*
