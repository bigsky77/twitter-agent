"""Twitter-Agent Entry Point"""

import os
import time
import yaml
import asyncio
from functools import wraps

import click


from twitter_client import fetch_clients
from langchain.llms import OpenAI

from executor.executor import TwitterExecutor
from collector.collector import TwitterCollector
from strategy import create_strategy
from storage.db_interface import create_connection, close_connection, get_tweet_ids, create_table, create_reports_table, save_report_to_db

# load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
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
@click.option(
    "--generate-report",
    default=False,
    is_flag=True,  # This makes it a flag that doesn't require a value (just presence indicates True)
    help="Generate a report.")
@click.option(
    "--run-engine",
    default=False,
    is_flag=True,  # Same as above
    help="Run the engine.")
@async_command
async def main(generate_report: bool, run_engine: bool):
    client_data = fetch_clients()
    llm = OpenAI(temperature=0.9)

    # create a database connection
    conn = create_connection()
    create_table(conn)

    # spawn collector, strategy, and executor for each client
    agents = []
    for data in client_data:
        client = data["client"]
        strategy_type = data["strategy"]
        agent_id = data["agent_id"]
        agent_name = data["user_name"]

        collector = TwitterCollector(agent_id, client, params)
        strategy = create_strategy(agent_id, llm, params, strategy_type)
        executor = TwitterExecutor(agent_id, client, conn)

        agents.append((collector, strategy, executor, agent_name, agent_id))

    if generate_report:
        create_reports_table(conn)
        for collector, _, _, _, agent_id in agents:
            tweet_ids = get_tweet_ids(conn)
            collector.generate_report(tweet_ids)
            report = collector.generate_report(tweet_ids)
            print(report)
            save_report_to_db(conn, report)

    # run
    if run_engine:
        await asyncio.gather(
            *(
                run(collector, strategy, executor, agent_name, agent_id)
                for collector, strategy, executor, agent_name, agent_id in agents
            )
        )

    # Close the connection at the end
    close_connection(conn)

async def run(collector, strategy, executor, agent_name, agent_id):

    print(f"\033[92m\033[1m\n*****Running {agent_name} Engine 🚒 *****\n\033[0m\033[0m")

    while True:
        try:
            # Step 1: Run Collector
            print(f"\033[92m\033[1m\n*****Running {agent_name} Collector 🔎 *****\n\033[0m\033[0m")
            twitterstate =  await collector.run()

            # Step 2: Pass timeline tweets to Strategy
            print(f"\033[92m\033[1m\n*****Running {agent_name} Strategy 🐲*****\n\033[0m\033[0m")
            actions = strategy.ingest(twitterstate)

            # Step 4: Pass actions to Executor
            print(f"\033[92m\033[1m\n*****Running {agent_name} Executor🌠 *****\n\033[0m\033[0m")
            executor.execute_actions(tweet_actions=actions)

            # Sleep for an hour (3600 seconds) before the next iteration
            print("Sleeping for an hour💤 💤💤")
            await asyncio.sleep(3600)
        except Exception as e:
            print(f"Error in run: {e}")


if __name__ == "__main__":
    asyncio.run(main())
