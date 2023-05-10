import os
import time
import tweepy
import yaml
import requests

from twitter_client import fetch_client
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI

from executor.executor import TwitterExecutor
from collector.collector import TwitterCollector
from strategy.strategy import TwitterStrategy

# load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
ACTIVELOOP_TOKEN = os.getenv("ACTIVELOOP_TOKEN", "")
USER_ID = os.getenv("USER_ID", "")

with open("./params.yaml", "r") as file:
    params = yaml.safe_load(file)


def main():
    twitterClient = fetch_client()
    llm = OpenAI(temperature=0.5)

    username = "bigsky77"
    dataset_path = f"hub://{username}/twitter-agent"
    local_dataset_path = f"../data/my_db"

    # create memory
    embeddings = OpenAIEmbeddings(disallowed_special=())
    db = DeepLake(dataset_path=local_dataset_path, embedding_function=embeddings)

    # spawn collector
    collector = TwitterCollector(twitterClient, db, USER_ID)

    # spawn executor
    executor = TwitterExecutor(twitterClient, params, llm)

    # spawn strategy
    strategy = TwitterStrategy(client=twitterClient, llm=llm, params=params)

    while True:
        # Step 1: Collect timeline tweets
        timeline_tweets = collector.upload_timeline(5)

        # Step 2: Pass timeline tweets to Strategy
        actions = strategy.analyze_tweets(timeline_tweets=timeline_tweets)
        print(actions)

        # Step 4: Pass actions to Executor
        # executor.execute_actions(actions=actions)

        # Sleep for an hour (3600 seconds) before the next iteration
        time.sleep(3600)


if __name__ == "__main__":
    main()
