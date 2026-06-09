# 🧠 CogniFlow: Autonomous RAG Knowledge Platform

**CogniFlow** is a next-generation Retrieval-Augmented Generation (RAG) system that transforms static documents into a dynamic, searchable, and chat-capable knowledge base. Built with a decoupled architecture, it features a high-performance Python backend and a real-time streaming Next.js interface.

screenshot

## 🚀 Key Features

*   **Real-Time Streaming AI:** Leverages **WebSockets** and **NVIDIA/Groq-powered reasoning models (Kimi-k2.5 / Llama 3.3)** to stream answers word-by-word for an elite user experience.
*   **Semantic Vector Vault:** Built on **ChromaDB**, the system uses mathematical embeddings to find relevant context in milliseconds, moving beyond simple keyword search.
*   **Autonomous File Watcher:** A background **Multithreaded Watcher** monitors your local directory. Drop a new PDF in, and the AI "learns" it automatically without a server restart.
*   **Targeted Context Search:** Users can chat with their entire library or "lock" the AI to a specific document for high-precision analysis.
*   **Advanced Document Ingestion:** Custom-built ingestion engine that handles PDF extraction, recursive chunking, and **Overlapping Sliding Windows** to preserve semantic context.

## 🛠️ Tech Stack

*   **Backend:** Python 3.12, FastAPI
*   **AI/LLM:** Groq API / NVIDIA NIM (OpenAI SDK Standard)
*   **Vector Database:** ChromaDB
*   **Document Processing:** PyMuPDF (Fitz)
*   **Frontend:** Next.js 14, React, TypeScript, Tailwind CSS
*   **State Management:** React Hooks (useRef, useEffect, useState)
*   **Real-time:** WebSockets
*   **Automation:** Watchdog (Filesystem Events)

## 🏗️ System Architecture

CogniFlow is designed as a **Microservice System**:

1.  **The Ingestor:** Breaks unstructured PDFs into smart, overlapping text chunks.
2.  **The Vault:** Generates high-dimensional vectors and stores them in a persistent local store.
3.  **The Watcher:** An autonomous thread that syncs the physical filesystem with the digital database.
4.  **The Brain:** An orchestration layer that bridges the user's question with retrieved context and the LLM.
5.  **The Interface:** A responsive Next.js dashboard featuring live-sync sidebars and citation-ready chat bubbles.

## 📦 Installation & Setup

### Prerequisites
*   [Groq API Key](https://console.groq.com/)
*   Node.js & Python 3.12+

### Backend Setup
1.  `cd backend`
2.  Create a `.env` file:
    ```text
    GROQ_API_KEY=your_key_here
    GROQ_BASE_URL=https://api.groq.com/openai/v1
    ```
3.  `uv run uvicorn main:app --reload`

### Frontend Setup
1.  `cd frontend`
2.  `npm install`
3.  `npm run dev`

## 🔮 Roadmap
- [ ] Multi-user session management
- [ ] OCR support for scanned documents
- [ ] Cloud deployment via Docker & AWS

---
**Developed by MUIZ UD DIN**  
*Full-Stack AI Automation Engineer | Available for high-impact projects on Upwork.*