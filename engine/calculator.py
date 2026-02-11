from datetime import datetime
from .markers import YEAR_MARKERS, MONTH_MARKERS, HUMAN_ARCHITECTURE_MARKERS

A1 = 23
B1 = 28
C1 = 33


# -------------------------
# HELPERS
# -------------------------

def is_leap_year(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)


def days_in_month(year: int, month: int) -> int:
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return MONTH_MARKERS[month]["days"]


def reduce_value(value: int, max_value: int) -> int:
    while value > max_value:
        value -= max_value
    if value == 0:
        value = max_value
    return value


def pct(v):
    return int(str(v).replace("%", ""))


# -------------------------
# CORE CALCULATION
# -------------------------

def run_calculation(input_data):

    birth_date = datetime.strptime(input_data.patient_dob, "%Y-%m-%d")
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day

    if year not in YEAR_MARKERS:
        return {"error": "Year not supported"}

    dim = days_in_month(year, month)

    if day < 1 or day > dim:
        return {"error": "Invalid day"}

    # YEAR markers
    A2 = YEAR_MARKERS[year]["A2"]
    B2 = YEAR_MARKERS[year]["B2"]
    C2 = YEAR_MARKERS[year]["C2"]

    # MONTH markers
    if month == 2:
        month_key = 2 if is_leap_year(year) else "2.1"
    else:
        month_key = month

    A3 = MONTH_MARKERS[month_key]["A3"]
    B3 = MONTH_MARKERS[month_key]["B3"]
    C3 = MONTH_MARKERS[month_key]["C3"]

    # DAY rule
    A4 = dim - day
    B4 = A4
    C4 = A4

    # FINAL markers
    X = reduce_value(A2 + A3 + A4, A1)
    Z = reduce_value(B2 + B3 + B4, B1)
    K = reduce_value(C2 + C3 + C4, C1)

    physical     = HUMAN_ARCHITECTURE_MARKERS[str(X)]["physical"]
    emotional    = HUMAN_ARCHITECTURE_MARKERS[str(Z)]["emotional"]
    intellectual = HUMAN_ARCHITECTURE_MARKERS[str(K)]["intellectual"]

    systems = {
        "structural": physical["systems"]["Structural Stability"],
        "adaptive": physical["systems"]["Reproductive & Adaptive"],
        "metabolic": emotional["systems"]["Metabolic Drive & Will"],
        "emotional": emotional["systems"]["Emotional Integration"],
        "expression": intellectual["systems"]["Expression & Implementation"],
        "cognitive": intellectual["systems"]["Cognitive Processing"],
    }

    # --- PRAKRUTI ---
    kapha_raw = pct(systems["structural"]) + pct(systems["adaptive"])
    pitta_raw = pct(systems["metabolic"]) + pct(systems["emotional"])
    vata_raw  = pct(systems["expression"]) + pct(systems["cognitive"])

    total = kapha_raw + pitta_raw + vata_raw

    kapha = round(kapha_raw / total * 100)
    pitta = round(pitta_raw / total * 100)
    vata  = round(vata_raw  / total * 100)

    # --- YIN / YANG ---
    yin = pct(systems["structural"]) + pct(systems["expression"]) + pct(systems["cognitive"])
    yang = pct(systems["adaptive"]) + pct(systems["metabolic"]) + pct(systems["emotional"])

    direction = "Balanced"
    if yang > yin:
        direction = "Yang dominant"
    elif yin > yang:
        direction = "Yin dominant"

    want = abs(yang - yin)
    can = pct(systems["structural"])
    magnetism = want * can

    return {
        "markers": {
            "physical": X,
            "emotional": Z,
            "intellectual": K
        },
        "profiles": {
            "physical": physical["profile"],
            "emotional": emotional["profile"],
            "intellectual": intellectual["profile"]
        },
        "systems": systems,
        "prakruti": {
            "kapha": kapha,
            "pitta": pitta,
            "vata": vata
        },
        "yin_yang": {
            "yin": yin,
            "yang": yang,
            "direction": direction,
            "balance_index": round(yang / yin, 2) if yin else None
        },
        "tension": {
            "want": want,
            "can": can,
            "magnetism": magnetism,
            "tension_ratio": round(want / can, 2) if can else None
        }
    }
