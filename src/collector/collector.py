import yaml
from typing import Any, Dict, Iterable, List
from langchain.docstore.document import Document

class TwitterCollector:
    def __init__(self, client, USER_ID, params):
        self.client = client
        self.USER_ID = USER_ID
        self.params = params

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

    def retrieve_weighted_lists(self, max_results: int, list_ids: List[int]) -> List[Document]:
        results: List[Document] = []
        for list_id in list_ids:
            tweets = self.client.get_list_tweets(id=list_id, max_results=max_results)
            docs = self._format_tweets(tweets)
            results.extend(docs)
        print(results)
        return results

    def retrieve_dms(self):
        res = self.client.get_direct_message_events(max_results=10)
        print(res)

    def run(self):
        pass

    def _format_tweets(
        self, tweets: List[Dict[str, Any]]
    ) -> Iterable[Document]:
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
