from typing import List
from langchain.docstore.document import Document


class TwitterExecutor:
    def __init__(self, agent_id, client):
        self.agent_id = agent_id
        self.client = client

    def execute_actions(self, tweet_actions: List[Document]):
        for tweet_action in tweet_actions:
            if tweet_action.metadata["action"] == "like_timeline_tweets":
                print("Tweet Liked:", tweet_action.metadata["tweet_id"])
                self.client.like(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "retweet_timeline_tweets":
                print("Tweet Retweeted:", tweet_action.metadata["tweet_id"])
                self.client.retweet(tweet_action.metadata["tweet_id"])
            elif tweet_action.metadata["action"] == "reply_to_timeline":
                self.handle_tweet_action(
                    self.reply_to_timeline,
                    tweet_action.page_content,
                    tweet_action.metadata["tweet_id"],
                )
            # TODO: Add GIF reply to timeline
            elif tweet_action.metadata["action"] == "gif_reply_to_timeline":
                self.handle_tweet_action(
                    self.gif_reply_to_timeline,
                    tweet_action.page_content,
                    tweet_action.metadata["tweet_id"],
                    tweet_action.metadata["media_id"],
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
        action_function(*args)

    def reply_to_timeline(self, tweet_text, tweet_id):
        print("Tweet Replied:", tweet_text)
        return self.client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet_id)

    def gif_reply_to_timeline(self, tweet_text, tweet_id, media_id):
        print("Tweet Replied with GIF:", tweet_text, media_id)
        return self.client.create_tweet(
            text=tweet_text, in_reply_to_tweet_id=tweet_id, media_ids=media_id
        )

    def quote_tweet(self, tweet_text, tweet_id):
        print("Tweet Quoted:", tweet_text)
        return self.client.create_tweet(text=tweet_text, quote_tweet_id=tweet_id)

    def post_tweet(self, tweet_text):
        print("Tweet Posted:", tweet_text)
        return self.client.create_tweet(text=tweet_text)
