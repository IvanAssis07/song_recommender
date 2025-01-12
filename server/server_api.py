import pickle
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, server running!"

@app.route("/api/recommend", methods=['POST'])
def recommend():
    VERSION = "1.0.0"
    MODEL_DATE = datetime.datetime.now().strftime("%Y-%m-%d") # TODO mudar lógica versionamento

    with open("../model/rules.pkl", "rb") as file:
        app_model = pickle.load(file)

    data = request.get_json(force=True)
    user_tracks = data.get('songs', [])

    if not isinstance(user_tracks, list) or not all(isinstance(song, str) for song in user_tracks):
        return jsonify({"Error": "Invalid input. 'songs' should be a list of strings."}), 400
    
    recommendations = []
    for row in app_model:
        antecedent, consequent, confidence = row
        if set(antecedent).issubset(set(user_tracks)):
            recommendations.extend(consequent)

    recommendations = list(set(recommendations))

    return jsonify({
        'songs': recommendations,
        'version': VERSION,
        'model_date': MODEL_DATE
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52033)