import os
import tweepy
import random
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

api_key = os.getenv("API_KEY", "")
api_secret_key = os.getenv("API_SECRET_KEY", "")
access_token = os.getenv("ACCESS_TOKEN", "")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET", "")

auth = tweepy.OAuth1UserHandler(
    api_key, api_secret_key, access_token, access_token_secret
)

api = tweepy.API(auth)
llm = OpenAI(temperature=0.9)

prompt = PromptTemplate(
    input_variables=["input_text"],
    template="You are a tweet reply agent.  You are replying to a tweet that says: {input_text}.  Make sure the reply is under 140 characters.  Be sarcastic and funny.",
)
chain = LLMChain(llm=llm, prompt=prompt)


def generate_response(input_text):
    # Use the input_text to generate a response using your Language Model
    # For example, using OpenAI's GPT-3
    response = chain.run(input_text=input_text)
    return response


def reply_to_replies():
    my_tweets = api.user_timeline(count=10)

    for tweet in my_tweets:
        print(tweet.user.screen_name, tweet.text)
        # Search for tweets that are a reply to your tweet and mention your screen name
        query = f"to:{tweet.user.screen_name} filter:replies"
        replies = tweepy.Cursor(
            api.search_tweets, q=query, tweet_mode="extended"
        ).items()

        # Keep track of replied tweets using a set
        replied_tweet_ids = set()

        for reply in replies:
            if reply.in_reply_to_status_id == tweet.id:
                # Check if the tweet has already been replied to
                if reply.id not in replied_tweet_ids:
                    user_reply_text = reply.full_text.replace(
                        f"@{tweet.user.screen_name}", ""
                    ).strip()
                    response_text = generate_response(user_reply_text)
                    api.update_status(
                        status=f"@{reply.user.screen_name} {response_text}",
                        in_reply_to_status_id=reply.id,
                        auto_populate_reply_metadata=True,
                    )
                    # Add the replied tweet ID to the set
                    replied_tweet_ids.add(reply.id)

def reply_to_mentions():
    mentions = api.mentions_timeline(tweet_mode='extended')

    for mention in mentions:
        # Check if the tweet has already been replied to
        if not mention.favorited:
            print(f'Replying to {mention.user.screen_name}...')
            user_mention_text = mention.full_text.replace(
                f"@{mention.user.screen_name}", ""
            ).strip()
            response_text = generate_response(user_mention_text)
            api.update_status(
                status=f"@{mention.user.screen_name} {response_text}",
                in_reply_to_status_id=mention.id,
                auto_populate_reply_metadata=True,
            )
            api.create_favorite(mention.id)  # Mark the tweet as "favorited"

def follow_back_followers(min_follower_count, max_follower_count, follow_probability):
    for follower in tweepy.Cursor(api.get_followers).items():
        if not follower.following and min_follower_count <= follower.followers_count <= max_follower_count:
            if random.random() <= follow_probability:
                try:
                    print(f"Following {follower.screen_name}")
                    follower.follow()
                except tweepy.TweepError as e:
                    print(f"Error following {follower.screen_name}: {e}")
                    break

def is_relevant(tweet, keywords):
    return any(keyword.lower() in tweet.text.lower() for keyword in keywords)

# Define a function to like tweets from the timeline with a given probability
def like_timeline_tweets(relevant_like_probability, irrelevant_like_probability, num_tweets, keywords):
    for tweet in tweepy.Cursor(api.home_timeline).items(num_tweets):
        if not tweet.favorited:
            like_probability = relevant_like_probability if is_relevant(tweet, keywords) else irrelevant_like_probability
            if random.random() <= like_probability:
                try:
                    print(f"Liking tweet from {tweet.user.screen_name}: {tweet.text}")
                    api.create_favorite(tweet.id)
                except tweepy.TweepError as e:
                    print(f"Error liking tweet from {tweet.user.screen_name}: {e}")

def retweet_timeline_tweets():
    # Retweet probability (5%)
    RETWEET_PROBABILITY = 0.05
    # Scaling factor for retweet probability of tweets from followers
    FOLLOWER_FACTOR = 2

    # Get the user's timeline
    timeline = api.home_timeline()

    # Get the list of user IDs who follow the authenticated user
    follower_ids = api.followers_ids()

    # Retweet random tweets with 5% probability, with higher probability for tweets from followers
    for tweet in timeline:
        if not tweet.retweeted and not tweet.favorited:
            probability = RETWEET_PROBABILITY
            if tweet.user.id in follower_ids:
                probability *= FOLLOWER_FACTOR
            if random.random() < probability:
                try:
                    api.retweet(tweet.id)
                    print(f"Retweeted: {tweet.text}")
                except tweepy.TweepError as e:
                    print(f"Error retweeting: {e}")


if __name__ == "__main__":
    min_follower_count = 50
    max_follower_count = 5000
    follow_probability = 0.8  # Set the follow-back probability (0.8 = 80% chance)
    follow_back_followers(min_follower_count, max_follower_count, follow_probability)

    relevant_like_probability = 0.35  # Set the like probability for relevant tweets (0.65 = 65% chance)
    irrelevant_like_probability = 0.15  # Set the like probability for irrelevant tweets (0.35 = 35% chance)
    num_tweets = 20
    keywords = ["AGI", "Langchain", "BabyAgi", "Python", "Paradigm", "Ethereum", "Warriors", "NBA", "Coding", "DeFi"]  # Set your relevant keywords here
    like_timeline_tweets(relevant_like_probability, irrelevant_like_probability, num_tweets, keywords)

    reply_to_replies()
    reply_to_mentions()
    retweet_timeline_tweets()
