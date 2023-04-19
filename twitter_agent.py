import os, yaml, json
import main
from dotenv import load_dotenv
#from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.requests import RequestsWrapper
from langchain.llms.openai import OpenAI
#from langchain.agents.agent_toolkits.openapi import planner
from flask import Flask, request, redirect, session

load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(50)


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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

#with open("./twitter_openapi.yaml") as f:
#    raw_twitter_api_spec = yaml.load(f, Loader=yaml.Loader)
#twitter_api_spec = reduce_openapi_spec(raw_twitter_api_spec)
#
#headers = {
#    "Authorization": "Bearer {}".format(refreshed_token["access_token"]),
#    "Content-Type": "application/json",
#}
#requests_wrapper = RequestsWrapper(headers=headers)
#
#llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.45)
#twitter_agent = planner.create_openapi_agent(twitter_api_spec, requests_wrapper, llm)
#
#user_query = "Send a message to user @BigSky_7 wishing them an awesome day!"
#
#twitter_agent.run(user_query)

if __name__ == "__main__":
    app.run()
