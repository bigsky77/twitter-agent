from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Sequence, Union
from langchain.docstore.document import Document

class TwitterCollector:
    def __init__(self, client, db):
        self.client = client
        self.db = db

    def get_tweet_info(self, tweet_id):
        return self.client.get_tweet(tweet_id)

    def load(self, count) -> List[Document]:
            results: List[Document] = []
            tweets = self.client.get_home_timeline(max_results=count)
            user = "lil_bigsky_agi"
            docs = self._format_tweets(tweets, user)
            results.extend(docs)
            print(results)
            return results

    def _format_tweets(
        self, tweets: List[Dict[str, Any]], user_info: dict
    ) -> Iterable[Document]:
        """Format tweets into a string."""
        for tweet in tweets.data:
            metadata = {
                "user_info": user_info,
            }
            yield Document(
                page_content=tweet.text,
                metadata=metadata,
            )
