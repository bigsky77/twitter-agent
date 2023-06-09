import re
from ...base_strategy import TwitterStrategy
from langchain.chains import LLMChain
from .remilio_prompt import reply_prompt, tweet_prompt, memory_prompt
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain

class RemilioTwitterStrategy(TwitterStrategy):
    def __init__(self, agent_id, llm, params):
        super().__init__(agent_id, llm, params)
        self.embeddings = OpenAIEmbeddings()
        self.db = DeepLake(
            dataset_path="./data/deeplake/remilio",
            embedding_function=self.embeddings,
            read_only=True,
        )

    def ingest(self, twitterstate):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(twitterstate.list_tweets)
        #self.db.add_documents(docs)
        results = self.process_and_action_tweets(twitterstate.list_tweets)
        return results

    def generate_tweet(self, input_text):
        topic = input_text
        docs = self.db.similarity_search(topic, k=1)
        prompt = memory_prompt
        inputs = [{"context": doc.page_content, "topic": topic} for doc in docs]
        tweet_chain = LLMChain(llm=self.llm, prompt=prompt)
        answer = tweet_chain.apply(inputs)
        response = answer[0]["text"]
        #response = chain.run(input_text=input_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r"^[\n\.\"]*", "", response)
        response = re.sub(r"[\n\.\"]*$", "", response)

        _len_check = self._check_length(response)

        if _len_check is False:
            self.generate_tweet(input_text)

        print(f"Generated tweet: {response}")
        return response

    def generate_response(self, input_text):
        prompt = reply_prompt
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