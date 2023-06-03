import yaml
import time
from typing import Any, Dict, Iterable, List
from langchain.docstore.document import Document


class TwitterState:
    def __init__(
        self,
        date: int,
        time: int,
        home_timeline: List[Document],
        follower_count: int,
        direct_messages: List[Document],
    ):
        self.date = date
        self.time = time
        self.home_timeline = home_timeline
        self.follower_count = follower_count
        self.direct_messages = direct_messages


class TwitterCollector:
    def __init__(self, client, client_v2, USER_ID, params):
        self.client = client
        self.USER_ID = USER_ID
        self.params = params
        self.client_v2 = client_v2

    def run(self):
        date = time.strftime("%Y-%m-%d")
        time_now = time.strftime("%H:%M:%S")
        home_timeline = self.retrieve_timeline(10)
        follower_count = self.retrieve_followers()
        direct_messages = self.retrieve_dms()
        twitter_state = TwitterState(
            date, time_now, home_timeline, follower_count, direct_messages
        )
        return twitter_state

    def get_tweet_info(self, tweet_id: int):
        return self.client.get_tweet(tweet_id)

    # convert to vector storable document
    def retrieve_timeline(self, count) -> List[Document]:
        results: List[Document] = []
        tweets = self.client.get_home_timeline(max_results=count)
        docs = self._format_tweets(tweets)
        results.extend(docs)
        return results

    def retrieve_list(self, max_results: int, list_id: int) -> List[Document]:
        results: List[Document] = []
        tweets = self.client.get_list_tweets(id=list_id, max_results=max_results)
        docs = self._format_tweets(tweets)
        results.extend(docs)
        return results

    def retrieve_followers(self) -> List[Document]:
        results: List[Document] = []
        followers = self.client_v2.get_users_followers(id=self.USER_ID)
        docs = self._format_followers(followers)
        results.extend(docs)
        return results

    def retrieve_weighted_lists(
        self, max_results: int, list_ids: List[int]
    ) -> List[Document]:
        results: List[Document] = []
        for list_id in list_ids:
            tweets = self.client.get_list_tweets(id=list_id, max_results=max_results)
            docs = self._format_tweets(tweets)
            results.extend(docs)
        return results

    def retrieve_user_tweets(self):
        res = self.client.get_users_tweets(id=self.USER_ID)

    def retrieve_tweet(self):
        res = self.client.get_tweet(id=1664601275944828933)

    def retrieve_dms(self):
        res = self.client.get_direct_message_events(max_results=30)
        return res

    def _format_tweets(self, tweets: List[Dict[str, Any]]) -> Iterable[Document]:
        """Format tweets into a string."""
        for tweet in tweets.data:
            liking_users = self.client_v2.get_liking_users(id=tweet.id)
            metadata = {
                "tweet_id": tweet.id,
                "liking_users": liking_users,
                "action": "none",
            }
            yield Document(
                page_content=tweet.text,
                metadata=metadata,
            )

    def _format_followers(self, followers: List[Dict[str, Any]]) -> Iterable[Document]:
        """Format tweets into a string."""
        for follower in followers.data:
            metadata = {
                "id": follower.id,
                "action": "none",
            }
            yield Document(
                page_content=follower.name,
                metadata=metadata,
            )
