import tweepy
import random
import re
from strategy.media import gif_reply
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Any, Dict, List

class TwitterExecutor:
    def __init__(self, client, llm):
        self.client = client
        self.llm = llm

    def get_me(self):
        return self.client.get_me()

    def get_user(self, user_id):
        return self.client.get_user(user_id)

    def get_my_timeline(self, count):
        return self.client.get_home_timeline(max_results=count)

    def execute_actions(self, tweet_actions: List[Dict[str, Any]]):
        for tweet_action in tweet_actions:
            if tweet_action.metadata["action"] == "like_timeline_tweets":
                self.client.like(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "retweet_timeline_tweets":
                self.client.retweet(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "reply_to_timeline":
                self.reply_to_timeline(tweet_action.page_content, tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "quote_tweet":
                self.quote_tweet(tweet_action.page_content, tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "none":
                pass

    # Define a function to reply to tweets from the timeline with a given probability
    def reply_to_timeline(self, tweet_text, tweet_id):
        response = self.generate_response(tweet_text)
        media = gif_reply.generate_gif_response(tweet_text)
        self.client.create_tweet(
            text=response,
            in_reply_to_tweet_id=tweet_id,
            media_ids=media,
        )
        print(f"Replied to: {tweet_text}")

    def generate_response(self, tweet_text):
        reply_prompt = PromptTemplate(
            input_variables=["input_text"],
            template=("You are an ancient Chinese dragon whose mission is to bring good luck and wealth to everyone."
            "You're goal is to create an awesome text about the following topic: {input_text}."
            "Make sure the reply is under 140 characters."
            "Be very positive and encouraging, wish people fortune and good luck, encourage them to pursue their dreams."
            "Use descriptive langauge."
            "Use lots of emojis and metaphors.  Never use hashtags"),
        )
        reply_chain = LLMChain(llm=self.llm, prompt=reply_prompt)
        response = reply_chain.run(input_text=tweet_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r'^[\n\.\"]*', '', response)
        response = re.sub(r'[\n\.\"]*$', '', response)

        return response

    def quote_tweet(self, tweet_text, tweet_id):
        response = self.generate_response(tweet_text)
        self.client.create_tweet(text=response, quote_tweet_id=tweet_id)
        print(f"Replied to: {tweet_text}")

    def generate_tweet(self, input_text):
        tweet_prompt = PromptTemplate(
            input_variables=["input_text"],
            template=("You are an agent whose mission is to bring good luck and wealth to everyone."
            "You're goal is to create an exciting and dramatic tweet about the following text: {input_text}."
            "Find one or two interesting topics from the text and write about them."
            "Make sure the reply is under 140 characters."
            "Be very positive and encouraging, wish people fortune and good luck, encourage them to pursue their dreams."
            "Use descriptive language.  Your goal is to tell a story with your tweet that excites and inspires people."
            "Use lots of emojis and metaphors.  Never use hashtags"),
        )
        tweet_chain = LLMChain(llm=self.llm, prompt=tweet_prompt)
        response = tweet_chain.run(input_text=input_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r'^[\n\.\"]*', '', response)
        response = re.sub(r'[\n\.\"]*$', '', response)

        print(f"Generated tweet: {response}")
        self.client.create_tweet(text=response)
