from typing import List
from langchain.docstore.document import Document


class TwitterExecutor:
    def __init__(self, client):
        self.client = client

    def execute_actions(self, tweet_actions: List[Document]):
        for tweet_action in tweet_actions:
            if tweet_action.metadata["action"] == "like_timeline_tweets":
                self.client.like(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "retweet_timeline_tweets":
                self.client.retweet(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "reply_to_timeline":
                self.reply_to_timeline(
                    tweet_action.page_content, tweet_action.metadata["tweet_id"]
                )
            elif tweet_action.metadata["action"] == "gif_reply_to_timeline":
                self.gif_reply_to_timeline(
                    tweet_action.page_content,
                    tweet_action.metadata["media_id"],
                    tweet_action.metadata["tweet_id"],
                )
            elif tweet_action.metadata["action"] == "quote_tweet":
                self.quote_tweet(
                    tweet_action.page_content, tweet_action.metadata["tweet_id"]
                )
            elif tweet_action.metadata["action"] == "post_tweet":
                self.post_tweet(tweet_action.page_content)
            elif tweet_action.metadata["action"] == "none":
                pass

    def reply_to_timeline(self, tweet_text, tweet_id):
        self.client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet_id)
        print(f"Replied to: {tweet_text}")

    def gif_reply_to_timeline(self, tweet_text, media_id, tweet_id):
        self.client.create_tweet(
            text=tweet_text, media_ids=media_id, in_reply_to_tweet_id=tweet_id
        )
        print(f"Gif Reply: {tweet_text}")

    def quote_tweet(self, tweet_text, tweet_id):
        self.client.create_tweet(text=tweet_text, quote_tweet_id=tweet_id)
        print(f"Quoted tweet: {tweet_text}")

    def post_tweet(self, tweet_text):
        self.client.create_tweet(text=tweet_text)
        print(f"Posted tweet: {tweet_text}")
