import tweepy
import random
from strategy.media import gif_reply
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class TwitterExecutor:
    def __init__(self, client, params, llm):
        self.client = client
        self.params = params
        self.llm = llm

    def get_me(self):
        return self.client.get_me()

    def get_user(self, user_id):
        return self.client.get_user(user_id)

    def get_my_timeline(self, count):
        return self.client.get_home_timeline(max_results=count)

    def execute_actions(self, actions: List[Dict[str, Any]]):
        for action in actions.data:
            if action["action"] == "like_tweets":
                self.client.like(action.id)
            elif action["action"] == "retweet_timeline_tweets":
                self.client.retweet(tweet_id)
            elif action["action"] == "reply_to_timeline":
                self.reply_to_timeline(action.text, action.id)
            elif action["action"] == "quote_tweet":
                self.quote_tweet(action.text, action.id)
            elif action["action"] == "none":
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
            template="You are a tweet reply agent.  You are replying to a tweet that says: {input_text}.  Make sure the reply is under 140 characters.  Be sarcastic and funny.",
        )
        reply_chain = LLMChain(llm=self.llm, prompt=reply_prompt)
        response = reply_chain.run(input_text=tweet_text)
        return response

    def quote_tweet(self):
        response = self.generate_response(tweet_text)
        self.client.create_tweet(text=response, quote_tweet_id=tweet_id)
        print(f"Replied to: {tweet_text}")

    def generate_tweet(self, input_text):
        tweet_prompt = PromptTemplate(
            input_variables=["input_text"],
            template="You are a tweet agent.  You're goal is to create an awesome tweet about the following topic: {input_text}.  Make sure the reply is under 140 characters.  Be sarcastic and funny. Use emojis but no hashtags.",
        )
        tweet_chain = LLMChain(llm=self.llm, prompt=tweet_prompt)
        response = tweet_chain.run(input_text=input_text)
        self.client.create_tweet(text=response)
