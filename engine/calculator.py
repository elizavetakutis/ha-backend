def run_calculation(input_data):
    """
    Core HA engine logic.
    This is where IF/THEN rules live.
    """

    result = {}

    protocol = input_data.protocol_content.lower()

    # Example rule set
    if "inflammation" in protocol:
        result["clinical_vector"] = "inflammatory-dominant"

    elif "thyroid" in protocol:
        result["clinical_vector"] = "endocrine-dominant"

    else:
        result["clinical_vector"] = "metabolic-general"

    # Example recommendation logic
    recommendations = []

    if "magnesium" not in protocol:
        recommendations.append("Consider magnesium support")

    if "vitamin d" not in protocol:
        recommendations.append("Review vitamin D levels")

    result["recommendations"] = recommendations

    result["summary"] = "Rule-based mock analysis completed."

    return result

