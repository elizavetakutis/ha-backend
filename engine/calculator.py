from datetime import datetime
from .markers import YEAR_MARKERS, MONTH_MARKERS, HUMAN_ARCHITECTURE_MARKERS

# NEW: interpretation layer (безопасный импорт)
try:
    from interpretation.protocol_assembly import assemble_protocol
except:
    assemble_protocol = None

# -------------------------
# CONSTANTS
# -------------------------

A1 = 23  # Physical cycle
B1 = 28  # Emotional cycle
C1 = 33  # Intellectual cycle


# -------------------------
# HELPERS
# -------------------------

def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month(year: int, month: int) -> int:
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return [31,28,31,30,31,30,31,31,30,31,30,31][month-1]


def reduce_value(value: int, max_value: int) -> int:
    while value > max_value:
        value -= max_value
    if value == 0:
        value = max_value
    return value


def pct(value: str) -> int:
    return int(str(value).replace("%", ""))


# -------------------------
# CORE CALCULATION
# -------------------------

def run_calculation(input_data):

    dob = input_data.patient_dob

    try:
        parsed = datetime.fromisoformat(dob)
    except:
        return {"error": "Invalid date format"}

    year = parsed.year
    month = parsed.month
    day = parsed.day

    if year not in YEAR_MARKERS:
        return {"error": "Year not supported"}

    dim = days_in_month(year, month)

    if day < 1 or day > dim:
        return {"error": "Invalid day"}

    A2 = YEAR_MARKERS[year]["A2"]
    B2 = YEAR_MARKERS[year]["B2"]
    C2 = YEAR_MARKERS[year]["C2"]

    leap = is_leap_year(year)
    month_key = month if month != 2 else (2 if leap else "2.1")

    if month_key not in MONTH_MARKERS:
        return {"error": "Missing month markers"}

    A3 = MONTH_MARKERS[month_key]["A3"]
    B3 = MONTH_MARKERS[month_key]["B3"]
    C3 = MONTH_MARKERS[month_key]["C3"]

    A4 = dim - day
    B4 = A4
    C4 = A4

    X = reduce_value(A2 + A3 + A4, A1)
    Z = reduce_value(B2 + B3 + B4, B1)
    K = reduce_value(C2 + C3 + C4, C1)

physical_data = HUMAN_ARCHITECTURE_MARKERS[str(X)]["physical"]
emotional_data = HUMAN_ARCHITECTURE_MARKERS[str(Z)]["emotional"]
intellectual_data = HUMAN_ARCHITECTURE_MARKERS[str(K)]["intellectual"]

physical_profile_id = physical_data.get("profile_id")
emotional_profile_id = emotional_data.get("profile_id")
intellectual_profile_id = intellectual_data.get("profile_id")


    systems = {
        "structural": pct(physical["systems"]["Structural Stability"]),
        "adaptive": pct(physical["systems"]["Reproductive & Adaptive"]),
        "metabolic": pct(emotional["systems"]["Metabolic Drive & Will"]),
        "emotional": pct(emotional["systems"]["Emotional Integration"]),
        "expression": pct(intellectual["systems"]["Expression & Implementation"]),
        "cognitive": pct(intellectual["systems"]["Cognitive Processing"]),
    }

    # -------------------------
    # PRAKRUTI
    # -------------------------

    kapha_raw = systems["structural"] + systems["adaptive"]
    pitta_raw = systems["metabolic"] + systems["emotional"]
    vata_raw = systems["expression"] + systems["cognitive"]

    total = kapha_raw + pitta_raw + vata_raw

    kapha = round(kapha_raw / total * 100)
    pitta = round(pitta_raw / total * 100)
    vata = round(vata_raw / total * 100)

    dominant = max(kapha, pitta, vata)

    if dominant == pitta:
        prakruti = "Pitta dominant"
    elif dominant == kapha:
        prakruti = "Kapha dominant"
    else:
        prakruti = "Vata dominant"

    # -------------------------
    # YIN / YANG
    # -------------------------

    yin = systems["structural"] + systems["expression"] + systems["cognitive"]
    yang = systems["adaptive"] + systems["metabolic"] + systems["emotional"]

    if yang > yin:
        direction = "Yang dominant"
    elif yin > yang:
        direction = "Yin dominant"
    else:
        direction = "Balanced"

    balance_index = round(yang / yin, 2) if yin != 0 else None

    # -------------------------
    # TENSION & MAGNETISM
    # -------------------------

    want = abs(yang - yin)
    can = systems["structural"]

    magnetism = want * can
    tension_ratio = round(want / can, 2) if can != 0 else None

    # -------------------------
    # NEW: PROTOCOL ASSEMBLY
    # -------------------------

    output_text = None

    if hasattr(input_data, "raw_protocol_text") and input_data.raw_protocol_text:
        if assemble_protocol:
            output_text = assemble_protocol(
                raw_text=input_data.raw_protocol_text,
                calculation_data={
                    "systems": systems,
                    "prakruti": prakruti,
                    "yin_yang_direction": direction,
                    "magnetism": magnetism
                }
            )
        else:
            # если interpretation layer ещё не создан
            output_text = input_data.raw_protocol_text

    # -------------------------
    # FINAL RESULT
    # -------------------------

    return {
        "markers": {
            "physical": X,
            "emotional": Z,
            "intellectual": K
        },
    "profiles": { "physical": physical.get("profile_id"), "emotional": emotional.get("profile_id"), "intellectual": intellectual.get("profile_id") },
        "systems": systems,
        "prakruti": {
            "kapha": kapha,
            "pitta": pitta,
            "vata": vata,
            "type": prakruti
        },
        "yin_yang": {
            "yin": yin,
            "yang": yang,
            "direction": direction,
            "balance_index": balance_index
        },
        "tension": {
            "want": want,
            "can": can,
            "magnetism": magnetism,
            "tension_ratio": tension_ratio
        },
        "output": output_text   # ← НОВОЕ ПОЛЕ
    }
# -------------------------
# COMMUNICATION EXTRACTION (PRIVATE)
# -------------------------

def extract_comm_state(calc_result: dict) -> dict:
    """
    Extracts ONLY 4 communication metrics from full calculation.
    This layer is private and must never be exposed directly.
    """

    systems = calc_result.get("systems", {})
    tension = calc_result.get("tension", {})

    magnetism_raw = tension.get("magnetism", 0)
    want_diff = tension.get("want", 0)

    magnetism_level = "L" if magnetism_raw < 1000 else "N"

    return {
        "c1": magnetism_level,                     # magnetism level
        "c2": systems.get("cognitive", 0),         # cognitive processing
        "c3": systems.get("structural", 0),        # structural stability
        "c4": want_diff                            # motivational tension
    }
