from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest
from app.graph import run_graph
from app.database import initialize_database

app = FastAPI(
    title="AI CRM Assistant API",
    version="1.0.0",
)

# -------------------------------------------------
# Startup
# -------------------------------------------------

@app.on_event("startup")
def startup():
    initialize_database()
    print("✅ Database Initialized")


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Root
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "🚀 AI CRM Backend Running Successfully"
    }


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -------------------------------------------------
# Chat Endpoint
# -------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    response = run_graph(request.message)

    return response