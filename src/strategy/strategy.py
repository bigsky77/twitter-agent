from .strategies.basic.basic import BasicTwitterStrategy
from .strategies.advanced.advanced import AdvancedTwitterStrategy

# Map strategy names to classes
STRATEGY_MAP = {
    'basic': BasicTwitterStrategy,
    'advanced': AdvancedTwitterStrategy,
    # Add additional strategies here as needed
}

def create_strategy(agent_id, llm, params, strategy_name):
    # Fetch the appropriate strategy class from the map
    StrategyClass = STRATEGY_MAP.get(strategy_name)

    # If we didn't find a matching strategy, raise an error
    if StrategyClass is None:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    # Instantiate and return an instance of the strategy
    return StrategyClass(agent_id, llm, params)
