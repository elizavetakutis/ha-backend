from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
from uuid import uuid4
from datetime import datetime

app = FastAPI(title="HA Backend API", version="0.3")

# ------------------------
# CORS (ОБЯЗАТЕЛЬНО)
# ------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # потом можно ограничить
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# In-memory session store
# ------------------------

SESSIONS: Dict[str, dict] = {}

# ------------------------
# Models
# ------------------------

class DoctorInfo(BaseModel):
    shopify_customer_id: str
    email: Optional[str] = None
    access_level: Optional[str] = None


class InputData(BaseModel):
    patient_dob: str
    protocol_type: str
    protocol_content: str
    lifestyle_enabled: bool = False


class SessionRunRequest(BaseModel):
    doctor: DoctorInfo
    input: InputData


# ------------------------
# Endpoints
# ------------------------

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "HA backend is running",
        "version": "0.3"
    }


@app.post("/sessions/run")
def run_session(payload: SessionRunRequest):
    session_id = str(uuid4())

    result_summary = {
        "analysis_status": "completed",
        "clinical_vector": "metabolic-dominant",
        "lifestyle_block_included": payload.input.lifestyle_enabled,
        "timestamp": datetime.utcnow().isoformat()
    }

    SESSIONS[session_id] = {
        "session_id": session_id,
        "status": "completed",
        "created_at": datetime.utcnow().isoformat(),
        "doctor": payload.doctor.dict(),
        "input": payload.input.dict(),
        "result": result_summary
    }

    return {
        "status": "accepted",
        "session_id": session_id
    }


@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    session = SESSIONS.get(session_id)

    if not session:
        return {
            "status": "not_found",
            "message": "Session not found"
        }

    return {
        "status": "success",
        "data": session
    }

