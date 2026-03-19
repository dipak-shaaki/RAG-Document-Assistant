# RAG Document Assistant Backend

A backend service with two REST APIs built using FastAPI. This project provides a complete RAG (Retrieval-Augmented Generation) pipeline for document ingestion and conversational answering, featuring multi-turn chat memory and automatic interview booking detection.

Built without `FAISS`, `Chroma`, `RetrievalQAChain`, or UI to strictly follow backend and algorithmic constraints.

## 🚀 Features & Architecture

### 1. Document Ingestion API (`POST /ingest/upload`)
- **File Parsing**: Extracts text from `.pdf` and `.txt` files.
- **Selectable Chunking**: Supports two strategies (`fixed` and `sentence`).
- **Embedding Generation**: Uses the fast, local `sentence-transformers` (`all-MiniLM-L6-v2`).
- **Vector Storage**: Stores embeddings and payload in **Qdrant** (running via strict local persistent mode, fulfilling the no-FAISS/Chroma constraint).
- **Metadata DB**: Stores document metadata (chunks, filenames, upload time) in **SQLite** via SQLAlchemy ORM.

### 2. Conversational RAG API (`POST /chat/`)
- **Custom RAG Implementation**: Completely manual retrieval and prompt augmentation (no LangChain `RetrievalQAChain` used).
- **Redis Chat Memory**: Stores conversation multi-turn history per `session_id` using **Redis** (falls back to in-memory dict if Redis server isn't running).
- **Smart Interview Booking**: 
  - **LLM Intent Detection**: The LLM parses user queries to detect interview requests.
  - **Data Extraction**: Once it detects `name`, `email`, `date`, and `time` in the conversation exchange, it automatically extracts them as structured JSON.
  - **Booking Storage**: Saves the extracted booking securely into the **SQLite** DB.

## 🛠 Tech Stack
- **Framework**: FastAPI
- **LLM Integration**: Groq API (LLaMA 3.3) / OpenAI compatible
- **Embeddings**: Sentence-Transformers
- **Vector Database**: Qdrant (Persistent)
- **Relational Database**: SQLite + SQLAlchemy
- **Cache / Memory**: Redis
- **File Parsing**: PyPDF2

---

## 💻 Setup & Installation

### 1. Prerequisites
- Python 3.10+
- Redis Server (Running locally on default port `6379`)

### 2. Environment Setup
Clone the repository and install dependencies:

```bash
git clone <your-github-repo-url>
cd RAG-Document-Assistant
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file based on the provided configuration:
```env
# Get a free API key at: https://console.groq.com/keys
GROQ_API_KEY=your_free_groq_api_key_here

REDIS_URL=redis://localhost:6379/0
QDRANT_PATH=./qdrant_data
DATABASE_URL=sqlite:///./app_data.db
LLM_MODEL=llama-3.3-70b-versatile
```

### 4. Run the API Server
Start the Uvicorn server:
```bash
uvicorn app.main:app --reload
```
The API is now running at `http://127.0.0.1:8000`. You can visit `http://127.0.0.1:8000/docs` to view the interactive Swagger API documentation.

---

## 📖 API Endpoints

### 1. Upload a Document
**POST** `/ingest/upload`
Uploads a document and chunks its contents.
- **Parameters**: `strategy` (`fixed` or `sentence`)
- **Body**: `multipart/form-data` containing a `file` (.txt or .pdf)

### 2. Chat with the Assistant
**POST** `/chat/`
Ask questions based on the uploaded documents or book an interview.
- **Body**: 
```json
{
  "session_id": "user_123",
  "query": "What is the capital of France?"
}
```

### 3. View All Bookings
**GET** `/bookings/`
Retrieve the list of all interviews booked via the Chat API.

## 📏 Application Constraints & Standards Met
- **Clean Architecture**: Separated concerns via `api`, `core`, `database`, `schemas`, and `services` modules.
- **Typing**: Extensive use of Python 3.10+ type hints and Pydantic validation throughout the code.
- **No FAISS/Chroma**: Exclusively utilizes Qdrant for dense vector storage.
- **No UI**: Backend and API logic strictly implemented.
- **No RetrievalQAChain**: The RAG pipeline and system prompts have been crafted natively.