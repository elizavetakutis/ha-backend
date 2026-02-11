from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI(title="HA Backend API", version="0.1")


# -----------------------
# CORS — ОБЯЗАТЕЛЬНО
# -----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://4doctors.us",
        "https://www.4doctors.us"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# Models
# -----------------------

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


# -----------------------
# Endpoints
# -----------------------

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "HA backend is running"
    }


@app.post("/sessions/run")
def run_session(payload: SessionRunRequest):
    session_id = str(uuid4())

    return {
        "status": "accepted",
        "session_id": session_id,
        "received": True
    }


