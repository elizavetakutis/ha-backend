from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import asyncio

from engine.calculator import run_calculation, extract_comm_state
from interpretation.protocol_assembly import assemble_protocol

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


class SessionRunRequest(BaseModel):
    doctor: DoctorInfo
    input: InputData


# -------------------------
# Background processing
# -------------------------

async def process_session(session_id: str):
    try:
        input_data: InputData = sessions[session_id]["input"]

        # Internal calculation (полная модель остаётся внутри)
calculation_result = run_calculation(input_data)

# 🔐 Extract encoded communication state (только 4 показателя)
comm_state = extract_comm_state(calculation_result)

# Берем raw protocol text
raw_text = input_data.protocol_content or ""

# Собираем финальный текст (без передачи полной модели)
final_output = assemble_protocol(
    raw_text=raw_text,
    comm_state=comm_state
)
        # Сохраняем INTERNAL (для будущих слоев)
        sessions[session_id]["internal"] = calculation_result

        # Сохраняем PUBLIC (только output)
        sessions[session_id]["public"] = {
            "output": final_output
        }

        sessions[session_id]["status"] = "completed"

    except Exception as e:
        sessions[session_id]["status"] = "error"
        sessions[session_id]["public"] = {
            "output": None
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
        "internal": None,
        "public": None
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

    session = sessions[session_id]

    if session["status"] != "completed":
        return {
            "status": session["status"]
        }

    # 🔐 Возвращаем только PUBLIC
    return {
        "status": "completed",
        "output": session["public"]["output"]
    }

