from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import asyncio

app = FastAPI(title="HA Backend API", version="0.2")

# -------------------------
# CORS (Shopify connection)
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://4doctors.us"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# In-memory session storage
# -------------------------

sessions = {}

# -------------------------
# Models
# -------------------------

class DoctorInfo(BaseModel):
    shopify_customer_id: str
    email: Optional[str] = None
    access_level: Optional[str] = None


class InputData(BaseModel):
    patient_dob: str
    protocol_type: str
    protocol_content: str


class SessionRunRequest(BaseModel):
    doctor: DoctorInfo
    input: InputData


# -------------------------
# Background processing
# -------------------------

async def process_session(session_id: str):
    await asyncio.sleep(3)  # имитация AI обработки

    sessions[session_id]["status"] = "completed"
    sessions[session_id]["result"] = {
        "summary": "Mock clinical interpretation completed.",
        "recommendations": [
            "Increase magnesium intake",
            "Optimize vitamin D levels",
            "Review inflammatory markers"
        ]
    }


# -------------------------
# Endpoints
# -------------------------

@app.get("/")
def health_check():
    return {"status": "ok", "message": "HA backend is running"}


@app.post("/sessions/run")
async def run_session(payload: SessionRunRequest):
    session_id = str(uuid4())

    sessions[session_id] = {
        "status": "processing",
        "result": None
    }

    # запускаем асинхронную обработку
    asyncio.create_task(process_session(session_id))

    return {
        "status": "accepted",
        "session_id": session_id
    }


@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        return {
            "status": "not_found",
            "message": "Session not found"
        }

    return sessions[session_id]





