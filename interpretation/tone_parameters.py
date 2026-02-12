if magnetism.level == "low":
    return ToneParameters(
        authority_distance="low",
        directive_intensity="low",
        validation_level="high",
        emotional_softening="high",
        phrasing_style="collaborative"
    )
else:
    return ToneParameters(
        authority_distance="neutral",
        directive_intensity="normal",
        validation_level="normal",
        emotional_softening="low",
        phrasing_style="direct"
    )
