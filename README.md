# Twitter-Agent

This Python script is an example of an autonomous AI-powered agent for interacting with the Twitter API. The system uses OpenAI and LangChain to tweet, send direct messages, and reply to mentions. Unlike a traditional Twitter Bot, this agent is designed to dynamically interact with the environment.

## Capabilities

 The Twitter-Agent currently has the following capabilities: 

    Retweet: ✅ 
    Tweet: ✅ 🤖
    Reply to mentions: ✅ 🤖
    Reply to replies: ✅ 🤖
    Reply to direct messages: ✅ 🤖
    Like tweets: ✅ 
    Follow users: ✅ 

To use the script, you will need to follow these steps:

### Installation

1. Clone the repository via `git clone https://github.com/bigsky77/khafre.git` and `cd` into the cloned repository.
2. Start a Python virtual environment `python -m venv venv` and then `source activate venv/bin/activate` (optional but HIGHLY recommended).
3. Install the required packages: `pip install -r requirements.txt`.
4. Copy the .env.example file to .env: `cp .env.example .env`. This is where you will set the ENV variables.
5. Set your OpenAI, and Twitter API keys in your new .env file.

### Execution

1. First, run `python main.py` to authenticate your Twitter account using OAUTH2.
2. Once authenticated, run `python twitter_agi.py` to start the AGI.

### Deployment

In order to deploy this agent, sign up for a [Render](https://render.com/) or another hosting site, and connect to your GitHub repository.

### References

- [Creating a Twitter Bot with Python, OAuth 2.0, and v2 of the Twitter API](https://developer.twitter.com/en/docs/tutorials/creating-a-twitter-bot-with-python--oauth-2-0--and-v2-of-the-twi)
- [LangChain Use Cases: Autonomous Agents](https://python.langchain.com/en/latest/use_cases/autonomous_agents.html)
- [BabyAGI on GitHub](https://github.com/yoheinakajima/babyagi)
- [Tweepy API](https://docs.tweepy.org/en/stable/api.html)
