from typing import Any, Dict, Iterable, List
from langchain.docstore.document import Document
from pprint import pprint


class TwitterState:
    def __init__(
        self,
        list_tweets: List[Document],
    ):
        self.list_tweets = list_tweets


class TwitterCollector:
    def __init__(self, AGENT_ID, client, vectorstore, weaviate_client):
        self.agent_id = AGENT_ID
        self.client = client
        self.vectorstore = vectorstore
        self.weaviate_client = weaviate_client

    async def ingest(self):
        return await self.ingest_weighted_lists(2)

    async def run(self) -> TwitterState:
        response = (
            self.weaviate_client.query.get("Tweets", ["tweet", "tweet_id", "agent_id"])
            .with_limit(5)
            .do()
        )

        pprint(response)

        results: List[Document] = []
        for tweet in response["data"]["Get"]["Tweets"]:
            docs = self._format_tweet(tweet)
            results.extend(docs)

        return results


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
        followers = self.client.get_users_followers(id=self.agent_id)
        docs = self._format_followers(followers)
        results.extend(docs)
        return results

    async def ingest_weighted_lists(self, max_results: int):
        lists_response = self.client.get_owned_lists(id=self.agent_id)
        lists = lists_response.data

        for list_data in lists:
            list_id = list_data["id"]
            tweets = self.client.get_list_tweets(id=list_id, max_results=max_results)
            with self.weaviate_client.batch(batch_size=4) as batch:
                # Batch import all Questions
                print(f"Importing {len(tweets.data)} tweets from list {list_id}")
                for tweet in tweets.data:
                    print("Tweet Content:", tweet.text)
                    properties = {
                        "tweet": tweet.text,
                        "tweet_id": str(tweet.id),
                        "agent_id": str(self.agent_id),
                    }

                    self.weaviate_client.batch.add_data_object(
                        properties,
                        "Tweets",
                    )

    def _format_tweet(self, tweet) -> Iterable[Document]:
        """Format tweets into a string."""
        metadata = {
            "tweet_id": tweet["tweet_id"],
            "action": "none",
        }
        yield Document(
            page_content=tweet["tweet"],
            metadata=metadata,
        )

    def _format_tweets(self, tweets: List[Dict[str, Any]]) -> Iterable[Document]:
        """Format tweets into a string."""
        for tweet in tweets:
            metadata = {
                "tweet_id": tweet.id,
                "action": "none",
            }
            yield Document(
                page_content= tweet.text,
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
