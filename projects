
from flask import Flask, render_template, request

app = Flask(__name__)

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

@app.route("/", methods=["GET", "POST"])
def index():
    chord = None
    notes = None
    error = None
    modes = []
    notes_list = []

    if request.method == "POST":
        chord = request.form.get("chord")
        if chord:
            # Placeholder logic for chord notes
            notes = ["C", "E", "G"]
            notes_list = notes.copy()
            modes = [("Ionian", ["C","D","E","F","G","A","B"], ["Dm","Em","F"])]
        else:
            error = "Please enter a chord!"

    return render_template("index.html", chord=chord, notes=notes, modes=modes, NOTES=NOTES, error=error, notes_list=notes_list)

if __name__ == "__main__":
    app.run(debug=True)
