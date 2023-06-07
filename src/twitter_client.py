import os
import tweepy
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "")
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "")

# Load the access tokens and secrets from the YAML file
with open('./tokens.yml', 'r') as f:
    tokens = yaml.safe_load(f)

def _fetch_client(access_token, access_token_secret):
    client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET_KEY,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True,
        )

    return client


def fetch_clients() -> list:
    # Initialize a client for each set of access tokens/secrets
    client_data = []
    for token in tokens:
        client = _fetch_client(token['token'], token['secret'])
        strategy = token['strategy']
        user_name = token['user_name']
        agent_id = token['id']
        client_data.append({
            "client": client,
            "strategy": strategy,
            "user_name": user_name,
            "agent_id": agent_id,
        })

    return client_data
