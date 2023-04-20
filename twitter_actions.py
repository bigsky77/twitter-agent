import os, yaml, json
import main
from dotenv import load_dotenv
import requests

load_dotenv()

# Get the Twitter API keys from the environment
twitter = main.make_token()
client_id = os.getenv("CLIENT_ID", "")
client_secret = os.getenv("CLIENT_SECRET", "")
token_url = "https://api.twitter.com/2/oauth2/token"

# Save the bearer token
t = main.r.get("token")
bb_t = t.decode("utf8").replace("'", '"')
data = json.loads(bb_t)

refreshed_token = twitter.refresh_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    refresh_token=data["refresh_token"],
)

# Save the refreshed token
st_refreshed_token = '"{}"'.format(refreshed_token)
j_refreshed_token = json.loads(st_refreshed_token)
main.r.set("token", j_refreshed_token)


def post_tweet(payload, in_reply_to=None):
    print("Tweeting!")

    if in_reply_to is not None:
        payload["reply"] = {"in_reply_to_tweet_id": in_reply_to}

    return requests.request(
        "POST",
        "https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(refreshed_token["access_token"]),
            "Content-Type": "application/json",
        },
    )


def post_tweet_thread(tweets):
    previous_tweet_id = None

    for tweet_text in tweets:
        payload = {
            "text": tweet_text,
        }

        response = post_tweet(payload, refreshed_token, in_reply_to=previous_tweet_id)
        response_json = response.json()

        if response.status_code == 201:
            previous_tweet_id = response_json["data"]["id"]

            time.sleep(15)
        else:
            print(f"Error posting tweet: {response_json}")
            break
