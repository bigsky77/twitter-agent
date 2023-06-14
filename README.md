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

# Twitter-Agent: Installation and Execution Guide
This guide provides step-by-step instructions on how to install and run the `twitter-agent` application.

## Prerequisites
Ensure that you have `python`, `pip`, `git`, and `docker` installed on your machine. The application requires a Python virtual environment and Docker for running Weaviate.

## Installation

### 1. Clone the Repository and Set Up the Environment

#### 1.1. Clone the Repository
Clone the repository into your local machine by running the following command:
```bash
git clone https://github.com/bigsky77/twitter-agent.git && cd twitter-agent

```

#### 1.2. Create a Python Virtual Environment
This step is optional, but highly recommended to avoid package conflicts. Run the following command to create a virtual environment named `venv`:
```bash
python -m venv venv
```
  * [ ] 
#### 1.3. Activate the Virtual Environment

To activate the virtual environment, run the following command:

```bash
source venv/bin/activate
```

#### 1.4. Install the Required Packages

The application dependencies are listed in the requirements.txt file. Install them by running the following command:

``` bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

#### 2.1. Copy the Sample Environment File
Run the following command to copy the contents of .env.example to a new file named .env:

``` bash
cp .env.example .env
```

#### 2.2. Set API Keys
Set your OpenAI and Twitter API keys in your new .env file. Make sure the keys are kept secure and not exposed publicly.

#### 3. Configure Tokens
When running multiple Twitter-Agents,  the engine reads the access tokens from tokens.yml in order to create multiple Tweepy client instances.

#### 3.1. Copy the Sample Tokens File

Run the following command to copy the contents of example_tokens.yml to a new file named tokens.yml:

``` bash
cp example_tokens.yml tokens.yml
```

### 4. OAUTH2 Setup

#### 4.1. Retrieve Access Tokens

Run the following script to get your Access Token and Access Token Secret:

``` bash
python src/utils/auth.py
```

This will output an authorization URL in the terminal. Paste this URL into your browser to authorize the application. If the redirect does not provide a pin number, and you encounter a "no connection" error, paste the last string from the new URL into the PIN area.

#### 4.2. Update Tokens File

Paste the Access Token and Access Token Secret in the tokens.yml file alongside the agent name and strategy.

## Execution

#### 1. Start Weaviate

Weaviate is used to cache tweets. Before running the main script, ensure Weaviate is up and running. This can be achieved by starting a Docker container for Weaviate in the project directory:

``` bash
sudo docker-compose up -d
```

#### 2. Run the Agent
Now that your .env file is fully configured, run the agent with the following command:

``` bash
python src/main.py --run-engine

```

#### 3. Test the Agent
You can test your agent configuration by running.  This will run a strategy but not actually collect any tweets or make any posts.  Note:  You will have had to run the engine at least once for this to work.

``` bash
python src/main.py --run-engine --test
```

Note: You will need to be a subscriber to the Twitter Basic API for the agent to fully function. If you are using the free tier, the agent will only be able to post Tweets and will not interact with the timeline.

That's it! You have now successfully installed and set up the twitter-agent. Happy tweeting!

### Contribute

We love contributions and seek to make contribution as easy as possible.  Our goal with this project is to make the worlds-best AGI Twitter agent.  If that sounds interesting to you, please reach out!

## Currently Deployed Agents

If you deploy a custom agent using this framework please create a pull-request to add it to the leaderboard!

Note these are all initial prototypes!

 - [lil bigsky agi](https://twitter.com/lil_bigsky_agi)
 - [lil remilio agi](https://twitter.com/lil_remilio_agi)
 - [luna](https://twitter.com/lil_luna_agi)

### References

- [Creating a Twitter Bot with Python, OAuth 2.0, and v2 of the Twitter API](https://developer.twitter.com/en/docs/tutorials/creating-a-twitter-bot-with-python--oauth-2-0--and-v2-of-the-twi)
- [LangChain Use Cases: Autonomous Agents](https://python.langchain.com/en/latest/use_cases/autonomous_agents.html)
- [BabyAGI on GitHub](https://github.com/yoheinakajima/babyagi)
- [Tweepy API](https://docs.tweepy.org/en/stable/api.html)
- [Strange Loops](https://en.wikipedia.org/wiki/Strange_loop)
- [How to run your own LLM](https://blog.rfox.eu/en/Programming/How_to_run_your_own_LLM_GPT.html)
- [Generative Simulacra](https://arxiv.org/abs/2304.03442)
- [Rewarding Chatbots with Real-World Engagement](https://arxiv.org/abs/2303.06135)
- [Artimis MEV Framework](https://github.com/paradigmxyz/artemis)
