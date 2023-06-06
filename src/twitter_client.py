import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET", "")
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "")

def fetch_client():
    # Set up OAuth 1.0a authentication
    client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET_KEY,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
        )

    # Initialize a Tweepy client instance
    return client

def fetch_v2_client():
    # Set up OAuth 2.0 authentication
    client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
    )

    # Initialize a Tweepy client instance
    return client
