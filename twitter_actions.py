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

def fetch_token_refreshed():
   return refreshed_token

