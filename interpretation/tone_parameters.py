from dataclasses import dataclass
from typing import Literal


MagnetismLevel = Literal["low", "normal"]


@dataclass(frozen=True)
class ToneParameters:
    authority_distance: Literal["low", "neutral"]
    directive_intensity: Literal["low", "normal"]
    validation_level: Literal["high", "normal"]
    emotional_softening: Literal["high", "low"]
    phrasing_style: Literal["collaborative", "direct"]


def build_tone_parameters(magnetism_level: MagnetismLevel) -> ToneParameters:
    """
    Builds tone parameters based strictly on normalized magnetism level.

    Magnetism scale (defined in internal_state):
        raw < 1000  -> "low"
        raw >= 1000 -> "normal"

    This function must remain independent from engine logic.
    """

    if magnetism_level not in ("low", "normal"):
        raise ValueError(
            f"Invalid magnetism level: {magnetism_level}. "
            "Expected 'low' or 'normal'."
        )

    if magnetism_level == "low":
        return ToneParameters(
            authority_distance="low",
            directive_intensity="low",
            validation_level="high",
            emotional_softening="high",
            phrasing_style="collaborative",
        )

    return ToneParameters(
        authority_distance="neutral",
        directive_intensity="normal",
        validation_level="normal",
        emotional_softening="low",
        phrasing_style="direct",
    )
