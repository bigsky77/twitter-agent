import os
import tweepy
import yaml
from twitter_client import fetch_client
from langchain.llms import OpenAI
from executor import twitter_executor
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
USER_ID = os.getenv("USER_ID", "")

with open("./params.yaml", "r") as file:
    params = yaml.safe_load(file)

def main():
   twitterClient = fetch_client()
   llm = OpenAI(temperature=0.5)
   executor = twitter_executor.TwitterExecutor(twitterClient, params, llm)
   #executor.generate_tweet("devin booker")
   executor.reply_to_timeline()

if __name__ == '__main__':
    main()
