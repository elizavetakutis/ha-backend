# Minimal signature change: old logic not broken internally; caller supplies new args.

from __future__ import annotations
from typing import Any, Dict, Optional

from engine.language import LanguageParameters


def assemble_protocol(
    raw_text: str,
    language_params: LanguageParameters,
    tone_params: Dict[str, Any],
) -> str:
    """
    Builds patient-facing protocol text using ONLY provided parameters.
    No medical interpretation is added.
    No diagnostic structures are exposed.
    """

    raw_text = (raw_text or "").strip()
    if not raw_text:
        return ""

    # NOTE:
    # Here you will apply only formatting/rewriting rules.
    # This file intentionally contains NO medical logic.

    # Placeholder: keep existing behavior until rewrite rules are plugged in.
    # You will integrate language_params to pick:
    # - sentence split strategy
    # - checklist vs prose
    # - redundancy for reinforcement
    # - directive force for verbs, etc.
    #
    # For now, return raw_text to keep old behavior stable.
    return raw_text
