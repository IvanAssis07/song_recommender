import pickle
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, server running!"

@app.route("/api/recommend", methods=['POST'])
def recommend():
    data = request.get_json(force=True)
    user_tracks = data.get('songs', [])
    version = os.getenv("APP_VERSION", "1.0.0")

    if not isinstance(user_tracks, list) or not all(isinstance(song, str) for song in user_tracks):
        return jsonify({"Error": "Invalid input. 'songs' should be a list of strings."}), 400

    with open("shared/rules.pkl", "rb") as file:
        metadata = pickle.load(file)

    app_model = metadata["rules"]
    model_date = metadata["updated_at"]
    
    recommendations = []
    for row in app_model:
        antecedent, consequent, confidence = row
        if set(antecedent).issubset(set(user_tracks)):
            recommendations.extend(consequent)

    recommendations = list(set(recommendations))

    if not recommendations:
        recommendations = ["Hey Mama", "No Faith in Brooklyn (feat. Jhameel)", "Not Today", "Love You Goodbye", "Bonfire"]

    return jsonify({
        'songs': recommendations,
        'version': version,
        'model_date': model_date
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52033)