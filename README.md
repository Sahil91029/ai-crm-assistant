# 🤖 AI-First CRM HCP Module

An AI-powered Healthcare Professional (HCP) Interaction Logging System built using **React, Redux, FastAPI, LangGraph, and AI-assisted information extraction**.

This project was developed as part of the AI-First CRM Technical Assessment.

---

# 🚀 Features

- AI-powered HCP interaction logging
- Conversational Chat Interface
- Voice-to-Text Interaction
- Automatic CRM Form Filling
- LangGraph AI Agent
- Five AI Tools
- SQLite Database
- FastAPI Backend
- React + Redux Frontend
- Responsive UI

---

# 🏗 Architecture

```
                User

                  │

      Voice / Text Interaction

                  │

             React Frontend

                  │

               Redux Store

                  │

             FastAPI Backend

                  │

              LangGraph Agent

                  │

         Tool Selection Logic

                  │

    ┌─────────────┼─────────────┐
    │             │             │
Search      Log Interaction   Edit
    │             │             │
Summary      Follow-up      Database
    │
Extractor / LLM Layer

                  │

              SQLite Database
```

---

# 🧠 LangGraph Agent

The LangGraph agent determines which tool should execute based on the user's message.

Implemented tools:

1. Log Interaction
2. Edit Interaction
3. Search HCP
4. Summarize Interaction
5. Suggest Follow-up

---

# 🤖 AI Information Extraction

The AI extracts:

- HCP Name
- Interaction Type
- Date
- Time
- Attendees
- Topics Discussed
- Materials Shared
- Samples Distributed
- Sentiment
- Outcome
- Follow-up Actions

and automatically updates the CRM form.

---

# 🎤 Voice Assistant

Uses the browser Speech Recognition API.

Features:

- Voice Recording
- Live Transcription
- Automatic Chat Input
- Automatic Form Update

---

# 🗄 Database

SQLite database stores:

- Doctor
- Date
- Time
- Topics
- Materials
- Samples
- Sentiment
- Outcome
- Follow-up

---

# ⚙ Tech Stack

## Frontend

- React
- Redux Toolkit
- Tailwind CSS
- Axios

## Backend

- FastAPI
- LangGraph
- SQLite
- Python

---

# 📂 Project Structure

```
frontend/

components/
pages/
redux/
services/

backend/

app/

graph.py
tools.py
extractor.py
database.py
llm.py
main.py
schemas.py
```

---

# ▶ Running

## Backend

```
cd backend

python -m venv .venv

pip install -r requirements.txt

python -m uvicorn app.main:app --reload
```

Backend:

```
https://ai-crm-assistant-vrp7.onrender.com
```

Swagger:

```
https://ai-crm-assistant-vrp7.onrender.com
```

---

## Frontend

```
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# 🎥 Demo

Features demonstrated:

- Voice Interaction
- Chat Interface
- AI Extraction
- Auto Form Filling
- LangGraph Tool Selection
- Database Storage

---

# 📌 Future Improvements

The project includes an `llm.py` abstraction layer designed for integration with **Groq (gemma2-9b-it)**. During development, Groq account creation was temporarily unavailable due to service issues, so the application currently uses a deterministic extraction fallback while preserving the same architecture. Replacing the fallback requires configuring a `GROQ_API_KEY`; no frontend or LangGraph changes are needed.

---

# 👨‍💻 Author

**Md Sahil Raza Khan**

Frontend Developer

React | FastAPI | LangGraph
