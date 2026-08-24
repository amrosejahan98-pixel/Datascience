import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def search_tweets(keyword, limit=20):
    response = client.search_recent_tweets(
        query=keyword,
        max_results=min(limit, 100),
        tweet_fields=["created_at", "author_id"]
    )

    if response.data is None:
        return []

    return [
        {
            "tweet": tweet.text,
            "created_at": tweet.created_at,
            "author_id": tweet.author_id
        }
        for tweet in response.data
    ]