from flask import Flask, render_template, request
app = Flask(__name__)

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJOR_SCALE_STEPS = [2, 2, 1, 2, 2, 2, 1]
MODES = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"]

# --- Music Logic Functions ---
def build_scale(root):
    idx = NOTES.index(root)
    scale = [root]
    for step in MAJOR_SCALE_STEPS[:-1]:
        idx = (idx + step) % 12
        scale.append(NOTES[idx])
    return scale

def all_modes(root):
    major_scale = build_scale(root)
    modes = {}
    for i, mode_name in enumerate(MODES):
        mode = major_scale[i:] + major_scale[:i]
        modes[f"{major_scale[i]} {mode_name}"] = mode
    return modes

def chord_notes(chord):
    chord = chord.strip()
    if not chord:
        raise ValueError("Empty chord input")
    root = chord[0].upper()
    accidental = ""
    chord_type = "major"
    idx = 1
    if len(chord) > 1 and chord[1] in ['#', 'b']:
        accidental = chord[1]
        idx = 2
    if len(chord) > idx:
        if chord[idx] == "m":
            chord_type = "minor"
        elif chord[idx] == "M":
            chord_type = "major"
        else:
            raise ValueError("Invalid chord format. Use M for major, m for minor.")
    root_note = root + accidental
    if root_note not in NOTES:
        raise ValueError(f"Invalid root note: {root_note}")
    intervals = [0, 4, 7] if chord_type == "major" else [0, 3, 7]
    root_idx = NOTES.index(root_note)
    return [NOTES[(root_idx + i) % 12] for i in intervals]

def chord_name_from_notes(root, notes):
    intervals = [(NOTES.index(notes[i]) - NOTES.index(root)) % 12 for i in range(len(notes))]
    if intervals == [0, 4, 7]:
        return f"{root}M"
    elif intervals == [0, 3, 7]:
        return f"{root}m"
    return f"{root}m7b5"

def triads_in_mode(mode_notes, input_chord_notes):
    triads = []
    for i in range(7):
        root = mode_notes[i]
        triad = [mode_notes[i], mode_notes[(i+2)%7], mode_notes[(i+4)%7]]
        if set(triad) != set(input_chord_notes):
            triads.append(chord_name_from_notes(root, triad))
    return triads

def find_modes(chord_tones):
    results = []
    for note in NOTES:
        modes_dict = all_modes(note)
        for mode_name, mode_notes in modes_dict.items():
            if all(n in mode_notes for n in chord_tones):
                other_triads = triads_in_mode(mode_notes, chord_tones)
                results.append((mode_name, mode_notes, other_triads))
    return results

# --- Routes ---
@app.route("/", methods=["GET","POST"])
def index():
    chord = ""
    notes = []
    notes_list = []
    modes = []
    error = None
    if request.method=="POST":
        chord = request.form.get("chord","").strip()
        try:
            notes_list = chord_notes(chord)
            notes = ", ".join(notes_list)
            modes = find_modes(notes_list)
        except Exception as e:
            error = f"Wrong input! {str(e)}"
            chord = ""
    return render_template("index.html", chord=chord, notes=notes, notes_list=notes_list, modes=modes, error=error, NOTES=NOTES)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
