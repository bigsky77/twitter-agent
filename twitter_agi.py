import os
import random
import twitter_actions
import faiss

from prompts import prompts
from collections import deque
from typing import Dict, List, Optional, Any
from typing import List

from dotenv import load_dotenv
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental import BabyAGI
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.utilities import WikipediaAPIWrapper

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

class BabyAgi:
    def __init__(self, themes, max_iterations: Optional[int] = 2, verbose: bool = False):
        # Initialize components
        self.tweets = []
        # ... (embeddings_model, vectorstore, tools, prompt, llm, etc.) ...
        embeddings_model = OpenAIEmbeddings()

        # Initialize the vectorstore as empty
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        self.vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

        todo_prompt = PromptTemplate.from_template(
            "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}. The todo list must not be longer than four tasks and must end with the Objective being completed."
        )
        todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt)
        search = GoogleSerperAPIWrapper()
        wikipedia = WikipediaAPIWrapper()
        tools = [
            Tool(
                name="Post Tweet",
                func=self.post_tweet,
                description="Usefull when you want to post a tweet.  Takes a string as input",
            ),
            Tool(
                name="TODO",
                func=todo_chain.run,
                description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
            ),
            Tool(
                name="Search",
                func=wikipedia.run,
                description="Usefull when you want to research a topic",
            ),
            Tool(
                name="Wikipedia",
                func=wikipedia.run,
                description="Usefull when you want to research a topic on Wikipedia",
            ),
        ]

        prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
        suffix = """Question: {task}
        {agent_scratchpad}"""
        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["objective", "task", "context", "agent_scratchpad"],
        )

        self.llm = OpenAI(temperature=0.6)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        tool_names = [tool.name for tool in tools]
        agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True
        )


        self.themes = themes
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=verbose
        )

    def post_tweet(self, tweet: str):
        self.tweets.append(tweet)

    def generate_tweet(self, objective: str) -> str:
        baby_agi_instance = BabyAGI.from_llm(
            llm=self.llm,
            vectorstore=self.vectorstore,
            task_execution_chain=self.agent_executor,
            verbose=self.verbose,
            max_iterations=self.max_iterations,
        )

        result = baby_agi_instance({"objective": objective})
        return self.tweets

    def rank_tweets(tweets: List[str], objective: str) -> List[str]:
        # Initialize the LLM and the evaluation prompt
        llm = OpenAI(temperature=0.5)
        evaluate_prompt = "You are an evaluator who is an expert at ranking tweets. Rank the following tweets based on this objective: {objective}. The best tweet is the one that best achieves the objective and is the most funny. Here are the tweets:\n{tweets}\n"

        # Join the list of tweets into a single string with each tweet on a new line
        tweets_str = "\n".join(tweets)

        # Format the prompt with the objective and the concatenated tweets
        prompt = evaluate_prompt.format(objective=objective, tweets=tweets_str)

        # Generate the LLM's response
        response = llm(prompt)

        # Parse the ranked tweets from the response
        ranked_tweets = response.strip().split
        return ranked_tweets
