import tweepy
import json
from gemini import execute_gemini


API_KEY = "GDwN9X3kFYoa1yABO823hBLc2"
API_SECRET_KEY = "H6U3knYSjRvO7jjgSuMX5GXAxc1sZVVi0LrSOvyWWqS7O5hyiw"
ACCESS_TOKEN = "944088005056200705-o5ZtBI9NImDWCnZzqBO8h1SOOwH02Zo"
ACCESS_TOKEN_SECRET = "OUVXQJvcJH2QOPQ2PrqvcWEj8zkRhmjaGh8pJukyw5QpI"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMaM3gEAAAAAomwOn6K0CNjhxYyG6F35by2xRa0%3D78SOwEvWVonokxRdxG7dGohYU7aldP0zsKbCxYGsUybM8SUOnc"

if __name__ == "__main__":
    # Initialize client
    twitter_client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True,
    )

    # Get user info
    user = twitter_client.get_user(username="sundarpichai")
    user_id = user.data.id

    # Get last 5 tweets with metrics and timestamp
    tweets = twitter_client.get_users_tweets(
        id=user_id,
        max_results=50,
        tweet_fields=["created_at", "public_metrics", "text"]
    )

    # Convert tweets to serializable dicts
    tweet_list = []
    if tweets.data:
        for t in tweets.data:
            tweet_list.append({
                "id": t.id,
                "text": t.text,
                "created_at": str(t.created_at),
                "public_metrics": t.public_metrics
            })

    # Save to JSON file
    with open("extracted_tweets.json", "w", encoding="utf-8") as json_file:
        json.dump(tweet_list, json_file, indent=4, ensure_ascii=False)

    print("Tweets saved to extracted_tweets.json")