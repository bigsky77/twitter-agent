import base64
import hashlib
import os
import re
import json
import time
import requests
import redis
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session
from dotenv import load_dotenv

load_dotenv()

r = redis.from_url(os.getenv("REDIS_URL", ""))

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(50)

# Twitter app credentials
client_id = os.getenv("CLIENT_ID", "")
client_secret = os.getenv("CLIENT_SECRET", "")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
redirect_uri = os.getenv("REDIRECT_URI", "")

# set scope
scope = [
    "tweet.read",
    "users.read",
    "tweet.write",
    "offline.access",
    "dm.read",
    "dm.write",
]

# generate code verifier
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

# generate code challenge
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")


# generate token
def make_token():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

@app.route("/")
def demo():
    global twitter
    twitter = make_token()
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
    )
    st_token = '"{}"'.format(token)
    j_token = json.loads(st_token)
    r.set("token", j_token)
    tweets = "placeholder"
    return tweets
    # response = post_tweet_thread(tweets, token)
    # return response


if __name__ == "__main__":
    app.run()
