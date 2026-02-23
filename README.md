# Max Blog AI Assistant (RAG System)

A Retrieval-Augmented Generation (RAG) system built on top of the articles published on 
https://maximilian-schwarzmueller.com/

This project indexes blog articles and enables semantic search + intelligent Q&A over the content using hybrid retrieval (Dense + Sparse).

---

## 🚀 Project Overview

This project demonstrates a full RAG pipeline applied to a real-world technical blog.

Instead of keyword-only search, this system:
- Understands natural language questions
- Retrieves relevant articles semantically
- Uses LLMs to generate context-aware answers
- Combines dense and sparse retrieval for improved performance

---

## 🧠 Architecture

User Query
↓
Query Processing
↓
Hybrid Retrieval (Dense + Sparse)
↓
Context Construction
↓
LLM Answer Generation
↓
Final Response

---

## 🏗️ Tech Stack

- Python 3.12
- FastAPI (API layer)
- FAISS / Vector DB
- Elasticsearch / BM25 (Sparse retrieval)
- OpenAI / LLM provider
- BeautifulSoup / Scraper
- HuggingFace Embeddings
- Docker (optional)

---

## 📂 Project Structure
```
.
├── scraper/
│ ├── scrape_articles.py
│ └── parser.py
├── indexing/
│ ├── chunking.py
│ ├── embedder.py
│ └── vector_store.py
├── retrieval/
│ ├── dense_retriever.py
│ ├── sparse_retriever.py
│ └── hybrid_retriever.py
├── generation/
│ └── answer_generator.py
├── api/
│ └── main.py
├── requirements.txt
└── README.md
```
---

## 🔍 RAG Pipeline

### 1️⃣ Data Collection
- Crawl the articles section
- Extract title, content, metadata
- Store raw HTML/text

### 2️⃣ Text Processing
- Clean HTML
- Chunk into semantic blocks
- Store metadata

### 3️⃣ Embedding & Indexing
- Generate embeddings
- Store in vector database
- Index full text for BM25

### 4️⃣ Hybrid Retrieval
- Dense retrieval (semantic similarity)
- Sparse retrieval (keyword matching)
- Combine scores

### 5️⃣ LLM Answer Generation
- Build context from top-k results
- Generate final answer using LLM

---

## 💬 Example Query

User Question:
> "What does Max think about AI replacing developers?"

System:
- Retrieves relevant article(s)
- Extracts contextual paragraphs
- Generates structured answer

---

## 🎯 Why This Project?

- Demonstrates real-world RAG
- Hybrid retrieval (dense + sparse)
- Clean architecture design
- Practical AI search implementation
- Portfolio-ready AI system

---

## 🛠️ Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/max-blog-ai-assistant.git
cd max-blog-ai-assistant
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_api_key_here
VECTOR_DB_PATH=./data/vector_store
ELASTICSEARCH_HOST=localhost
```

---

### 5️⃣ Run the Application

```bash
uvicorn api.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

---

### 6️⃣ Test the API

Open:

```
http://127.0.0.1:8000/docs
```

This will open the interactive Swagger UI.

---

## 📊 Future Improvements
- Add query reformulation agent
- Add re-ranking model
- Add streaming responses
- Add evaluation metrics (Recall@K, MRR)
- Add UI (React / Next.js frontend)
- Deploy to cloud (AWS / GCP)

---

## ⚠️ Disclaimer

This project is built for educational and research purposes.
All original article content belongs to the respective author.
