import tweepy
import os
from dotenv import load_dotenv
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


api_key = os.getenv("API_KEY", "")
api_secret_key = os.getenv("API_SECRET_KEY", "")
access_token = os.getenv("ACCESS_TOKEN", "")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET", "")

auth = tweepy.OAuth1UserHandler(
    api_key, api_secret_key, access_token, access_token_secret
)

api = tweepy.API(auth)


def send_dm(message):
   reciepient_id = "1336800090569183233"
   api.send_direct_message(reciepient_id, message)


def post_tweet(message):
   api.update_status(message)
