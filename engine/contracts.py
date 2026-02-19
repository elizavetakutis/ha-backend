# engine/contracts.py
from pydantic import BaseModel, Field
from typing import Dict, Optional, Literal

SchemaVersion = Literal["1.0"]

class ProfilesIDs(BaseModel):
    physical: str
    emotional: str
    intellectual: str

class Systems(BaseModel):
    structural: int
    adaptive: int
    metabolic: int
    emotional: int
    expression: int
    cognitive: int

class Prakruti(BaseModel):
    kapha: int
    pitta: int
    vata: int
    type: str

class YinYang(BaseModel):
    yin: int
    yang: int
    direction: str
    balance_index: Optional[float] = None

class Tension(BaseModel):
    want: int
    can: int
    magnetism: int
    tension_ratio: Optional[float] = None

class CalcResultInternal(BaseModel):
    schema_version: SchemaVersion = Field(default="1.0")
    markers: Dict[str, int]  # {"physical": X, "emotional": Z, "intellectual": K}
    profiles: ProfilesIDs    # ONLY IDs (PHxx/EMxx/INxx)
    systems: Systems
    prakruti: Prakruti
    yin_yang: YinYang
    tension: Tension

