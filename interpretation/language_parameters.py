from dataclasses import dataclass
from typing import Literal

from engine.profile_traits import (
    PHYSICAL_PROFILE_MAP,
    EMOTIONAL_PROFILE_MAP,
    INTELLECTUAL_PROFILE_MAP,
)

# -------------------------
# LANGUAGE CONTRACT
# -------------------------

DirectiveStyle = Literal["direct", "structured", "supportive", "minimal"]
EmotionalTone = Literal["neutral", "warm", "contained", "soft"]
CognitiveDensity = Literal["low", "moderate", "high"]
InstructionStructure = Literal["stepwise", "compact", "expanded"]

@dataclass(frozen=True)
class LanguageParameters:
    directive_style: DirectiveStyle
    emotional_tone: EmotionalTone
    cognitive_density: CognitiveDensity
    instruction_structure: InstructionStructure


# -------------------------
# MAIN BUILDER
# -------------------------

def build_language_parameters(
    physical_id: str,
    emotional_id: str,
    intellectual_id: str,
) -> LanguageParameters:

    # ---- VALIDATION ----
    if physical_id not in PHYSICAL_PROFILE_MAP:
        raise ValueError(f"Unknown physical profile: {physical_id}")

    if emotional_id not in EMOTIONAL_PROFILE_MAP:
        raise ValueError(f"Unknown emotional profile: {emotional_id}")

    if intellectual_id not in INTELLECTUAL_PROFILE_MAP:
        raise ValueError(f"Unknown intellectual profile: {intellectual_id}")

    physical = PHYSICAL_PROFILE_MAP[physical_id]
    emotional = EMOTIONAL_PROFILE_MAP[emotional_id]
    intellectual = INTELLECTUAL_PROFILE_MAP[intellectual_id]

    # -------------------------
    # DIRECTIVE STYLE (from PH)
    # -------------------------

    if physical["energy_style"] == "outward":
        directive_style = "direct"
    elif physical["boundary_style"] in ["goal-driven", "reactive-driven"]:
        directive_style = "structured"
    elif physical["energy_style"] == "inward":
        directive_style = "supportive"
    else:
        directive_style = "minimal"

    # -------------------------
    # EMOTIONAL TONE (from EM)
    # -------------------------

    if emotional["trait_emotional_intensity"] == "low":
        emotional_tone = "contained"
    elif emotional["trait_relational_orientation"] == "high":
        emotional_tone = "warm"
    elif emotional["trait_boundary_permeability"] == "withdrawn":
        emotional_tone = "neutral"
    else:
        emotional_tone = "soft"

    # -------------------------
    # COGNITIVE DENSITY (from IN)
    # -------------------------

    abstraction = intellectual["trait_abstraction_level"]
    decision = intellectual["trait_decision_speed"]

    if abstraction == "high" and decision == "high":
        cognitive_density = "high"
    elif abstraction == "low":
        cognitive_density = "low"
    else:
        cognitive_density = "moderate"

    # -------------------------
    # INSTRUCTION STRUCTURE (from IN + PH)
    # -------------------------

    structure_need = intellectual["trait_structure_need"]

    if structure_need in ["precise", "executive"]:
        instruction_structure = "stepwise"
    elif structure_need in ["integrative", "integrative-precise"]:
        instruction_structure = "expanded"
    else:
        instruction_structure = "compact"

    return LanguageParameters(
        directive_style=directive_style,
        emotional_tone=emotional_tone,
        cognitive_density=cognitive_density,
        instruction_structure=instruction_structure,
    )

