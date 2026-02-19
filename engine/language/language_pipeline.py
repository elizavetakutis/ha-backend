from engine.contracts import CalcResultInternal
from engine.language.traits_bridge import resolve_traits
from engine.language.machine_protocol_assembly import assemble_protocol


def run_language_pipeline(calc_result: dict, raw_text: str) -> str:
    """
    Safe wrapper around new language layer.
    If anything fails — returns original raw_text.
    """

    try:
        model = CalcResultInternal(**calc_result)

        traits = resolve_traits(model)

        return assemble_protocol(
            raw_text=raw_text,
            language_params=traits,
            tone_params={},
        )

    except Exception:
        # Hard safety fallback
        return raw_text
