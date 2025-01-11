import pickle
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
with open("rules.pkl", "rb") as file:
    app_model = pickle.load(file)

VERSION = "1.0.0"
MODEL_DATE = datetime.datetime.now().strftime("%Y-%m-%d") # TODO mudar lógica versionamento

def recommend_tracks(user_tracks, model):
    recommendations = []
    for row in model:
        antecedent, consequent, confidence = row
        if set(antecedent).issubset(set(user_tracks)):
            recommendations.extend(consequent)
    return list(set(recommendations))

@app.route("/")
def hello_world():
    return "Hello, server running!"

@app.route("/api/recommend", methods=['POST'])
def recommend():
    data = request.get_json(force=True)
    print(data)
    user_tracks = data.get('songs', [])

    if not isinstance(user_tracks, list) or not all(isinstance(song, str) for song in user_tracks):
        return jsonify({"Error": "Invalid input. 'songs' should be a list of strings."}), 400
    
    recommended_songs = recommend_tracks(user_tracks=user_tracks, model=app_model)

    return jsonify({
        'songs': recommended_songs,
        'version': VERSION,
        'model_date': MODEL_DATE
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52033)