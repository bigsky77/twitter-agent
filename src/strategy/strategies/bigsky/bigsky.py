import re
from ...base_strategy import TwitterStrategy
from langchain.chains import LLMChain
from .bigsky_prompt import reply_prompt, tweet_prompt, tweet_memory_prompt

class BigSkyTwitterStrategy(TwitterStrategy):
    def __init__(self, llm, vectorstore):
        super().__init__(llm, vectorstore)

    def generate_tweet(self, input_text):
        topic = input_text
        docs = self.vectorstore.similarity_search(topic, k=1)
        prompt = tweet_memory_prompt
        inputs = [{"context": doc.page_content, "topic": topic} for doc in docs]
        tweet_chain = LLMChain(llm=self.llm, prompt=prompt)
        answer = tweet_chain.apply(inputs)
        response = answer[0]["text"]

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
