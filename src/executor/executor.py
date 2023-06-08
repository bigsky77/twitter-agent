from typing import List
from langchain.docstore.document import Document
from storage.db_interface import insert_tweet
import datetime


class TwitterExecutor:
    def __init__(self, agent_id, client, conn):
        self.agent_id = agent_id
        self.client = client
        self.conn = conn

    def execute_actions(self, tweet_actions: List[Document]):
        for tweet_action in tweet_actions:
            if tweet_action.metadata["action"] == "like_timeline_tweets":
                self.client.like(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "retweet_timeline_tweets":
                self.client.retweet(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "reply_to_timeline":
                self.handle_tweet_action(
                    self.reply_to_timeline,
                    tweet_action.page_content,
                    tweet_action.metadata["tweet_id"],
                )
            elif tweet_action.metadata["action"] == "gif_reply_to_timeline":
                self.handle_tweet_action(
                    self.gif_reply_to_timeline,
                    tweet_action.page_content,
                    tweet_action.metadata["media_id"],
                    tweet_action.metadata["tweet_id"],
                )
            elif tweet_action.metadata["action"] == "quote_tweet":
                self.handle_tweet_action(
                    self.quote_tweet,
                    tweet_action.page_content,
                    tweet_action.metadata["tweet_id"],
                )
            elif tweet_action.metadata["action"] == "post_tweet":
                self.handle_tweet_action(self.post_tweet, tweet_action.page_content)
            elif tweet_action.metadata["action"] == "none":
                pass

    def handle_tweet_action(self, action_function, *args):
        response = action_function(*args)
        tweet_response = response.data

        user_id = self.agent_id
        tweet_id = tweet_response["id"]
        tweet = tweet_response["text"]

        current_date = datetime.datetime.now().strftime(
            "%y-%m-%d %H:%M:%S"
        )  # corrected format
        insert_tweet(self.conn, user_id, tweet_id, tweet, current_date)

        print(f"Action performed: {tweet}")

    def reply_to_timeline(self, tweet_text, tweet_id):
        return self.client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet_id)

    def gif_reply_to_timeline(self, tweet_text, media_id, tweet_id):
        return self.client.create_tweet(
            text=tweet_text, media_ids=media_id, in_reply_to_tweet_id=tweet_id
        )

    def quote_tweet(self, tweet_text, tweet_id):
        return self.client.create_tweet(text=tweet_text, quote_tweet_id=tweet_id)

    def post_tweet(self, tweet_text):
        return self.client.create_tweet(text=tweet_text)
