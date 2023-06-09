import yaml
import time
from typing import Any, Dict, Iterable, List
from langchain.docstore.document import Document
import datetime

class Report:
    def __init__(self, agent_name, agent_id, followers_count, average_ratio):
        self.date = datetime.datetime.now()
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.followers_count = followers_count
        self.average_ratio = average_ratio

    def __str__(self):
        return (
            f"Date: {self.date}\n"
            f"Agent Name: {self.agent_name}\n"
            f"Agent ID: {self.agent_id}\n"
            f"Follower Count: {self.followers_count}\n"
            f"Average Likes to Followers Ratio: {self.average_ratio}"
        )


class TwitterState:
    def __init__(
        self,
        list_tweets: List[Document],
    ):
        self.list_tweets = list_tweets

class TwitterCollector:
    def __init__(self, USER_ID, client, params):
        self.USER_ID = USER_ID
        self.client = client
        self.params = params

    async def run(self):
        list_tweets = await self.retrieve_weighted_lists(10)
        twitter_state = TwitterState(
            list_tweets
        )
        return twitter_state

    async def fetch_status(self):
        followers = self.retrieve_followers()
        print("Follower Count:", len(followers))

    def generate_report(self, tweet_ids: List[int]):
        agent = self.client.get_me()
        followers_count = len(self.retrieve_followers())
        likes_to_followers_ratios = []

        for tweet_id in tweet_ids:
            likes_response = self.client.get_liking_users(id=tweet_id)
            likes_count = likes_response.meta['result_count']

            ratio = likes_count / followers_count if followers_count else 0  # Avoid division by zero.
            likes_to_followers_ratios.append(ratio)
            # TODO: fix rate limit
            time.sleep(1)

        average_ratio = sum(likes_to_followers_ratios) / len(likes_to_followers_ratios) if likes_to_followers_ratios else 0  # Avoid division by zero.
        report = Report(agent.data.name, agent.data.id, followers_count, average_ratio)
        return report

    async def get_tweet_info(self, tweet_id: int):
        return self.client.get_tweet(tweet_id)

    # convert to vector storable document
    async def retrieve_timeline(self, count) -> List[Document]:
        results: List[Document] = []
        tweets = self.client.get_home_timeline(max_results=count)
        docs = self._format_tweets(tweets)
        results.extend(docs)
        return results

    async def retrieve_list(self, max_results: int, list_id: int) -> List[Document]:
        results: List[Document] = []
        tweets = self.client.get_list_tweets(id=list_id, max_results=max_results)
        docs = self._format_tweets(tweets)
        results.extend(docs)
        return results

    def retrieve_followers(self) -> List[Document]:
        results: List[Document] = []
        followers = self.client.get_users_followers(id=self.USER_ID)
        docs = self._format_followers(followers)
        results.extend(docs)
        return results

    async def retrieve_weighted_lists(
        self, max_results: int
    ) -> List[Document]:
        lists_response = self.client.get_owned_lists(id=self.USER_ID)
        lists = lists_response.data

        results: List[Document] = []
        for list_data in lists:
            list_id = list_data["id"]
            tweets = self.client.get_list_tweets(id=list_id, max_results=max_results)
            docs = self._format_tweets(tweets)
            results.extend(docs)

        return results

    async def retrieve_dms(self):
        res = self.client.get_direct_message_events(max_results=3)
        return res

    def _format_tweets(self, tweets: List[Dict[str, Any]]) -> Iterable[Document]:
        """Format tweets into a string."""
        for tweet in tweets.data:
            metadata = {
                "tweet_id": tweet.id,
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
