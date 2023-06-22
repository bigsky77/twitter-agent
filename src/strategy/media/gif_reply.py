import os
import re
import yaml
import tweepy
import random
import pytz
from dotenv import load_dotenv
from datetime import datetime, timedelta
import urllib.request
import json
import requests
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
giphy_api_key = os.getenv("GIPHY_API", "")

llm = OpenAI(temperature=0.9)
gif_prompt = PromptTemplate(
    input_variables=["input_text"],
    template=("You are a word matching agent."
              "Based on the: {input_text} say three words as a single line like `stallion joy wealth`."
              "Only reply with the three words."
              "If you do not have three words, reply with a random celebrity name."
              "Do not use line breaks, or commas."
              ),
)
gif_chain = LLMChain(llm=llm, prompt=gif_prompt)

reply_prompt = PromptTemplate(
    input_variables=["input_text"],
    template=("You are a tweet agent whose mission is to bring good luck and wealth to everyone."
              "You're goal is to create an awesome tweet about the following topic: {input_text}."
              "Make sure the reply is under 140 characters."
              "Be very positive and encouraging, wish people fortune and good luck, encourage them to pursue their dreams."
              "Use descriptive langauge."
              "Use lots of emojis and metaphors.  Never use hashtags"),
    )
reply_chain = LLMChain(llm=llm, prompt=reply_prompt)


def generate_response(tweet):
    # Generate a response using your LLM agent based on the context of the tweet
    response = reply_chain.run(
        tweet.text
    )  # Replace this with your actual LLM-generated response
    print(f"Responding to {tweet.user.screen_name}: {tweet.text}")
    return response


def modifier(s):
    """
    returns hashtags based on the GIF names from GIPHY
    """
    ms = ""
    for i in range(len(s)):
        if s[i] == "-":
            ms += " "
        else:
            ms += s[i]
    ls = ms.split()
    del ls[-1]
    ls[0] = "#" + ls[0]
    return " #".join(ls)


def gif_download(gif_url):
    """
    Takes the URL of an Image/GIF and downloads it
    """
    gif_data = requests.get(gif_url).content
    with open("image.gif", "wb") as handler:
        handler.write(gif_data)
        handler.close()


def gif_post(gif_url_list, msg, twitter_client):
    v1_api = twitter_client["v1_api"]
    """
    uploads a single random GIF and returns the media_id
    """
    random_index = random.randint(
        0, len(gif_url_list) - 1
    )  # Randomly select an index from the gif_url_list

    try:
        gif_download(gif_url_list[random_index])
        m = modifier(msg[random_index])
        result = v1_api.media_upload("image.gif")
        return result
    except Exception as e:
        print("Error occurred: ", e)


def search_gif(query, twitter_client):
    """
    Searches for GIFs based on a query
    """
    words = re.findall(r"\w+", query, re.MULTILINE)
    formatted_query = "+".join(words)
    print("Searching for GIFs based on query: ", formatted_query)
    giphy_url = (
        "https://api.giphy.com/v1/gifs/search?api_key="
        + giphy_api_key
        + "&q="
        + formatted_query
        + "&limit=20&offset=0&rating=r&lang=en"
    )

    with urllib.request.urlopen(giphy_url) as response:
        html = response.read()

    h = html.decode("utf-8")
    gif_info = json.loads(h)
    gif_data = gif_info["data"]
    gif_urls = []
    slugs = []

    for i in range(len(gif_data)):
        gif = gif_data[i]["images"]["downsized"]["url"]
        slug = gif_data[i]["slug"]
        gif_urls.append(gif)
        slugs.append(slug)

    media_id = gif_post(gif_urls, slugs, twitter_client)
    return media_id


def generate_gif_response(text, twitter_client):
    gif_response = gif_chain.run(text)

    res = search_gif(gif_response, twitter_client)
    return [res.media_id_string]
