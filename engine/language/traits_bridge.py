# engine/language/traits_bridge.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from engine.contracts import CalcResultInternal
from engine.profile_maps import (
    PHYSICAL_NAME_TO_ID,
    EMOTIONAL_NAME_TO_ID,
    INTELLECTUAL_NAME_TO_ID,
    PHYSICAL_PROFILE_MAP,
    EMOTIONAL_PROFILE_MAP,
    INTELLECTUAL_PROFILE_MAP,
)


# -------------------------
# Errors
# -------------------------

class TraitsBridgeError(Exception):
    pass


class ProfileNameNotMappedError(TraitsBridgeError):
    pass


class ProfileIdNotFoundError(TraitsBridgeError):
    pass


# -------------------------
# Data container
# -------------------------

@dataclass(frozen=True)
class ResolvedTraits:
    physical_id: str
    emotional_id: str
    intellectual_id: str
    physical_traits: Dict[str, Any]
    emotional_traits: Dict[str, Any]
    intellectual_traits: Dict[str, Any]


# -------------------------
# Core function
# -------------------------

def resolve_traits(calc_result: CalcResultInternal) -> ResolvedTraits:
    """
    Converts HUMAN_ARCHITECTURE profile names
    into profile IDs (PHxx / EMxx / INxx),
    then loads trait maps.

    Deterministic mapping only.
    No medical logic.
    No inference.
    """

    raw_profiles = calc_result.profiles

    # IMPORTANT:
    # calculator currently returns full profile dicts,
    # not just IDs. So we extract profile name from dict.

    physical_name = raw_profiles.physical.get("profile")
    emotional_name = raw_profiles.emotional.get("profile")
    intellectual_name = raw_profiles.intellectual.get("profile")

    if not physical_name or not emotional_name or not intellectual_name:
        raise TraitsBridgeError("Missing profile name in calculation result")

    # --- NAME → ID ---

    try:
        physical_id = PHYSICAL_NAME_TO_ID[physical_name]
    except KeyError:
        raise ProfileNameNotMappedError(
            f"Unmapped physical profile: {physical_name}"
        )

    try:
        emotional_id = EMOTIONAL_NAME_TO_ID[emotional_name]
    except KeyError:
        raise ProfileNameNotMappedError(
            f"Unmapped emotional profile: {emotional_name}"
        )

    try:
        intellectual_id = INTELLECTUAL_NAME_TO_ID[intellectual_name]
    except KeyError:
        raise ProfileNameNotMappedError(
            f"Unmapped intellectual profile: {intellectual_name}"
        )

    # --- ID → TRAITS ---

    try:
        physical_traits = PHYSICAL_PROFILE_MAP[physical_id]
    except KeyError:
        raise ProfileIdNotFoundError(
            f"Physical ID not found: {physical_id}"
        )

    try:
        emotional_traits = EMOTIONAL_PROFILE_MAP[emotional_id]
    except KeyError:
        raise ProfileIdNotFoundError(
            f"Emotional ID not found: {emotional_id}"
        )

    try:
        intellectual_traits = INTELLECTUAL_PROFILE_MAP[intellectual_id]
    except KeyError:
        raise ProfileIdNotFoundError(
            f"Intellectual ID not found: {intellectual_id}"
        )

    return ResolvedTraits(
        physical_id=physical_id,
        emotional_id=emotional_id,
        intellectual_id=intellectual_id,
        physical_traits=physical_traits,
        emotional_traits=emotional_traits,
        intellectual_traits=intellectual_traits,
    )

