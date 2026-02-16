from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import asyncio

from engine.calculator import run_calculation

app = FastAPI(title="HA Backend API", version="0.5")

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://4doctors.us",
        "https://www.4doctors.us",
    ],
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
    protocol_type: Optional[str] = None
    protocol_content: Optional[str] = None
    
    # ✅ НОВОЕ ПОЛЕ
    raw_protocol_text: Optional[str] = None


class SessionRunRequest(BaseModel):
    doctor: DoctorInfo
    input: InputData


# -------------------------
# Background processing
# -------------------------

async def process_session(session_id: str):
    try:
        input_data: InputData = sessions[session_id]["input"]

        # Передаем всё в калькулятор
        result = run_calculation(input_data)

        sessions[session_id]["status"] = "completed"
        sessions[session_id]["result"] = result

    except Exception as e:
        sessions[session_id]["status"] = "error"
        sessions[session_id]["result"] = {
            "error": str(e)
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
        "input": payload.input,
        "result": None
    }

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






