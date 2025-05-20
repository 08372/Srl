from flask import Flask, jsonify, send_file, make_response
import random
from datetime import datetime
from fpdf import FPDF
import io

app = Flask(__name__)

todays_matches = [
    ("Man City", "Arsenal"),
    ("Chelsea", "Everton")
]

teams_data = {
    "Man City": {"attaque": 2.1, "defense": 0.8},
    "Arsenal": {"attaque": 1.8, "defense": 1.0},
    "Chelsea": {"attaque": 1.4, "defense": 1.3},
    "Everton": {"attaque": 1.1, "defense": 1.5}
}

match_results = []

def poisson(lmbda):
    L = pow(2.71828, -lmbda)
    k = 0
    p = 1
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def simulate_match(team1, team2):
    lambda1 = (teams_data[team1]['attaque'] + teams_data[team2]['defense']) / 2
    lambda2 = (teams_data[team2]['attaque'] + teams_data[team1]['defense']) / 2
    g1 = poisson(lambda1)
    g2 = poisson(lambda2)

    events = []
    for minute in range(1, 91):
        if random.random() < 0.03:
            team = random.choice([team1, team2])
            events.append({"minute": minute, "team": team, "text": f"{team} tente une action dangereuse."})
        if minute in random.sample(range(1, 91), g1 + g2):
            if g1 > 0:
                events.append({"minute": minute, "team": team1, "text": f"BUT pour {team1}!"})
                g1 -= 1
            elif g2 > 0:
                events.append({"minute": minute, "team": team2, "text": f"BUT pour {team2}!"})
                g2 -= 1

    return {
        "teams": f"{team1} vs {team2}",
        "score": f"{team1} {g1} - {g2} {team2}",
        "events": events
    }

@app.route("/api/srl/today")
def api_srl_today():
    global match_results
    match_results = []
    for match in todays_matches:
        sim = simulate_match(match[0], match[1])
        match_results.append(sim)
    return jsonify(match_results)

@app.route("/api/srl/pdf/<int:match_id>")
def get_match_pdf(match_id):
    if match_id >= len(match_results):
        return make_response("Match non trouvé", 404)

    match = match_results[match_id]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=match["teams"], ln=True, align='C')
    pdf.cell(200, 10, txt="Score final : " + match["score"], ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Résumé minute par minute :", ln=True)
    for event in match['events']:
        pdf.cell(200, 10, txt=f"{event['minute']}' - {event['text']}", ln=True)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name=f"fiche_match_{match_id}.pdf")

@app.route("/")
def home():
    return "SRL Auto Simulator - Accédez à /api/srl/today"

if __name__ == "__main__":
    app.run()
