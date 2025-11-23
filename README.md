# Omni-Agent Knowledge Hub

**Omni-Agent Knowledge Hub** is a unified AI platform that integrates advanced Generative AI concepts into a single, modular application. It combines Retrieval-Augmented Generation (RAG), autonomous agents, multi-modal ingestion, and code generation to create a powerful research and development assistant.

## 🚀 Features

*   **🧠 Intelligent Routing (LangGraph)**: An autonomous agent that dynamically routes user queries to either a specialized Vector Store (for internal knowledge) or Wikipedia (for general knowledge).
*   **📚 Multi-Modal Ingestion**:
    *   **PDF RAG**: Upload and index PDF documents for deep semantic search.
    *   **YouTube & Web Summarization**: Ingest YouTube videos or website URLs, generate concise summaries, and store the content for future querying.
*   **💾 Vector Memory (AstraDB)**: Uses DataStax AstraDB as a serverless vector store to maintain long-term knowledge.
*   **💻 Dedicated Code Assistant**: A specialized mode powered by **CodeLlama** (via Ollama) to assist with programming tasks, debugging, and script generation.
*   **🎨 Modern UI**: A clean, glassmorphism-inspired interface built with vanilla HTML/CSS/JS for a lightweight and responsive experience.

## 🛠️ Tech Stack

*   **Backend**: FastAPI, Python
*   **Frontend**: HTML5, CSS3, JavaScript
*   **AI/ML Frameworks**: LangChain, LangGraph
*   **Database**: DataStax AstraDB (Vector Store)
*   **LLMs**:
    *   **Groq** (Llama 3) for fast inference and routing.
    *   **Ollama** (CodeLlama) for local code generation.
    *   **HuggingFace** for embeddings.

## 📋 Prerequisites

Ensure you have the following installed/configured:

*   **Python 3.9+**
*   **Ollama** (running locally with `codellama` model pulled)
*   **API Keys**:
    *   Groq API Key
    *   AstraDB Token & Endpoint
    *   HuggingFace Token

## ⚙️ Installation

1.  **Clone the repository** (if applicable) or navigate to the project folder:
    ```bash
    cd omniAgent_knowledge_hub
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your credentials:
    ```env
    GROQ_API_KEY="your_groq_key"
    ASTRA_DB_APPLICATION_TOKEN="your_astra_token"
    ASTRA_DB_API_ENDPOINT="your_astra_endpoint"
    HF_TOKEN="your_hf_token"
    OLLAMA_BASE_URL="http://localhost:11434"
    ```

## 🚀 Usage

1.  **Start the Backend Server**:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will run at `http://localhost:8000`.

2.  **Launch the Frontend**:
    Open `frontend/index.html` in your preferred web browser.

3.  **Interact**:
    *   **General Knowledge**: Ask questions. The agent will decide whether to use your uploaded documents or Wikipedia.
    *   **Ingest**: Use the sidebar to upload PDFs or paste YouTube URLs.
    *   **Code Mode**: Switch to "Code Assistant" to generate code snippets.

## 📂 Project Structure

```
omniAgent_knowledge_hub/
├── backend/
│   └── main.py          # FastAPI application & endpoints
├── frontend/
│   ├── index.html       # Main UI
│   ├── style.css        # Styling
│   └── script.js        # Frontend logic & API calls
├── model/
│   ├── agent.py         # LangGraph agent & routing logic
│   ├── ingestion.py     # PDF/URL processing & summarization
│   ├── vector_store.py  # AstraDB connection & embedding logic
│   └── code_assistant.py# Ollama integration for code gen
├── .env                 # API keys (not shared)
└── requirements.txt     # Python dependencies
```

---
*Built as a demonstration of Agentic AI capabilities.*
