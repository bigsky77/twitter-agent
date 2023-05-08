import tweepy
import random

class TwitterExecutor:
    def __init__(self, client):
        self.client = client

    def get_me(self):
        return self.client.get_me()

    def get_user(self, user_id):
        return self.client.get_user(user_id)

    def get_my_timeline(self, count):
        return self.client.get_home_timeline(max_results=count)
