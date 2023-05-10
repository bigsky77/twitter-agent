import random
from langchain.docstore.document import Document
from typing import Any, Dict, Iterable, List


class TwitterStrategy:
    def __init__(self, client, llm, params):
        self.client = client
        self.llm = llm
        self.params = params

    def analyze_tweets(self, timeline_tweets):
        return timeline_tweets

    def weighted_random_choice(actions, probabilities):
        return random.choices(actions, probabilities)[0]

    def select_action(self, tweets: List[Dict[str, Any]]):
        actions = [
            "quote_tweet",
            "reply_to_timeline",
            "like_timeline_tweets",
            "retweet_timeline_tweets",
            "none",
        ]

        probabilities = [
            0.1,  # quote_tweet
            0.2,  # reply_to_timeline
            0.2,  # like_timeline_tweets
            0.1,  # retweet_timeline_tweets
            0.4,  # none
        ]

        for tweet in tweets:
            # Select an action based on the probabilities
            action = self.weighted_random_choice(actions, probabilities)
            self._update_tweet(tweet, action)

        return tweets

    def _update_tweet(self, tweet: [Dict[str, Any]], action: str) -> Iterable[Document]:
        """Format tweets into a string."""
        metadata = {
            "tweet_id": tweet.id,
            "action": action,
        }
        yield Document(
            page_content=tweet.text,
            metadata=metadata,
        )
