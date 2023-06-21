"""Twitter-Agent Entry Point"""

import os
import json
import time
import weaviate
import yaml
import pdb
import asyncio
from functools import wraps

import click

from langchain.llms import OpenAI
from langchain.vectorstores import Weaviate
from langchain.embeddings.openai import OpenAIEmbeddings


from twitter_client import fetch_clients
from executor.executor import TwitterExecutor
from collector.collector import TwitterCollector
from strategy import create_strategy

# load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USER_ID = os.getenv("USER_ID", "")


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--run-engine", default=False, is_flag=True, help="Run the engine."  # Same as above
)
@click.option(
    "--test", default=False, is_flag=True, help="Test the engine."  # Same as above
)
@click.option(
    "--ingest", default=False, is_flag=True, help="Ingest data into Weaviate."
)
@async_command
async def main(run_engine: bool, test: bool, ingest: bool):
    twitter_clients = fetch_clients()
    weaviate_client = weaviate.Client("http://localhost:8080")

    llm = OpenAI(temperature=0.9)
    embeddings = OpenAIEmbeddings()

    # spawn collector, strategy, and executor for each client
    agents = []
    for twitter_client in twitter_clients:
        client = twitter_client["client"]
        strategy_type = twitter_client["strategy"]
        agent_id = twitter_client["agent_id"]
        agent_name = twitter_client["user_name"]

        vectorstore = Weaviate(weaviate_client, "Remilio", "content", embeddings)

        collector = TwitterCollector(agent_id, client, vectorstore, weaviate_client)
        strategy = create_strategy(llm, strategy_type, twitter_client, vectorstore)
        executor = TwitterExecutor(agent_id, client)

        if ingest:
            await collector.ingest()

        agents.append((collector, strategy, executor, agent_name, agent_id))

    # run
    if run_engine:
        await asyncio.gather(
            *(
                run(collector, strategy, executor, agent_name, agent_id, test)
                for collector, strategy, executor, agent_name, agent_id in agents
            )
        )


async def run(collector, strategy, executor, agent_name, agent_id, test):
    print(f"\033[92m\033[1m\n*****Running {agent_name} Engine 🚒 *****\n\033[0m\033[0m")

    while True:
        try:
            # Step 1: Run Collector
            print(
                f"\033[92m\033[1m\n*****Running {agent_name} Collector 🔎 *****\n\033[0m\033[0m"
            )
            twitterstate = await collector.run()
            print(f"Twitterstate: {twitterstate}")

            # Step 2: Pass timeline tweets to Strategy
            print(
                f"\033[92m\033[1m\n*****Running {agent_name} Strategy 🐲*****\n\033[0m\033[0m"
            )
            actions = strategy.ingest(twitterstate)

            # Step 4: Pass actions to Executor
            print(
                f"\033[92m\033[1m\n*****Running {agent_name} Executor🌠 *****\n\033[0m\033[0m"
            )
            if test:
                pass
            else:
                executor.execute_actions(tweet_actions=actions)

            # Sleep for an hour (3600 seconds) before the next iteration
            print("Sleeping for an hour💤 💤💤")
            await asyncio.sleep(3600)
        except Exception as e:
            print(f"Error in run: {e}")


if __name__ == "__main__":
    asyncio.run(main())
