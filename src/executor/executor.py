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

    def execute_actions(actions):
        pass

    # Define a function to like tweets from the timeline with a given probability
    def like_tweets(self, keywords, num_tweets=10):
        irrelevant_like_probability = self.params["irrelevant_like_probability"],
        relevant_like_probability = self.params["relevant_like_probability"]

        response = self.get_my_timeline(num_tweets)
        for tweet in response.data:
            tweet_id = tweet.id
            tweet_text = tweet.text

            if not tweet_text.startswith('RT'):
                like_probability = (
                    relevant_like_probability
                    if self.is_relevant(tweet_text, keywords)
                    else irrelevant_like_probability
                )
                if random.random() <= like_probability:
                    try:
                        print(f"Liking tweet: {tweet_text}")
                        self.client.like(tweet_id)
                    except tweepy.TweepError as e:
                        print(f"Error liking tweet: {e}")

    @staticmethod
    def is_relevant(tweet_text, keywords):
        return any(keyword.lower() in tweet_text.lower() for keyword in keywords)

    # Define a function to rewind tweets from the timeline with a given probability
    def retweet_timeline_tweets(self):
        RETWEET_PROBABILITY = self.params["retweet_probability"]

        # Get the user's timeline
        timeline = self.get_my_timeline(10)

        # Retweet random tweets with a given probability, with higher probability for tweets from followers
        for tweet in timeline.data:
            tweet_id = tweet.id
            tweet_text = tweet.text

            if not tweet_text.startswith('RT'):
                probability = RETWEET_PROBABILITY
                if random.random() < probability:
                    try:
                        self.client.retweet(tweet_id)
                        print(f"Retweeted: {tweet_text}")
                    except tweepy.TweepError as e:
                        print(f"Error retweeting: {e}")


    # Define a function to reply to tweets from the timeline with a given probability
    def reply_to_timeline(self):
        REPLY_PROBABILITY = self.params["reply_probability"]
        timeline = self.get_my_timeline(10)

        for tweet in timeline.data:
            tweet_id = tweet.id
            tweet_text = tweet.text

            if not tweet_text.startswith('RT'):
                probability = REPLY_PROBABILITY
                if random.random() < probability:
                    try:
                        response = self.generate_response(tweet_text)
                        media = gif_reply.generate_gif_response(tweet_text)
                        self.client.create_tweet(text=response, in_reply_to_tweet_id=tweet_id, media_ids=media)
                        print(f"Replied to: {tweet_text}")
                    except tweepy.TweepError as e:
                        print(f"Error replying: {e}")


    def generate_response(self, tweet_text):
        reply_prompt = PromptTemplate(
            input_variables=["input_text"],
            template="You are a tweet reply agent.  You are replying to a tweet that says: {input_text}.  Make sure the reply is under 140 characters.  Be sarcastic and funny.",
        )
        reply_chain = LLMChain(llm=self.llm, prompt=reply_prompt)
        response = reply_chain.run(input_text=tweet_text)
        return response

    def quote_tweet(self):
        REPLY_PROBABILITY = self.params["reply_probability"]
        timeline = self.get_my_timeline(10)
        for tweet in timeline.data:
            tweet_id = tweet.id
            tweet_text = tweet.text

            probability = REPLY_PROBABILITY
            if random.random() < probability:
                try:
                    response = self.generate_response(tweet_text)
                    self.client.create_tweet(text=response, quote_tweet_id=tweet_id)
                    print(f"Replied to: {tweet_text}")
                except tweepy.TweepError as e:
                    print(f"Error replying: {e}")

    def generate_tweet(self, input_text):
        tweet_prompt = PromptTemplate(
            input_variables=["input_text"],
            template="You are a tweet agent.  You're goal is to create an awesome tweet about the following topic: {input_text}.  Make sure the reply is under 140 characters.  Be sarcastic and funny. Use emojis but no hashtags.",
        )
        tweet_chain = LLMChain(llm=self.llm, prompt=tweet_prompt)
        response = tweet_chain.run(input_text=input_text)
        self.client.create_tweet(text=response)
