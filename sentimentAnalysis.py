from textblob import TextBlob

text = input("Enter text for analysis: ")
print(text)

blob = TextBlob(text)
sentiment = blob.sentiment.polarity

def getEmotion(polarity):
    polarity = float(polarity)
    if polarity <= -0.6:
        return "Very Negative"
    elif polarity <= -0.2:
        return "Negative"
    elif polarity < 0.2:
        return "Neutral"
    elif polarity < 0.6:
        return "Positive"
    else:
        return "Very Positive"

print(getEmotion(sentiment))

def map_sentiment_to_genre(sentiment):
    genre_mapping = {
        "Very Negative": "metal",
        "Negative": "sad",
        "Neutral": "chill",
        "Positive": "pop",
        "Very Positive": "edm"
    }
    return genre_mapping.get(sentiment)

sentiment_category = getEmotion(sentiment)
music_genre = map_sentiment_to_genre(sentiment_category)

print(f"The sentiment of the text is: {sentiment_category}")
print(f"Suggested music genres: {music_genre}")