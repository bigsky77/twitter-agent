import random
from langchain.docstore.document import Document
from typing import Any, Dict, Iterable, List

class TwitterStrategy:
    def __init__(self, agent_id, llm, params):
        self.agent_id = agent_id
        self.llm = llm
        self.params = params

    def ingest(self, twitterstate):
        results = self.select_action(twitterstate.list_tweets)
        return results

    def weighted_random_choice(self, actions, probabilities):
        return random.choices(actions, probabilities)[0]

    def select_action(self, tweets: list[dict[str, any]]):
        actions = [
            "post_tweet",
            "quote_tweet",
            "reply_to_timeline",
            "like_timeline_tweets",
            "retweet_timeline_tweets",
            "none",
        ]

        probabilities = [
            0.05,  # post_tweet
            0.05,  # quote_tweet
            0.10,  # reply_to_timeline
            0.10,  # like_timeline_tweets
            0.05,  # retweet_timeline_tweets
            0.65,  # none
        ]


        results: list[Document] = []
        for tweet in tweets:
            # select an action based on the probabilities
            action = self.weighted_random_choice(actions, probabilities)
            docs = self._update_tweet(tweet, action)
            results.extend(docs)

        return results

    def _update_tweet(self, tweet: [dict[str, any]], action: str) -> Iterable[Document]:
        """format tweets into a string."""
        metadata = {
            "tweet_id": tweet.metadata["tweet_id"],
            "action": action,
        }
        yield Document(
            page_content=tweet.page_content,
            metadata=metadata,
        )
