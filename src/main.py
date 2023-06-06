"""Twitter-Agent Entry Point"""

import os
import time
import yaml
import asyncio
from functools import wraps

import click


from twitter_client import fetch_client, fetch_v2_client
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

def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass



@cli.command()
@click.option("--fetch-status", default=None, help="Fetch updates from twitter")
@async_command
async def main(fetch_status):
    twitterClient_v2 = fetch_v2_client()
    twitterClient = fetch_client()
    llm = OpenAI(temperature=0.9)

    # spawn collector
    collector = TwitterCollector(twitterClient, twitterClient_v2, USER_ID, params)

    # spawn strategy
    strategy = TwitterStrategy(client=twitterClient, llm=llm, params=params)

    # spawn executor
    executor = TwitterExecutor(twitterClient, llm)

    if fetch_status:
        collector.fetch_status()
    # run
    #run(collector, strategy, executor)


def run(collector, strategy, executor):
    while True:
        # Step 1: Run Collector
        twitterstate = collector.run()

        # Step 2: Pass timeline tweets to Strategy
        actions = strategy.ingest(twitterstate)

        # Step 4: Pass actions to Executor
        executor.execute_actions(tweet_actions=actions)

        text = ''
        for tweet in twitterstate.list_tweets:
            text += tweet.page_content + ''

        # Step 5: Generate a tweet
        executor.generate_tweet(text)

        # Sleep for an hour (3600 seconds) before the next iteration
        print("Sleeping for an hour...")
        time.sleep(3600)

if __name__ == "__main__":

    main()
