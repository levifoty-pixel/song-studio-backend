from mido import MidiFile

# Standard guitar tuning in MIDI notes:
# E2, A2, D3, G3, B3, E4
STRING_TUNINGS = {
    6: 40,  # E2
    5: 45,  # A2
    4: 50,  # D3
    3: 55,  # G3
    2: 59,  # B3
    1: 64   # E4
}

def find_string_and_fret(note):
    """
    Given a MIDI note number, return (string, fret)
    or None if the note can't be played on standard guitar tuning.
    """
    for string, open_note in STRING_TUNINGS.items():
        fret = note - open_note
        if 0 <= fret <= 20:  # reasonable fret range
            return string, fret
    return None

def midi_to_tab(midi_path):
    mid = MidiFile(midi_path)

    # Collect note events with timing
    events = []
    current_time = 0

    for msg in mid:
        current_time += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            events.append({
                "note": msg.note,
                "time": current_time
            })

    # Quantize timing into columns
    # (e.g., every 0.25 seconds = one column)
    QUANTIZE = 0.25
    columns = {}

    for event in events:
        col = int(event["time"] / QUANTIZE)
        if col not in columns:
            columns[col] = []
        columns[col].append(event["note"])

    # Build tab grid
    max_col = max(columns.keys()) if columns else 0
    tab = {s: ["-"] * (max_col + 1) for s in range(1, 7)}

    for col, notes in columns.items():
        for note in notes:
            sf = find_string_and_fret(note)
            if sf:
                string, fret = sf
                tab[string][col] = str(fret)

    # Convert lists into strings
    final_tab = {}
    for string in range(1, 7):
        final_tab[string] = "".join(
            f.ljust(2, "-") if len(f) == 1 else f
            for f in tab[string]
        )

    return final_tab
