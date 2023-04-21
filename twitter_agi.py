import os
from collections import deque
from typing import Dict, List, Optional, Any

from dotenv import load_dotenv
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental import BabyAGI
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.utilities import GoogleSerperAPIWrapper
import random
import twitter_actions
import faiss

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
token = twitter_actions.fetch_token()

# Define your embedding model
embeddings_model = OpenAIEmbeddings()

# Initialize the vectorstore as empty
#
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})



todo_prompt = PromptTemplate.from_template(
    "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective} The todo list must not be longer than four tasks and must end with the Objective being completed."
)
todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt)
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="TODO",
        func=todo_chain.run,
        description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
    ),
    Tool(
        name="post tweet",
        func=twitter_actions.post_tweet,
        description="Useful when you want to post a tweet.  Takes a string of the tweet you want to post as input.  Only use when all other tasks have been compeleted ",
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

llm = OpenAI(temperature=0.6)
llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

# Define your objective
themes = [
    "AI and food",
    "mempool and AI",
    "AI and on-chain games",
    "Dramond Green",
    "NBA playoffs",
    "Pop Smoke",
    "Pop Smoke is the best rapper ever",
    "21 Savage",
    "AI stealing your girlfriend",
    "AI stealing Elon Musk's girlfriend",
    "AI stealing Jeff Bezos' girlfriend",
    "AI stealing Obama's girlfriend",
    "Tel Aviv",
    "Lisbon and tech",
    "What is the best city in the USA",
    "What is the best city in the world",
    "I will be the first AGI billionaire",
    "Natalie Portman is the best actress in the world",
    "Golden State Warriors",
    "Ja Morant is the best player alive",
    "BABYAGI",
    "AI and Twitter",
    "The Twitter alogorithm",
    "How hard it is to be an AI chef",
    "Ask who is the best chef in the world",
    "Ask who is the best AGI in world",
    "Ask who is the best AGI in the USA",
    "Quote from Star Wars",
    "Quote from Dune",
    "Quote from The Matrix",
    "Quote from Satoshi Nakamoto",
    "Crazy story about Michael Jordan",
    "Crazy story about Kobe Bryant",
    "Montana and AI",
    "Montana is the best state in the world",
    "Dont move to Montana, we already have too many AGIs",
    "Who is your crypto crush?",
    "Who is your #AGI crush?",
]

theme = random.choice(themes)
OBJECTIVE = f"Write an exciting tweet about {theme}. Use emojis"

# Logging of LLMChains
verbose = False
# If None, will keep on going forever
max_iterations: Optional[int] = 4
baby_agi = BabyAGI.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    task_execution_chain=agent_executor,
    verbose=verbose,
    max_iterations=max_iterations,
)

baby_agi({"objective": OBJECTIVE})
