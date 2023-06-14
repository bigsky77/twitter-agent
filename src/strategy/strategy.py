from .strategies.basic.basic import BasicTwitterStrategy
from .strategies.remilio.remilio import RemilioTwitterStrategy

# Map strategy names to classes
STRATEGY_MAP = {
    'basic': BasicTwitterStrategy,
    'remilio': RemilioTwitterStrategy,
}

def create_strategy(llm, strategy_name, twitter_client, vectorstore):
    # Fetch the appropriate strategy class from the map
    StrategyClass = STRATEGY_MAP.get(strategy_name)

    # If we didn't find a matching strategy, raise an error
    if StrategyClass is None:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    # Instantiate and return an instance of the strategy
    return StrategyClass(llm, twitter_client, vectorstore)
