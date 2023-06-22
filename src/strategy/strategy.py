import random
import re
from langchain.docstore.document import Document
from langchain.chains import LLMChain
from typing import List
from .media.gif_reply import generate_gif_response
from .prompt import reply_prompt, tweet_prompt

class TwitterStrategy:
    def __init__(self, llm, twitter_client, vectorstore):
        self.llm = llm
        self.vectorstore = vectorstore
        self.twitter_client = twitter_client
        self.action_mapping = {
            "like_timeline_tweets": self.like_tweet,
            "retweet_timeline_tweets": self.retweet_tweet,
            "reply_to_timeline": self.reply_to_timeline,
            "gif_reply_to_timeline": self.gif_reply_to_timeline,
            "quote_tweet": self.quote_tweet,
            "post_tweet": self.post_tweet,
            "none": self.none_action,
        }
        self.probabilities = [
            0.02,  # like_timeline_tweets
            0.01,  # retweet_timeline_tweets
            0.02,  # reply_to_timeline
            0.02,  # gif_reply_to_timeline
            0.01,  # quote_tweet
            0.02,  # post_tweet
            0.90,  # none
        ]

    def run(self, twitterstate):
        print("Running strategy...")
        print("Twitter state: ", twitterstate)
        results = self.process_and_action_tweets(twitterstate)
        return results

    def weighted_random_choice(self, actions, probabilities):
        return random.choices(actions, probabilities)[0]

    def process_and_action_tweets(self, tweets: List[Document]):
        actions = [
            "like_timeline_tweets",
            "retweet_timeline_tweets",
            "reply_to_timeline",
            "gif_reply_to_timeline",
            "quote_tweet",
            "post_tweet",
            "none",
        ]

        results: List[Document] = []
        for tweet in tweets:
            action = self.weighted_random_choice(actions, self.probabilities)
            method = self.action_mapping.get(action)
            if method:
                doc = method(tweet)
                results.append(doc)

        return results

    def post_tweet(self, tweet: Document):
        response = self.generate_tweet(tweet.page_content)
        metadata = {"action": "post_tweet"}
        return Document(page_content=response, metadata=metadata)

    def generate_tweet(self, input_text):
        print("Generating tweet...")
        prompt = tweet_prompt
        tweet_chain = LLMChain(llm=self.llm, prompt=prompt)
        response = tweet_chain.run(input_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r"^[\n\.\"]*", "", response)
        response = re.sub(r"[\n\.\"]*$", "", response)

        _len_check = self._check_length(response)

        if _len_check is False:
            self.generate_tweet(input_text)

        print(f"Generated tweet: {response}")
        return response

    def reply_to_timeline(self, tweet: Document):
        response = self.generate_response(tweet.page_content)
        metadata = {
            "tweet_id": tweet.metadata["tweet_id"],
            "action": "reply_to_timeline",
        }
        return Document(page_content=response, metadata=metadata)

    def gif_reply_to_timeline(self, tweet: Document):
        response = self.generate_response(tweet.page_content)
        print(response)
        gif_id = generate_gif_response(tweet.page_content, self.twitter_client)
        metadata = {
            "tweet_id": tweet.metadata["tweet_id"],
            "media_id": gif_id,
            "action": "gif_reply_to_timeline",
        }
        return Document(page_content=response, metadata=metadata)

    def like_tweet(self, tweet: Document):
        # As like action doesn't generate a response, metadata will be sufficient
        metadata = {
            "tweet_id": tweet.metadata["tweet_id"],
            "action": "like_timeline_tweets",
        }
        return Document(page_content=tweet.page_content, metadata=metadata)

    def retweet_tweet(self, tweet: Document):
        # Similarly for retweet action
        metadata = {
            "tweet_id": tweet.metadata["tweet_id"],
            "action": "retweet_timeline_tweets",
        }
        return Document(page_content=tweet.page_content, metadata=metadata)

    def quote_tweet(self, tweet: Document):
        response = self.generate_response(tweet.page_content)
        metadata = {"tweet_id": tweet.metadata["tweet_id"], "action": "quote_tweet"}
        return Document(page_content=response, metadata=metadata)

    def none_action(self, tweet: Document):
        # No action, just return metadata with action as "none"
        metadata = {"tweet_id": tweet.metadata["tweet_id"], "action": "none"}
        return Document(page_content=tweet.page_content, metadata=metadata)

    def generate_response(self, input_text):
        prompt = reply_prompt
        tweet_chain = LLMChain(llm=self.llm, prompt=prompt)
        response = tweet_chain.run(input_text=input_text)

        # Remove newlines and periods from the beginning and end of the tweet
        response = re.sub(r"^[\n\.\"]*", "", response)
        response = re.sub(r"[\n\.\"]*$", "", response)

        _len_check = self._check_length(response)

        if _len_check is False:
            self.generate_response(input_text)

        print(f"Generated Response: {response}")
        return response

    def _check_length(self, text):
        if len(text) > 140:
            return False
