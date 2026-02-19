# engine/language/language_parameters.py
# Production-ready machine-first language layer.
#
# Contract:
# - Input: three profile_ids (physical, emotional, intellectual)
# - Uses ONLY trait fields (never real_profile_name)
# - Returns a normalized dataclass LanguageParameters
# - No human-readable labels, no psych names, no medical interpretation
# - No if-chaos: composable, data-driven rules

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Tuple


# -------------------------
# Errors (machine-safe)
# -------------------------

class LanguageLayerError(Exception):
    """Base error for language layer."""


class UnknownProfileIdError(LanguageLayerError):
    """Raised when profile_id is not present in the profile maps."""


class InvalidTraitsError(LanguageLayerError):
    """Raised when traits are missing or invalid."""


# -------------------------
# Normalized model
# -------------------------

@dataclass(frozen=True, slots=True)
class LanguageParameters:
    """
    Machine-first parameters (0..1 continuous where applicable).
    No labels. No psych naming. No medical meaning.
    """
    # Formatting / readability
    sentence_length: float                 # 0..1 (short -> long)
    clause_density: float                  # 0..1 (simple -> nested)
    vocabulary_complexity: float           # 0..1 (plain -> technical)
    redundancy: float                      # 0..1 (low repetition -> high repetition)
    step_granularity: float                # 0..1 (coarse steps -> micro-steps)

    # Behavioral scaffolding
    directive_force: float                 # 0..1 (soft -> firm)
    rationale_weight: float                # 0..1 (do -> explain why)
    caution_density: float                 # 0..1 (few safety notes -> more safety notes)
    autonomy_support: float                # 0..1 (command -> choice framing)

    # Voice / emotional surface (still machine-safe)
    warmth: float                          # 0..1 (neutral -> warm)
    reassurance: float                     # 0..1
    urgency: float                         # 0..1

    # Optional knobs (bools are still machine-safe)
    allow_analogy: bool
    allow_examples: bool
    allow_checklists: bool

    # Provenance (safe)
    source_profile_ids: Tuple[str, str, str] = field(default_factory=tuple)


# -------------------------
# Utilities
# -------------------------

def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return float(x)


def _as_float01(value: Any, *, key: str) -> float:
    """
    Accept int/float/str numeric, normalize to 0..1 if already within range,
    otherwise raise (we don't guess scales in machine-first layer).
    """
    if value is None:
        raise InvalidTraitsError(f"Missing trait '{key}'")
    try:
        x = float(value)
    except (TypeError, ValueError) as e:
        raise InvalidTraitsError(f"Trait '{key}' must be numeric") from e
    if not (0.0 <= x <= 1.0):
        raise InvalidTraitsError(f"Trait '{key}' must be in [0..1], got {x}")
    return x


