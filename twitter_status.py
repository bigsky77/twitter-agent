import os
import tweepy
import pytz
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv("API_KEY", "")
api_secret_key = os.getenv("API_SECRET_KEY", "")
access_token = os.getenv("ACCESS_TOKEN", "")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET", "")

auth = tweepy.OAuth1UserHandler(
    api_key, api_secret_key, access_token, access_token_secret
)

api = tweepy.API(auth)

user_id=1614799524580712449
user = api.get_user(user_id=user_id)

follower_count = api.get_follower_ids()
count = len(follower_count)

# Set up time range for the past 24 hours
now = datetime.now(pytz.utc)
one_day_ago = now - timedelta(days=1)

# Initialize counts
tweet_count = 0
reply_count = 0
dm_count = 0
like_count = 0

 # Get tweets from the past 24 hours
for tweet in tweepy.Cursor(api.user_timeline, user_id=user.id, tweet_mode="extended", since_id=one_day_ago.timestamp()).items():
    if tweet.in_reply_to_status_id is not None:
        reply_count += 1
    else:
        tweet_count += 1
        like_count += tweet.favorite_count

print("Date: " + str(now))
print("Followers: " + str(count))
print("Tweets: " + str(tweet_count))
print("Replies: " + str(reply_count))
print("Likes: " + str(like_count))
