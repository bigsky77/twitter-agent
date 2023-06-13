import re
import weaviate
import logging
from ...base_strategy import TwitterStrategy
from langchain.chains import LLMChain
from .prompt import reply_prompt, tweet_prompt
from datetime import datetime, timedelta
from typing import List
from termcolor import colored
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.experimental.generative_agents import (
    GenerativeAgent,
    GenerativeAgentMemory,
)

from langchain.vectorstores import Weaviate
import math
import faiss


class BigSkyTwitterStrategy(TwitterStrategy):
    def __init__(self, agent_id, llm, params):
        super().__init__(agent_id, llm, params)
        self.bigskys_memory = GenerativeAgentMemory(
            llm=self.llm,
            memory_retriever=self.create_new_memory_retriever(),
            verbose=False,
            reflection_threshold=8,
        )
        self.bigsky = GenerativeAgent(
            name="bigsky",
            age=28,
            traits="Athlete.  Loves sports. Always positive. Asks deep philosophical questions.",  # You can add more persistent traits here
            status="want's to make friends",
            memory_retriever=self.create_new_memory_retriever(),
            llm=self.llm,
            memory=self.bigskys_memory,
        )

    def ingest(self, twitterstate):
        for tweet in twitterstate.list_tweets:
            self.bigskys_memory.add_memory(tweet.page_content)
        results = self.process_and_action_tweets(twitterstate.list_tweets)
        return results

    def relevance_score_fn(self, score: float) -> float:
        """Return a similarity score on a scale [0, 1]."""
        # This will differ depending on a few things:
        # - the distance / similarity metric used by the VectorStore
        # - the scale of your embeddings (OpenAI's are unit norm. Many others are not!)
        # This function converts the euclidean norm of normalized embeddings
        # (0 is most similar, sqrt(2) most dissimilar)
        # to a similarity function (0 to 1)
        return 1.0 - score / math.sqrt(2)

    def create_new_memory_retriever(self):
        """Create a new vector store retriever unique to the agent."""
        # Define your embedding model
        embeddings_model = OpenAIEmbeddings()
        client = weaviate.Client("http://localhost:8080")
        # Initialize the vectorstore as empty
        embedding_size = 1536
        vectorstore = Weaviate(
            client,
            "bigsky",
            "test",
            embeddings_model.embed_query,
            #InMemoryDocstore({}),
            #self.relevance_score_fn
        )
        return TimeWeightedVectorStoreRetriever(
            vectorstore=vectorstore, other_score_keys=["importance"], k=15
        )

    def generate_tweet(self, input_text):
        prompt = tweet_prompt
        tweet_chain = LLMChain(llm=self.llm, prompt=prompt)
        response = tweet_chain.run(input_text=input_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r"^[\n\.\"]*", "", response)
        response = re.sub(r"[\n\.\"]*$", "", response)

        _len_check = self._check_length(response)

        if _len_check is False:
            self.generate_tweet(input_text)

        print(f"Generated tweet: {response}")
        return response

    def interview_agent(self, agent: GenerativeAgent, message: str) -> str:
        """Help the notebook user interact with the agent."""
        new_message = f"Write reply to this {message} in under 120 characters. You love using emojis and never use hashtags. Your goal is to create an engaging response that prompts more conversation"
        res = agent.generate_reaction(new_message)[1]
        new_text = re.sub(r"BigSky\s*", "", res)
        return new_text

    def generate_response(self, input_text):
        response = self.interview_agent(self.bigsky, input_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r"^[\n\.\"]*", "", response)
        response = re.sub(r"[\n\.\"]*$", "", response)

        _len_check = self._check_length(response)

        if _len_check is False:
            self.generate_tweet(input_text)

        print(f"Generated Response: {response}")
        return response
