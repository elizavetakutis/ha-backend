from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI(title="HA Backend API", version="0.3")

# =========================
# CORS CONFIG
# =========================

origins = [
    "https://4doctors.us",
    "https://www.4doctors.us",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# In-memory storage
# =========================

sessions = {}

# =========================
# Models
# =========================

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


# =========================
# Endpoints
# =========================

@app.get("/")
def health_check():
    return {"status": "ok", "message": "HA backend is running"}


@app.post("/sessions/run")
def run_session(payload: SessionRunRequest):
    session_id = str(uuid4())

    sessions[session_id] = {
        "status": "processing",
        "result": None
    }

    return {
        "status": "accepted",
        "session_id": session_id
    }


@app.get("/sessions/{session_id}")
def get_session_status(session_id: str):
    if session_id not in sessions:
        return {
            "status": "not_found",
            "message": "Session not found"
        }

    return {
        "status": sessions[session_id]["status"],
        "result": sessions[session_id]["result"]
    }




