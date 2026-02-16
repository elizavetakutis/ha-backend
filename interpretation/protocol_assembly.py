def assemble_protocol(raw_text: str, calculation_data: dict) -> str:

    systems = calculation_data.get("systems", {})
    prakruti_data = calculation_data.get("prakruti", {})
    yin_yang = calculation_data.get("yin_yang", {})
    tension = calculation_data.get("tension", {})

    structured_text = f"""
Patient Plan Summary

Metabolic Type: {prakruti_data.get("type", "N/A")}
Energy Direction: {yin_yang.get("direction", "N/A")}
Magnetism Score: {tension.get("magnetism", "N/A")}

System Overview:
- Structural Stability: {systems.get("structural", 0)}%
- Adaptive Capacity: {systems.get("adaptive", 0)}%
- Metabolic Drive: {systems.get("metabolic", 0)}%
- Emotional Integration: {systems.get("emotional", 0)}%
- Expression: {systems.get("expression", 0)}%
- Cognitive Processing: {systems.get("cognitive", 0)}%

-----------------------------------
Doctor Prescribed Plan:
-----------------------------------

{raw_text}

-----------------------------------
This plan was structured for clarity and patient understanding.
"""

    return structured_text.strip()

