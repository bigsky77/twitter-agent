import tweepy
import os
from dotenv import load_dotenv
import yaml
from langchain.llms.openai import OpenAI
from langchain.requests import RequestsWrapper
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.tools import BaseTool
from langchain.agents import AgentType, Tool, initialize_agent, tool

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


API_KEY = "EZFpo0SUy5ytW3p3HEIbocZz6"
API_SECRET_KEY = "dtS2hHf6YMmk0lTUFKWFKy3K17LVwe6xyxEcU6rhqqtt2ieC2o"
ACCESS_TOKEN = "1614799524580712449-wynFln05gFqRCviC3e3tO7ina6MDc1"
ACCESS_TOKEN_SECRET = "RyZmDFbD6uiRA5O46jaB8rS10PCbTRZM8iwKepmoqxoSH"

auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
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

agent = initialize_agent(
   tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

result = agent.run(
   "how many people are in the world?",
)
