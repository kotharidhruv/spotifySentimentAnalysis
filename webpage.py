from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from sentimentAnalysis import getEmotion, map_sentiment_to_genre
from textblob import TextBlob
from flask import Flask, render_template, request

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = result.json()
    token = json_result.get("access_token")
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_recommendations_by_genre(token, genre, limit=5):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)
    params = {
        "seed_genres": genre.lower(),  # Spotify genres are typically lowercase
        "limit": limit
    }

    response = get(url, headers=headers, params=params)
    print(f"API Response for genre '{genre}': {response.json()}")  # Debug statement
    if response.status_code == 200:
        json_response = response.json()
        tracks = json_response.get("tracks", [])
        return [{"name": track["name"], "artist": track["artists"][0]["name"], "uri": track["uri"]} for track in tracks]
    else:
        return []

token = get_token()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    text = request.form['text']
    sentiment = TextBlob(text).sentiment.polarity
    sentiment_category = getEmotion(sentiment)
    music_genre = map_sentiment_to_genre(sentiment_category)
    print(f"Sentiment: {sentiment_category}, Genre: {music_genre}")  # Debug statement
    recommendations = get_recommendations_by_genre(token, music_genre)
    return render_template('recommendations.html', sentiment=sentiment_category, genre=music_genre, recommendations=recommendations)

if __name__ == '__main__':
    app.run()