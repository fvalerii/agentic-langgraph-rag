# 🕵️ Agentic Q&A System: LangGraph & Multi-Agent Orchestration
### *Autonomous RAG Ecosystem with Self-Correction & Reflection Loops*

![Multi-Agentic RAG](project-overview.jpg)
*Figure 1: High-fidelity multi-agent workflow featuring autonomous routing and verification loops.*

---

## 📋 Project Objective
This system represents a sophisticated evolution in document intelligence, moving beyond linear retrieval to an autonomous multi-agent framework. It automates the extraction of verified knowledge from complex documents by leveraging LangGraph for stateful orchestration and IBM Watsonx for high-reasoning synthesis.

- **Intelligent Orchestration:** Instead of a fixed pipeline, the system utilizes a Relevance Checker to classify query intent and route tasks dynamically.
- **Fact-Grounded Reflection:** Implements a Verification Agent that performs a secondary audit of all generated answers, identifying and correcting hallucinations or unsupported claims before delivery.

---

## 🏗️ System Architecture
The system follows a modular **Orchestrator-Worker** design pattern:

**🔄 The Multi-Agent Workflow**
1. **Document Ingestion (Docling):** Converts complex PDFs and DOCX files into structural Markdown to preserve semantic context for chunking.
2. **Hybrid Retrieval:** An **Ensemble Retriever** combines keyword-based **BM25** with semantic **Vector Search** (ChromaDB) to ensure maximum recall accuracy.
3. **Synthesis Engine:** A lead agent generates context-grounded responses using Llama-3.2-90B.
4. **Verification Loop:** A dedicated node audits the synthesis against the original context using Granite-4, providing a detailed verification report.

![Gradio Interface Preview](images/gradio_ui.png)
*Figure 2: User interface showing PDF upload and context-grounded chat interaction.*

---

## 🚀 Key Features

- **Docling Integration:** Advanced text-to-markdown conversion for better semantic chunking.
- **SHA-256 Content Caching:** Implements persistent document caching to avoid redundant processing of previously uploaded files.
- **Self-Correction Loop:** Automatic identification of unsupported claims and contradictions in the research report.
- **Session-State Management:** Gradio-based interface that maintains document indices and hashes across user queries.

---

## ⚙️ Execution Guide

### 1. Clone the repository
```bash
git clone [https://github.com/fvalerii/agentic-langchin-rag.git](https://github.com/fvalerii/agentic-langchain-rag.git)
cd agentic-langhchain-rag
```

### 2. Set-up Credential

1. Locate the `.env` file in the root directory .

2. Fill in your token keys:
```bash
# Watsonx Config
WATSONX_API_KEY=your_ibm_api_key
PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Persistence Config
CHROMA_DB_PATH=./chroma_db
CACHE_DIR=document_cache
```

### 3. Run the Application
This project uses `uv` for simplified and accelerated dependency management and can be launched directly without manual environment setup:

```bash
# Launch the DocChat Agentic Terminal
uv run app.py
```

---

## 🛠️ System Operations & Maintenance

### **Persistent Caching Logic**
The system uses a sophisticated `DocumentProcessor` to manage resources and speed up repeated research:

- **Hash-Based Recovery:** Before processing, the system generates a content-based SHA-256 hash. If the file exists in the document_cache, it loads the pre-processed chunks instantly.
- **Safety Limits:** Built-in constants prevent memory overflows by enforcing a 50MB per-file limit and a 200MB total session limit.

---

## 💻 Tech Stack: Agentic Backend

### 🏢 Version A: Enterprise Watsonx (LTS)
Optimized for the 2026 IBM Watsonx ecosystem with high-fidelity orchestration.

- **Orchestration:** `LangGraph` & `LangChain`
- **Synthesis LLM:** `meta-llama/llama-3-2-90b-vision-instruct` 
- **Verification LLM:** `ibm/granite-4-h-small`
- **Routing LLM:** `ibm/granite-3-3-8b-instruct`
- **Embeddings:** `ibm/slate-125m-english-rtrvr-v2`
- **Vector Database:** **ChromaDB**
- **Parsing Engine:** **Docling** (Text-to-Markdown)

---

##  Credits
Designed for high-fidelity research and autonomous document analysis.
