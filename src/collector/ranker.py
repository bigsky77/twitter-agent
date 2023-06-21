import numpy as np
import openai
import requests
import time
import operator
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import json
from collections import deque


class AgentTrainer:
   def __init__(self, client, weaviate_client, OPENAI_API_KEY):
       self.weaviate_client = weaviate_client
       self.client = client
       self.OPENAI_API_KEY = OPENAI_API_KEY
       self.prompt = "Score this tweet between between 1 and 10."

   async def run(self):
      response = (
          self.weaviate_client.query.get(
              "Tweets", ["tweet", "tweet_id", "agent_id", "date", "author_id", "like_count", "follower_count"]
          )
          .with_limit(100)
          .do()
      )

      x = 100  # number of tweets to return
      sorted_tweets = self.sort_tweets(response, x)
      for tweet in sorted_tweets:
            print("**** Tweet ****")
            print("Date", tweet["date"])
            print("Tweet Cotent", tweet["tweet"])
            print("Like Count", tweet["like_count"])
            print("Follower Count", tweet["follower_count"])
            print("")

      #likes = []
      #followers = []
      #for tweet in sorted_tweets:
      #    like_count = tweet["like_count"]
      #    if like_count is None:
      #          like_count = 0

      #    print("Likes:", like_count)
      #    likes.append(like_count)

      #    follower_count = tweet["follower_count"]
      #    if follower_count is None:
      #          follower_count = 0
      #    followers.append(follower_count)
      #    print("Followers:", follower_count)

      #    tweet_ranks = self.rank_tweets(likes, followers)

      #    file_path = "tweets.json"
      #    new_data = [{"prompt": t["tweet"], "completion": r} for t, r in zip(sorted_tweets, tweet_ranks)]

      #    try:
      #        with open(file_path, "r") as f:
      #            existing_data = json.load(f)
      #    except (FileNotFoundError, json.JSONDecodeError):
      #        existing_data = []

      #    existing_data.extend(new_data)
      #    updated_data = deque(existing_data, maxlen=500)

      #    with open(file_path, "w") as f:
      #        json.dump(list(updated_data), f)

   async def fine_tune_model(self, prompt, dataset="./tweets_prepared.jsonl", model_engine="davinci", num_epochs=3, batch_size=4):
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.OPENAI_API_KEY}",
        }

        data = {
        "model": f"{model_engine}-0",
        "dataset": dataset,
        "prompt": prompt,
        "num_epochs": num_epochs,
        "batch_size": batch_size
        }

        url = "https://api.openai.com/v1/fine-tunes"
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise ValueError("Failed to fine-tune the model.")

        # Get the ID of the fine-tuned model
        model_id = response.json()["model_id"]
        return model_id

   def sort_tweets(self, data: Any, x: int) -> List[dict]:
       tweets = data["data"]["Get"]["Tweets"]
       valid_tweets = [t for t in tweets if t["date"] is not None]
       sorted_tweets = sorted(
           valid_tweets, key=operator.itemgetter("date"), reverse=True
       )
       return sorted_tweets[:x]

   def normalize_data(self, data):
       min_val = min(data)
       max_val = max(data)
       if max_val == min_val:
           return [0.5 for _ in data]  # or whatever constant you prefer
       normalized_data = [(d - min_val) / (max_val - min_val) for d in data]
       return normalized_data

   def log_transform(self, data):
       return [np.log1p(d) for d in data] # np.log1p ensures that log(0) = 0

   def calculate_score(self, normalized_likes, normalized_followers, weight_likes=0.5, weight_followers=0.5):
       return [weight_likes * l + weight_followers * f for l, f in zip(normalized_likes, normalized_followers)]

   def rescale_score(self, scores):
       min_val = min(scores)
       max_val = max(scores)
       rescaled_scores = [(s - min_val) * 10 / (max_val - min_val) for s in scores]
       return rescaled_scores

   def rank_tweets(self, likes, followers, weight_likes=0.5, weight_followers=0.5):
       print("Normalizing data...")
       normalized_likes = self.normalize_data(likes)
       normalized_followers = self.normalize_data(followers)

       print("Transforming data...")
       transformed_likes = self.log_transform(normalized_likes)
       transformed_followers = self.log_transform(normalized_followers)

       print("Calculating scores...")
       scores = self.calculate_score(transformed_likes, transformed_followers, weight_likes, weight_followers)

       final_scores = self.rescale_score(scores)
       return final_scores
