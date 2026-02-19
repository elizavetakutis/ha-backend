# engine/contracts.py

from pydantic import BaseModel, Field
from typing import Dict, Optional, Literal, Any


SchemaVersion = Literal["1.0"]


# -------------------------
# MARKERS
# -------------------------

class Markers(BaseModel):
    physical: int
    emotional: int
    intellectual: int


# -------------------------
# PROFILES (RAW DICTS FROM HUMAN_ARCHITECTURE_MARKERS)
# -------------------------

class ProfilesRaw(BaseModel):
    physical: Dict[str, Any]
    emotional: Dict[str, Any]
    intellectual: Dict[str, Any]


# -------------------------
# SYSTEMS
# -------------------------

class Systems(BaseModel):
    structural: int
    adaptive: int
    metabolic: int
    emotional: int
    expression: int
    cognitive: int


# -------------------------
# PRAKRUTI
# -------------------------

class Prakruti(BaseModel):
    kapha: int
    pitta: int
    vata: int
    type: str


# -------------------------
# YIN / YANG
# -------------------------

class YinYang(BaseModel):
    yin: int
    yang: int
    direction: str
    balance_index: Optional[float] = None


# -------------------------
# TENSION
# -------------------------

class Tension(BaseModel):
    want: int
    can: int
    magnetism: int
    tension_ratio: Optional[float] = None


# -------------------------
# FINAL CALC RESULT (MATCHES run_calculation EXACTLY)
# -------------------------

class CalcResultInternal(BaseModel):
    schema_version: SchemaVersion = Field(default="1.0")
    markers: Markers
    profiles: ProfilesRaw
    systems: Systems
    prakruti: Prakruti
    yin_yang: YinYang
    tension: Tension
    output: Optional[str] = None

