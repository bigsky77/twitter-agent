from ...base_strategy import TwitterStrategy
import tweepy
import random
import re
from strategy.media import gif_reply
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Any, Dict, List


class AdvancedTwitterStrategy(TwitterStrategy):
    def __init__(self, agent_id, llm, params):
        super().__init__(agent_id, llm, params)
#
#    self.action_mapping = {
#            "like_timeline_tweets": self.client.like,
#            "retweet_timeline_tweets": self.client.retweet,
#            "reply_to_timeline": self.reply_to_timeline,
#            "quote_tweet": self.quote_tweet,
#            "post_tweet": self.post_tweet,
#            "none": lambda _: None,  # Placeholder for "none" action
#        }
#
#    def generate_actions(self, tweet_actions: List[Dict[str, Any]]):
#        for tweet_action in tweet_actions:
#            action = tweet_action.metadata["action"]
#            method = self.action_mapping.get(action)
#            if method:
#                method(tweet_action.metadata["tweet_id"])
#
#    # Define a function to reply to tweets from the timeline with a given probability
#    def reply_to_timeline(self, tweet_text, tweet_id):
#        response = self.generate_response(tweet_text)
#        media = gif_reply.generate_gif_response(tweet_text)
#        self.client.create_tweet(
#            text=response,
#            in_reply_to_tweet_id=tweet_id,
#            media_ids=media,
#        )
#        print(f"Replied to: {tweet_text}")
#
#    def generate_response(self, tweet_text):
#        reply_prompt = PromptTemplate(
#            input_variables=["input_text"],
#            template=("You are an ancient Chinese dragon whose mission is to bring good luck and wealth to everyone."
#            "You're goal is to create an awesome text about the following topic: {input_text}."
#            "Make sure the reply is under 140 characters."
#            "Be very positive and encouraging, wish people fortune and good luck, encourage them to pursue their dreams."
#            "Use descriptive langauge."
#            "Use lots of emojis and metaphors.  Never use hashtags"),
#        )
#        reply_chain = LLMChain(llm=self.llm, prompt=reply_prompt)
#        response = reply_chain.run(input_text=tweet_text)
#
#        # Remove newlines and periods from the beginning and end of the tweet
#        response = re.sub(r'^[\n\.\"]*', '', response)
#        response = re.sub(r'[\n\.\"]*$', '', response)
#
#        val = self._check_length(response)
#
#        if val == False:
#            response = self.generate_response(tweet_text)
#
#        return response
#
#    def quote_tweet(self, tweet_text, tweet_id):
#        response = self.generate_response(tweet_text)
#        self.client.create_tweet(text=response, quote_tweet_id=tweet_id)
#        print(f"Replied to: {tweet_text}")
#
#    def generate_tweet(self, input_text):
#        tweet_prompt = PromptTemplate(
#            input_variables=["input_text"],
#            template=("You are an agent whose mission is to bring good luck and wealth to everyone."
#            "You're goal is to create an exciting and dramatic tweet about the following text: {input_text}."
#            "Find one or two interesting topics from the text and write about them."
#            "Make sure the reply is under 140 characters."
#            "Be very positive and encouraging, wish people fortune and good luck, encourage them to pursue their dreams."
#            "Use descriptive language.  Your goal is to tell a story with your tweet that excites and inspires people."
#            "Use lots of emojis and metaphors.  Never use hashtags"),
#        )
#        tweet_chain = LLMChain(llm=self.llm, prompt=tweet_prompt)
#        response = tweet_chain.run(input_text=input_text)
#
#        # Remove newlines and periods from the beginning and end of the tweet
#        response = re.sub(r'^[\n\.\"]*', '', response)
#        response = re.sub(r'[\n\.\"]*$', '', response)
#
#        _len_check = self._check_length(response)
#
#        if _len_check is False:
#            self.generate_tweet(input_text)
#
#        print(f"Generated tweet: {response}")
#        self.client.create_tweet(text=response)
#
#    def _check_length(self, text):
#        if len(text) > 280:
