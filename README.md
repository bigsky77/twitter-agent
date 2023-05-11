# Twitter-Agent 🐣

This Python script is an example of an autonomous AI-powered agent for interacting with the Twitter API. The system uses OpenAI and LangChain to tweet, send direct messages, and reply to mentions. Unlike a traditional Twitter Bot, this agent is designed to dynamically interact with the environment.  The agent uses a variety of tools (such as searching google and wikipedia). 

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

Run `python src/main.py` once your .env is fully configured.  Note, you will need to be a subscriber to the Twitter Basic API for the Agent to fully function.  If you are using the free tier, the agent will only be able to post Tweets and not interact with the timeline.   

### Deployment

In order to deploy this agent, sign up for a [Render](https://render.com/) or another hosting site, and connect to your GitHub repository.

### Contribute

We love contributions and seek to make contribution as easy as possible.  Our goal with this project is to make the worlds-best AGI Twitter agent.  If that sounds interesting to you, please reach out!

### References

- [Creating a Twitter Bot with Python, OAuth 2.0, and v2 of the Twitter API](https://developer.twitter.com/en/docs/tutorials/creating-a-twitter-bot-with-python--oauth-2-0--and-v2-of-the-twi)
- [LangChain Use Cases: Autonomous Agents](https://python.langchain.com/en/latest/use_cases/autonomous_agents.html)
- [BabyAGI on GitHub](https://github.com/yoheinakajima/babyagi)
- [Tweepy API](https://docs.tweepy.org/en/stable/api.html)
- [Strange Loops](https://en.wikipedia.org/wiki/Strange_loop)
- [How to run your own LLM](https://blog.rfox.eu/en/Programming/How_to_run_your_own_LLM_GPT.html)
- [Generative Simulacra](https://arxiv.org/abs/2304.03442)
