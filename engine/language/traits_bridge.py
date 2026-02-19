# engine/language/traits_bridge.py

from __future__ import annotations

from typing import Dict, Any

from engine.contracts import CalcResultInternal


# -------------------------
# Errors
# -------------------------

class TraitsBridgeError(Exception):
    """Base error for traits bridge."""


class InvalidProfilesStructureError(TraitsBridgeError):
    """Raised when profiles structure does not match expected format."""


# -------------------------
# Public API
# -------------------------

def extract_raw_profiles(calc_result: CalcResultInternal) -> Dict[str, Dict[str, Any]]:
    """
    Extracts raw profile dictionaries from CalcResultInternal.

    This bridge:
    - Does NOT assume profile IDs
    - Does NOT modify calculator output
    - Does NOT access HUMAN_ARCHITECTURE_MARKERS
    - Only validates and returns profile dicts

    Returns:
        {
            "physical": {...},
            "emotional": {...},
            "intellectual": {...}
        }
    """

    if not isinstance(calc_result, CalcResultInternal):
        raise TraitsBridgeError("calc_result must be CalcResultInternal")

    profiles = calc_result.profiles

    if not isinstance(profiles.physical, dict):
        raise InvalidProfilesStructureError("physical profile must be dict")

    if not isinstance(profiles.emotional, dict):
        raise InvalidProfilesStructureError("emotional profile must be dict")

    if not isinstance(profiles.intellectual, dict):
        raise InvalidProfilesStructureError("intellectual profile must be dict")

    return {
        "physical": profiles.physical,
        "emotional": profiles.emotional,
        "intellectual": profiles.intellectual,
    }

