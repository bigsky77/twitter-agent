import random
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

strategy_prompt = PromptTemplate(
    input_variables=["input_text", "action"],
    template="You a decision agent.  Based on the: {input_text} and the {action} return a score between 0 and 1. The higher the score the more likely you are to take the action. Only return a score.  Your criteria is the following.  For like you should do this for generic tweets.  For reply you should do this engaging or provactive tweets that makes a statement",
)

class TwitterStrategy:
    def __init__(self, client, llm, params):
        self.client = client
        self.llm = llm
        self.params = params

    def analyze_tweets(self, timeline_tweets):
        strategy_chain = LLMChain(llm=self.llm, prompt=strategy_prompt)
        actions = []

        for tweet_doc in timeline_tweets:
            tweet_content = tweet_doc.page_content
            tweet_id = tweet_doc.metadata['tweet_id']

            # Use LLM to generate a score for each action
            response_score = strategy_chain.run(input_text=tweet_content, action="respond")
            like_score = strategy_chain.run(input_text=tweet_content, action="like")
            retweet_score = strategy_chain.run(input_text=tweet_content, action="retweet")

            # Determine which action to take based on the LLM scores and probabilities
            action = self.choose_action(response_score, like_score, retweet_score)

            if action:
                actions.append((action, tweet_id))

        return actions

    def choose_action(self, response_score, like_score, retweet_score):
        action_probabilities = {
            "respond": self.params["response_probability"],
            "like": self.params["like_probability"],
            "retweet": self.params["retweet_probability"]
        }

        # Normalize probabilities
        total = sum(action_probabilities.values())
        normalized_probabilities = {k: v / total for k, v in action_probabilities.items()}

        action_scores = {
            "respond": response_score,
            "like": like_score,
            "retweet": retweet_score
        }

        # Calculate weighted scores
        weighted_scores = {k: v * action_scores[k] for k, v in normalized_probabilities.items()}

        # Choose the action with the highest weighted score
        chosen_action = max(weighted_scores, key=weighted_scores.get)

        # Apply a random threshold to add some randomness to the chosen actions
        if random.random() < self.params["action_threshold"]:
            return chosen_action

        return None

