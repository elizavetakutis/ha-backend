def assemble_protocol(raw_text: str, calculation_data: dict) -> str:

    # Пока MVP — просто возвращаем красиво обернутый текст
    # Без упоминания HA, без названия калькулятора

    structured_text = f"""
Patient Plan Summary

{raw_text}

This plan was structured for clarity and patient understanding.
"""

    return structured_text.strip()

