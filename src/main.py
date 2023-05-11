import os
import time
import yaml
import random
from .. import prompts

from twitter_client import fetch_client
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
    llm = OpenAI(temperature=0.9)

    # spawn memory
    embeddings = OpenAIEmbeddings(disallowed_special=())
    db = DeepLake(
        dataset_path="./data/", embedding_function=embeddings, read_only=True
    )

    # spawn collector
    collector = TwitterCollector(twitterClient, USER_ID)

    # spawn strategy
    strategy = TwitterStrategy(client=twitterClient, llm=llm, params=params)

    # spawn executor
    executor = TwitterExecutor(twitterClient, llm)

    # run
    run(db, collector, strategy, executor)


def run(db, collector, strategy, executor):
    # while True:
    # Step 1: Collect timeline tweets
    timeline_tweets = collector.retrieve_timeline(10)

    # Step 2: Pass timeline tweets to Strategy
    actions = strategy.select_action(tweets=timeline_tweets)

    # Step 4: Pass actions to Executor
    executor.execute_actions(tweet_actions=actions)

    # Step 5: Generate a tweet
    time.sleep(300)
    themes = prompts["themes"]
    tweet_theme = random.choice(themes)
    executor.generate_tweet(tweet_theme)

    # Sleep for an hour (3600 seconds) before the next iteration
    time.sleep(3600)


if __name__ == "__main__":
    main()
