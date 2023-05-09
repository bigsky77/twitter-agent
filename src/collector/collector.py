from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Sequence, Union
from langchain.docstore.document import Document


class TwitterCollector:
    def __init__(self, client, db, USER_ID):
        self.client = client
        self.db = db
        self.USER_ID = USER_ID

    def get_tweet_info(self, tweet_id):
        return self.client.get_tweet(tweet_id)

    # upload timeline to database
    def upload_timeline(self, count) -> List[Document]:
        results: List[Document] = []
        tweets = self.client.get_home_timeline(max_results=count)
        user = "lil_bigsky_agi"
        docs = self._format_tweets(tweets, user)
        results.extend(docs)
        print(results)
        self.db.add_documents(results)
        return results

    def _format_tweets(
        self, tweets: List[Dict[str, Any]], user_info: dict
    ) -> Iterable[Document]:
        """Format tweets into a string."""
        for tweet in tweets.data:
            metadata = {
                "tweet_id": tweet.id,
                "current": "true",
            }
            yield Document(
                page_content=tweet.text,
                metadata=metadata,
            )

    # retrieve last uploaded timeline
    def load_timeline(self):
        return self.db.search("tweet_id")
