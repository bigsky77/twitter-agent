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


tools = [
   Tool(
       name="Send DM",
       func=send_dm,
       description="Useful for when you need to send a direct message. The input should be a string of the message you want to send.",
   ),
   Tool(
       name="Post Tweet",
       func=post_tweet,
       description="Useful for when you need to post a Tweet.  The input should be a string of the Tweet you want to post.",
   ),
]

llm = ChatOpenAI(temperature=0.5)
agent = initialize_agent(
   tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

result = agent.run(
   "write a tweet about how twitter is like the mempool for artifical intelligence",
)
