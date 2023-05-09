import os
import tweepy
import yaml
import requests

from twitter_client import fetch_client
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI

from executor import twitter_executor
from collector import collector

# load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
ACTIVELOOP_TOKEN = os.getenv("ACTIVELOOP_TOKEN", "")

with open("./params.yaml", "r") as file:
    params = yaml.safe_load(file)

def main():
   twitterClient = fetch_client()
   llm = OpenAI(temperature=0.5)
   username = "bigsky77"
   dataset_path = f"hub://{username}/twitter-agent"

   # create memory
   embeddings = OpenAIEmbeddings(disallowed_special=())
   db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings)

   # spawn executor
   executor = twitter_executor.TwitterExecutor(twitterClient, params, llm)

   # spawn collector
   collector_instance = collector.TwitterCollector(twitterClient, db)
   collector_instance.load(count=10)


if __name__ == '__main__':
    main()
