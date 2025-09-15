# AI-Powered Alumni Engagement & Management System  
**Smart India Hackathon 2025 â€“ Problem Statement ID 25017**

---

## Overview  
This project is an **AI-powered Alumni Engagement and Management System** designed to bridge the gap between alumni, students, and institutions. It combines **resume parsing, alumni search, fraud detection, event management, and conversational AI** into a single platform.

The system integrates:  
- **Resume Parser** (TinyLlama 1.1B local inference)  
- **AI Chatbot with RAG** (Ollama LLaMA3 + FAISS + HuggingFace embeddings)  
- **Alumni Databases** (SQLite + MongoDB)  
- **FastAPI Backend APIs**  
- **Frontend UI** (Donation Page, Alumni Map, Chatbot Widget, Login/Signup)  

---

## System Architecture  

Resume Upload â†’ Resume Parser â†’ Alumni Database â†’ FAISS Vectorstore â†’ RAG Service (Ollama + Embeddings) â†’ FastAPI API â†’ Frontend (Donation Page, Alumni Map, Chatbot, Login/Signup)

### Key Components
- **Resume Parser**  
  - Extracts text from PDF/DOCX resumes  
  - Normalizes skills, validates social media links  
  - Outputs structured JSON  

- **Database Layer**  
  - SQLite: Resume parsing + deduplication (SHA-256 hash)  
  - MongoDB: Central alumni DB for RAG queries  

- **RAG Service (Chatbot)**  
  - LLaMA3 (via Ollama) for natural Q&A  
  - HuggingFace embeddings (`all-MiniLM-L6-v2`)  
  - FAISS for semantic search  
  - Session-based conversation memory  

- **FastAPI Backend**  
  - REST APIs for resume parsing, alumni addition, querying, chat history, embeddings update, health check  

- **Frontend**  
  - Donation page with preset/custom amounts  
  - Interactive alumni map (LeafletJS)  
  - Alumni news/events dashboard  
  - Chatbot widget with backend integration  

---

## Setup Instructions  

### 1. Clone the Repo
```bash
git clone https://github.com/IIT-LMNOP/ASAP.git
cd ASAP
```

### 2. Backend Setup
- Install Python dependencies:
```bash
pip install -r requirements.txt
```

- Run MongoDB locally or connect to a remote cluster  
- Initialize sample alumni data:
```bash
python setup_sample_data.py
```

- Start FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Resume Parser
- Upload PDF/DOCX resumes via:
```bash
POST /parse-resume/
```

### 4. RAG Chatbot
- Query alumni database via:
```bash
POST /query
```

Example request:
```json
{
  "question": "Who works at Google?",
  "session_id": "demo1"
}
```

### 5. Frontend
- Open the frontend directory in a browser (static HTML/JS).  
- Connects to backend APIs for donations, alumni map, and chatbot.

---

## Features Implemented  

- âœ… Resume parsing with TinyLlama-1.1B  
- âœ… SQLite + MongoDB alumni databases  
- âœ… RAG chatbot with FAISS + embeddings  
- âœ… FastAPI APIs for alumni management  
- âœ… Demo alumni dataset (Google, Microsoft, Tesla, etc.)  
- âœ… Frontend UI: donation, map, chatbot, signup/login  

---

## Feasibility and Viability  

### Feasibility
- Extends existing alumni portal infrastructure  
- AI/ML models available for resume parsing, fraud detection, recommendations  
- Interactive dashboards and maps for alumni presence and events  
- Real-time communication tools (chat, notifications)  
- Scalable event management (RSVP, prediction, reminders)  

### Risks
- Data privacy & security of alumni/student information  
- Accuracy of AI models (fraud detection, event prediction)  
- Alumni/student adoption & trust  
- Cost of cloud hosting and integrations  

### Mitigation Strategies
- Strong encryption & access control  
- Hybrid AI + manual verification for critical tasks  
- Awareness campaigns + simple UI  
- Phased rollout (resume parser â†’ chatbot â†’ maps â†’ events)  
- Partnerships with cloud providers & payment gateways  

---

## Roadmap (Next Steps)  
- [ ] Merge resume parser + RAG into unified backend  
- [ ] Add authentication and role-based access control  
- [ ] Cloud deployment (AWS/GCP/Azure)  
- [ ] Payment gateway integration for donations  
- [ ] Structured chatbot JSON responses  
- [ ] Event attendance prediction & analytics  

---

## Contributors  
**Team ASAP** Smart India Hackathon 2025  

---

## License  
This project is licensed under the MIT License.