def _as_bool(value: Any, *, key: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("true", "1", "yes"):
            return True
        if v in ("false", "0", "no"):
            return False
    raise InvalidTraitsError(f"Trait '{key}' must be bool-like")


def _get_profile_traits(
    profile_map: Mapping[str, Mapping[str, Any]],
    profile_id: str,
) -> Mapping[str, Any]:
    """
    profile_map entries can be:
      - { "traits": {...}, "real_profile_name": "...", ... }
      - or directly traits dict
    We ONLY use 'traits' or the dict itself if it looks like traits.
    """
    if not profile_id or not isinstance(profile_id, str):
        raise UnknownProfileIdError("profile_id must be a non-empty string")

    entry = profile_map.get(profile_id)
    if entry is None:
        raise UnknownProfileIdError(f"Unknown profile_id: {profile_id}")

    # Safe: ignore any human-readable names
    if "traits" in entry and isinstance(entry["traits"], Mapping):
        return entry["traits"]
    # If the entry itself is traits-like
    return entry


def _weighted_mix(parts: Tuple[Tuple[Mapping[str, Any], float], ...], key: str) -> float:
    """
    Mix numeric traits key across (traits, weight) parts.
    All trait values must be in [0..1]. We keep deterministic behavior.
    """
    total_w = sum(w for _, w in parts)
    if total_w <= 0:
        raise InvalidTraitsError("Internal: total weight must be > 0")

    acc = 0.0
    for traits, w in parts:
        acc += _as_float01(traits.get(key), key=key) * w
    return _clamp01(acc / total_w)


def _dominant_bool(parts: Tuple[Tuple[Mapping[str, Any], float], ...], key: str) -> bool:
    """
    Weighted boolean vote. True if weighted sum >= 0.5*total_w.
    """
    total_w = sum(w for _, w in parts)
    if total_w <= 0:
        raise InvalidTraitsError("Internal: total weight must be > 0")

    true_w = 0.0
    for traits, w in parts:
        if _as_bool(traits.get(key), key=key):
            true_w += w
    return true_w >= (0.5 * total_w)


# -------------------------
# Trait contract (machine-safe)
# -------------------------
#
# Your PH/EM/IN tables must provide ONLY these keys inside "traits",
# each numeric is already normalized to [0..1].
#
# Numeric traits:
# - sentence_length
# - clause_density
# - vocabulary_complexity
# - redundancy
# - step_granularity
# - directive_force
# - rationale_weight
# - caution_density
# - autonomy_support
# - warmth
# - reassurance
# - urgency
#
# Bool traits:
# - allow_analogy
# - allow_examples
# - allow_checklists
#
# Anything else is ignored.


_REQUIRED_NUMERIC_TRAITS = (
    "sentence_length",
    "clause_density",
    "vocabulary_complexity",
    "redundancy",
    "step_granularity",
    "directive_force",
    "rationale_weight",
    "caution_density",
    "autonomy_support",
    "warmth",
    "reassurance",
    "urgency",
)

_REQUIRED_BOOL_TRAITS = (
    "allow_analogy",
    "allow_examples",
    "allow_checklists",
)


def _validate_traits(traits: Mapping[str, Any]) -> None:
    for k in _REQUIRED_NUMERIC_TRAITS:
        _as_float01(traits.get(k), key=k)
    for k in _REQUIRED_BOOL_TRAITS:
        _as_bool(traits.get(k), key=k)


# -------------------------
# Public API
# -------------------------

def build_language_parameters(
    *,
    physical_profile_id: str,
    emotional_profile_id: str,
    intellectual_profile_id: str,
    physical_profile_map: Mapping[str, Mapping[str, Any]],
    emotional_profile_map: Mapping[str, Mapping[str, Any]],
    intellectual_profile_map: Mapping[str, Mapping[str, Any]],
    weights: Tuple[float, float, float] = (0.38, 0.32, 0.30),
) -> LanguageParameters:
    """
    Build normalized, machine-safe LanguageParameters from 3 profile_ids.

    - Uses ONLY traits.
    - Validates profile_ids and trait contracts.
    - Data-driven: weighted mixing of trait vectors, no branching logic.
    """
    w_ph, w_em, w_in = weights
    if any((not isinstance(w, (int, float)) or w < 0) for w in weights):
        raise InvalidTraitsError("weights must be non-negative numbers")
    if (w_ph + w_em + w_in) <= 0:
        raise InvalidTraitsError("weights sum must be > 0")

    ph_traits = _get_profile_traits(physical_profile_map, physical_profile_id)
    em_traits = _get_profile_traits(emotional_profile_map, emotional_profile_id)
    in_traits = _get_profile_traits(intellectual_profile_map, intellectual_profile_id)

    _validate_traits(ph_traits)
    _validate_traits(em_traits)
    _validate_traits(in_traits)

    parts = ((ph_traits, float(w_ph)), (em_traits, float(w_em)), (in_traits, float(w_in)))

    # Numeric vector mix
    params: Dict[str, Any] = {k: _weighted_mix(parts, k) for k in _REQUIRED_NUMERIC_TRAITS}

    # Bool votes
    params.update({k: _dominant_bool(parts, k) for k in _REQUIRED_BOOL_TRAITS})

    return LanguageParameters(
        sentence_length=params["sentence_length"],
        clause_density=params["clause_density"],
        vocabulary_complexity=params["vocabulary_complexity"],
        redundancy=params["redundancy"],
        step_granularity=params["step_granularity"],
        directive_force=params["directive_force"],
        rationale_weight=params["rationale_weight"],
        caution_density=params["caution_density"],
        autonomy_support=params["autonomy_support"],
        warmth=params["warmth"],
        reassurance=params["reassurance"],
        urgency=params["urgency"],
        allow_analogy=bool(params["allow_analogy"]),
        allow_examples=bool(params["allow_examples"]),
        allow_checklists=bool(params["allow_checklists"]),
        source_profile_ids=(physical_profile_id, emotional_profile_id, intellectual_profile_id),
    )

