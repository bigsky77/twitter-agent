import os
import random
import twitter_actions
import faiss
import auth

from prompts import prompts
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

from twitter_agi import BabyAgi

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

def authenticate():
    api = auth.make_api()
    return api

class TwitterAGI:
    def __init__(self, baby_agi: BabyAgi):
        self.api = authenticate()
        self.baby_agi = baby_agi
        # Initialize other necessary components for your AGI, e.g. your RL model

    def generate_tweet(self, objective: str):
        # Generate a tweet using the BabyAgi instance
        tweet = self.baby_agi.generate_tweet(objective)
        return tweet

    def select_tweet(self, tweets: List[str]):
        # Select the best tweet from the list of tweets
        return tweet

    def post_tweet(self, tweet):
        status = self.api.update_status(tweet)
        return status.id

    def like_timeline_tweet(self, tweet_id):
        # Like the tweet using the Twitter API
        pass

    def respond_to_tweet(self, tweet_id, response):
        # Reply to the tweet using the Twitter API
        pass

    def retweet_tweet(self, tweet_id):
        # Retweet the tweet using the Twitter API
        pass

    def respond_to_dm(self):
        # Reply to the DM using the Twitter API
        pass

    def follow_user(self, user_id):
        # Follow the user using the Twitter API
        pass

    def unfollow_user(self, user_id):
        # Unfollow the user using the Twitter API
        pass

    def send_dm(self, user_id, message):
        # Send a DM to the user using the Twitter API
        pass

    def get_likes_feedback(self, tweet_id):
        # Retrieve the number of likes for the given tweet
        tweet = self.api.get_status(tweet_id)
        return tweet.favorite_count

    def update_model(self, tweet_id):
        # Update your RL model using the feedback (likes) from the tweet
        likes = self.get_likes_feedback(tweet_id)
        # Update the model using the likes as a reward signal
        pass

    def evaluate(self, tweet: str) -> int:
        tweet_id = self.post_tweet(tweet)
        likes = self.get_likes_feedback(tweet_id)
        return likes

# Main function
def main():
    # Define your objective
    themes = prompts["themes"]
    theme = random.choice(themes)
    include = [
        "Use emojis",
        "Don't use emojis or hashtags"
    ]
    include = random.choice(include)
    OBJECTIVE = f"Write an exciting tweet about {theme}. {include}"

    # Create a BabyAgi instance
    baby_agi = BabyAgi(themes=themes)

    # Create a TwitterAGI instance
    twitter_agi = TwitterAGI(baby_agi)

    # Generate a tweet using the AGI logic
    tweets = twitter_agi.generate_tweet(OBJECTIVE)
    ranked_tweets = baby_agi.rank_tweets(tweets, OBJECTIVE)

if __name__ == '__main__':
    main()
