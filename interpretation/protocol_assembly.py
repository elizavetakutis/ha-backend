def assemble_protocol(raw_text: str, comm_state: dict) -> str:
    """
    Builds patient-facing protocol text using ONLY encoded communication state.
    No diagnostic structures are exposed.
    """

    c1 = comm_state.get("c1")  # magnetism encoded
    c2 = comm_state.get("c2", 0)  # cognitive processing
    c3 = comm_state.get("c3", 0)  # structural stability
    c4 = comm_state.get("c4", 0)  # motivational difference

    # -------------------------
    # Tone Logic (Encoded)
    # -------------------------

    if c1 == "L":
        intro = "Please consider the following guidance:\n\n"
    else:
        intro = ""

    # Cognitive detail adjustment
    if c2 >= 60:
        detail_line = "\n\nConsistency and timing may influence effectiveness."
    else:
        detail_line = ""

    # Structural confidence adjustment
    if c3 < 30:
        support_line = "\n\nMaintain routine to support stability."
    else:
        support_line = ""

    # Motivational emphasis
    if c4 > 100:
        motivation_line = "\n\nConsistency will be especially important for best results."
    else:
        motivation_line = ""

    structured_text = (
        "Patient Plan Summary\n\n"
        + intro
        + raw_text.strip()
        + detail_line
        + support_line
        + motivation_line
    )

    return structured_text

