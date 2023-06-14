import yaml
import json
import time
from typing import Any, Dict, Iterable, List
from langchain.docstore.document import Document
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import CharacterTextSplitter
from pathlib import Path
from pprint import pprint

class TwitterState:
    def __init__(
        self,
        list_tweets: List[Document],
    ):
        self.list_tweets = list_tweets

class TwitterCollector:
    def __init__(self, USER_ID, client, vectorstore, weaviate_client):
        self.USER_ID = USER_ID
        self.client = client
        self.vectorstore = vectorstore
        self.weaviate_client = weaviate_client

    async def run(self):
        list_tweets = await self.retrieve_weighted_lists(1)

        pprint(list_tweets)

        with self.weaviate_client.batch(
            batch_size=1
        ) as batch:
            # Batch import all Questions
            for tweet in list_tweets:
                properties = {
                    "tweet": tweet.page_content,
                    "tweet_id": str(tweet.metadata["tweet_id"]),
                }

                self.weaviate_client.batch.add_data_object(
                    properties,
                    "Tweets",
                )

        twitter_state = TwitterState(
            list_tweets
        )

        return twitter_state.list_tweets

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

    def run_test(self):
        response = (
            self.weaviate_client.query
            .get("Tweets", ["tweet", "tweet_id"])
            .with_limit(2)
            .do()
        )

        results: List[Document] = []
        for tweet in response['data']['Get']['Tweets']:
            docs = self._format_tweet(tweet)
            results.extend(docs)

        return results

    def _format_tweet(self, tweet) -> Iterable[Document]:
        """Format tweets into a string."""
        metadata = {
            "tweet_id": tweet['tweet_id'],
            "action": "none",
        }
        yield Document(
            page_content=tweet['tweet'],
            metadata=metadata,
        )

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
