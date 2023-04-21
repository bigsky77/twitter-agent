# Twitter-Agent

This is a prototype of a Twitter specific AGI.  The agent plans, researchs, and posts tweets.  The agent can also respond to direct messages, and reply to other users.  

# How to Use<a name="how-to-use"></a>
To use the script, you will need to follow these steps:

### Install

1. Clone the repository via `git clone https://github.com/bigsky77/khafre.git` and `cd` into the cloned repository.
2. Start a python virtual environment `python -m venv venv` and then `source activate venv/bin/activate` (optional but HIGHLY recommended)
3. Install the required packages: `pip install -r requirements.txt`
4. Copy the .env.example file to .env: `cp .env.example .env`. This is where you will set the ENV variables.
5. Set your OpenAI, and Twitter API keys in your new .env file

### Run

1. First run `python main.py` to authenticate your twitter account using OAUTH2
2. Once authenticated run `python twitter_agi.py` to start the AGI 

### Deploy

In order to deploy this agent sign up for a https://render.com/ or another hosting site, and connect to your github repository.
