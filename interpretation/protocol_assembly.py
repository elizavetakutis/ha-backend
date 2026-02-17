def assemble_protocol(raw_text: str, comm_state: dict) -> str:
    """
    Builds patient-facing protocol text using ONLY encoded communication state.
    No medical interpretation is added.
    No diagnostic structures are exposed.
    """

    raw_text = (raw_text or "").strip()

    # Encoded parameters
    c1 = comm_state.get("c1")  # magnetism level (L / N)
    c2 = comm_state.get("c2", 0)  # cognitive processing (encoded number)
    c3 = comm_state.get("c3", 0)  # structural stability
    c4 = comm_state.get("c4", 0)  # motivational difference

    # -------------------------
    # Tone only (no advice)
    # -------------------------

    if c1 == "L":
        intro = "Please follow the plan below as discussed with your doctor.\n\n"
    else:
        intro = ""

    structured_text = (
        "Patient Plan Summary\n\n"
        + intro
        + raw_text
    )

    return structured_text


