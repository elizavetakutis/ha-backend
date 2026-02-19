from datetime import datetime
from .markers import YEAR_MARKERS, MONTH_MARKERS, HUMAN_ARCHITECTURE_MARKERS

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

    # Получаем данные профилей
    physical_data = HUMAN_ARCHITECTURE_MARKERS[str(X)]["physical"]
    emotional_data = HUMAN_ARCHITECTURE_MARKERS[str(Z)]["emotional"]
    intellectual_data = HUMAN_ARCHITECTURE_MARKERS[str(K)]["intellectual"]

    # Получаем profile_id
    physical_profile_id = physical_data.get("profile_id")
    emotional_profile_id = emotional_data.get("profile_id")
    intellectual_profile_id = intellectual_data.get("profile_id")

    # Системные проценты
    systems = {
        "structural": pct(physical_data["systems"]["Structural Stability"]),
        "adaptive": pct(physical_data["systems"]["Reproductive & Adaptive"]),
        "metabolic": pct(emotional_data["systems"]["Metabolic Drive & Will"]),
        "emotional": pct(emotional_data["systems"]["Emotional Integration"]),
        "expression": pct(intellectual_data["systems"]["Expression & Implementation"]),
        "cognitive": pct(intellectual_data["systems"]["Cognitive Processing"]),
    }

    # -------------------------
    # TENSION & MAGNETISM
    # -------------------------

    yin = systems["structural"] + systems["expression"] + systems["cognitive"]
    yang = systems["adaptive"] + systems["metabolic"] + systems["emotional"]

    want = abs(yang - yin)
    can = systems["structural"]

    magnetism = want * can
    tension_ratio = round(want / can, 2) if can != 0 else None

    # -------------------------
    # FINAL RESULT
    # -------------------------

    return {
        "markers": {
            "physical": X,
            "emotional": Z,
            "intellectual": K
        },
        "profiles": {
            "physical": physical_profile_id,
            "emotional": emotional_profile_id,
            "intellectual": intellectual_profile_id
        },
        "systems": systems,
        "tension": {
            "want": want,
            "can": can,
            "magnetism": magnetism,
            "tension_ratio": tension_ratio
        }
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
        "c1": magnetism_level,
        "c2": systems.get("cognitive", 0),
        "c3": systems.get("structural", 0),
        "c4": want_diff
    }

