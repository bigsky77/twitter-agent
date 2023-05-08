import os
import tweepy
from twitter_client import fetch_client
from executor import twitter_executor
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
USER_ID = os.getenv("USER_ID", "")

def main():
   twitterClient = fetch_client()
   executor = twitter_executor.TwitterExecutor(twitterClient)
   res  = executor.get_my_timeline(10)
   print(res)

if __name__ == '__main__':
    main()
