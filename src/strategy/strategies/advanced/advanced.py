from ...base_strategy import TwitterStrategy

class AdvancedTwitterStrategy(TwitterStrategy):
    def __init__(self, agent_id, llm, params):
        super().__init__(agent_id, llm, params)
