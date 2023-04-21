import os
import tweepy
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

api_key = os.getenv("API_KEY", "")
api_secret_key = os.getenv("API_SECRET_KEY", "")
access_token = os.getenv("ACCESS_TOKEN", "")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET", "")

auth = tweepy.OAuth1UserHandler(
    api_key, api_secret_key, access_token, access_token_secret
)

api = tweepy.API(auth)
llm = OpenAI(temperature=0.9)

prompt = PromptTemplate(
    input_variables=["input_text"],
    template="You are a tweet reply agent.  You are replying to a tweet that says: {input_text}.  Make sure the reply is under 140 characters.  Be sarcastic and funny.",
)
chain = LLMChain(llm=llm, prompt=prompt)


def generate_response(input_text):
    # Use the input_text to generate a response using your Language Model
    # For example, using OpenAI's GPT-3
    response = chain.run(input_text=input_text)
    return response


def reply_to_replies():
    my_tweets = api.user_timeline(count=10)

    for tweet in my_tweets:
        print(tweet.user.screen_name, tweet.text)
        # Search for tweets that are a reply to your tweet and mention your screen name
        query = f"to:{tweet.user.screen_name} filter:replies"
        replies = tweepy.Cursor(
            api.search_tweets, q=query, tweet_mode="extended"
        ).items()

        for reply in replies:
            if reply.in_reply_to_status_id == tweet.id:
                user_reply_text = reply.full_text.replace(
                    f"@{tweet.user.screen_name}", ""
                ).strip()
                response_text = generate_response(user_reply_text)
                api.update_status(
                    status=f"@{reply.user.screen_name} {response_text}",
                    in_reply_to_status_id=reply.id,
                    auto_populate_reply_metadata=True,
                )

def reply_to_mentions():
    mentions = api.mentions_timeline(tweet_mode='extended')

    for mention in mentions:
        # Check if the tweet has already been replied to
        if not mention.favorited:
            print(f'Replying to {mention.user.screen_name}...')
            user_mention_text = mention.full_text.replace(
                f"@{mention.user.screen_name}", ""
            ).strip()
            response_text = generate_response(user_mention_text)
            api.update_status(
                status=f"@{mention.user.screen_name} {response_text}",
                in_reply_to_status_id=mention.id,
                auto_populate_reply_metadata=True,
            )
            api.create_favorite(mention.id)  # Mark the tweet as "favorited"


if __name__ == "__main__":
    reply_to_replies()
    reply_to_mentions()
