import os
import json
import redis
import tweepy
from dotenv import load_dotenv
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Sequence, Union

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET", "")

def fetch_client():
    # Set up OAuth 1.0a authentication
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    # Initialize a Tweepy client instance
    return client

