#  🐣 Twitter-Agent 

Twitter-Agent is a python framework for concurently running multiple AI-powered Agents on Twitter.  Each agent uses Langchain, Tweepy, and BabyAGI to interact with the timeline, post tweets, and engage with other users. 

##  What is this?

Large-Language Models(LLMS) promise to transform how we work, the content we create, and many aspects of our lives.  Today, we think of these models as working in isolation.  If you're reading this, you probably knows the feeling of typing in a prompt  and recieving and exciting or unexpected answer.  However,  the real unlock comes when LLMs begin to interact with both with each-other and with the outside world. 

We see a future where the internet is populated by a vast number of indipendent actors, both human and machine.  This engine is designed as an initial propotype for managing a massive number of AI-agents at scale.

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

## Currently Deployed Agents

 - [lil bigsky agi](https://twitter.com/lil_bigsky_agi)
 - [lil remilio agi](https://twitter.com/lil_remilio_agi)
 - [luna](https://twitter.com/lil_luna_agi)

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
- [Rewarding Chatbots with Real-World Engagement](https://arxiv.org/abs/2303.06135)
