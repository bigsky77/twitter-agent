#  🐣 Twitter-Agent 

Twitter-Agent is a python framework for concurently running multiple AI-powered Agents on Twitter.  Each agent uses Langchain, Tweepy, and BabyAGI to interact with the timeline, post tweets, and engage with other users. This engine is designed as an initial propotype for managing a massive number of AI-agents at scale. 

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

#### Initial Set-Up
1. Clone the repository via `git clone https://github.com/bigsky77/twitter-agent.git` 
2.  Change to the twitter-agent directory `cd twitter-agent` 
3. Create a Python virtual environment `python -m venv venv` and 
4. Activate virtual env `source activate venv/bin/activate` (optional but HIGHLY recommended).
5. Install the required packages: `pip install -r requirements.txt`.

#### Env Set-Up
4. Copy the .env.example file to .env: `cp .env.example .env`. This is where you will set the ENV variables.
5. Copy the `cp example_tokens.yml tokens.yml` This is where you will input each Agents Access Token and Secret
6. Set your OpenAI, and Twitter API keys in your new .env file.

#### OAUTH2 Setup
1. Run `python src/auth.py` to retrieve you Access Token and Access Token Secret
2.  This will output an auth url in the terminal.  Paste this url into your browser and authorize the app
3. If the redirect does not give you a pin number and you get a no connection error paste the last string in the new url into the PIN area
8. Paste these values in the `tokens.yml` file alongside the Agent name and strategy to run

### Execution

Run `python src/main.py --run-engine` once your .env is fully configured.  Note, you will need to be a subscriber to the Twitter Basic API for the Agent to fully function.  If you are using the free tier, the agent will only be able to post Tweets and not interact with the timeline.   

### Deployment

In order to deploy this agent, sign up for a [Render](https://render.com/) or another hosting site, and connect to your GitHub repository.

### Contribute

We love contributions and seek to make contribution as easy as possible.  Our goal with this project is to make the worlds-best AGI Twitter agent.  If that sounds interesting to you, please reach out!

## Currently Deployed Agents

 - [lil bigsky agi](https://twitter.com/lil_bigsky_agi)
 - [lil remilio agi](https://twitter.com/lil_remilio_agi)
 - [luna](https://twitter.com/lil_luna_agi)

| Agent Name     | Tweets Made | Followers  | Total Likes  | AVG Like/Follower Ratio |
| -------------- | ----------- | ---------- | ------------ | ------------            | 
| lil bigsky agi | 100         | 50         | 120          | 2023-06-01              |
| lil remilio agi| 120         | 65         | 200          | 2023-06-02              |
| luna           | 90          | 70         | 150          | 2023-06-03              |

### References

- [Creating a Twitter Bot with Python, OAuth 2.0, and v2 of the Twitter API](https://developer.twitter.com/en/docs/tutorials/creating-a-twitter-bot-with-python--oauth-2-0--and-v2-of-the-twi)
- [LangChain Use Cases: Autonomous Agents](https://python.langchain.com/en/latest/use_cases/autonomous_agents.html)
- [BabyAGI on GitHub](https://github.com/yoheinakajima/babyagi)
- [Tweepy API](https://docs.tweepy.org/en/stable/api.html)
- [Strange Loops](https://en.wikipedia.org/wiki/Strange_loop)
- [How to run your own LLM](https://blog.rfox.eu/en/Programming/How_to_run_your_own_LLM_GPT.html)
- [Generative Simulacra](https://arxiv.org/abs/2304.03442)
- [Rewarding Chatbots with Real-World Engagement](https://arxiv.org/abs/2303.06135)
