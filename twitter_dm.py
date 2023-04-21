import os
import tweepy
import random
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
    template="You are a message reply agent.  You are replying to a message that says: {input_text}.  Make sure the reply is under 140 characters.  Be positive and welcoming.",
)
chain = LLMChain(llm=llm, prompt=prompt)


def get_last_dm_sent_to(user_id):
    sent_dms = api.get_direct_messages()
    for dm in sent_dms:
        if dm.message_create["target"]["recipient_id"] == user_id:
            return dm
    return None


def reply_to_new_direct_messages():
    received_dms = api.get_direct_messages(count=10)
    for dm in received_dms:
        sender_id = dm.message_create["sender_id"]
        if sender_id != api.me().id:  # Make sure it's not a message sent by yourself
            last_dm_sent = get_last_dm_sent_to(sender_id)
            if not last_dm_sent or last_dm_sent.id < dm.id:
                try:
                    print(f"Replying to DM from {sender_id}")
                    input_text = dm.message_create['message_data']['text']
                    if random.random() < 0.8:  # Randomly decide to reply or not
                        reply_text = chain.generate(input_text=input_text)
                        api.send_direct_message(sender_id, reply_text)
                except tweepy.TweepError as e:
                    print(f"Error replying to DM from {sender_id}: {e}")

if __name__ == "__main__":
    reply_to_new_direct_messages()
