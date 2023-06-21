import re
from ...base_strategy import TwitterStrategy
from langchain.chains import LLMChain
from .prompt import reply_prompt, tweet_prompt

class BasicTwitterStrategy(TwitterStrategy):
    def __init__(self, llm, twitter_client, vectorstore):
        super().__init__(llm, twitter_client, vectorstore)
        self.probabilities = [
            0.20,  # like_timeline_tweets
            0.10,  # retweet_timeline_tweets
            0.00,  # reply_to_timeline
            0.00,  # gif_reply_to_timeline
            0.00,  # quote_tweet
            0.00,  # post_tweet
            0.70,  # none
        ]

    def generate_tweet(self, input_text):
        prompt = tweet_prompt
        tweet_chain = LLMChain(llm=self.llm, prompt=prompt)
        response = tweet_chain.run(input_text=input_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r'^[\n\.\"]*', '', response)
        response = re.sub(r'[\n\.\"]*$', '', response)

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
        response = re.sub(r'^[\n\.\"]*', '', response)
        response = re.sub(r'[\n\.\"]*$', '', response)

        _len_check = self._check_length(response)

        if _len_check is False:
            self.generate_tweet(input_text)

        print(f"Generated tweet: {response}")
        return response
