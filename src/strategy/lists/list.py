class ListStrategy:
    def __init__(self, client):
        self.client = client

    def create_agent_lists(self, lists):
        for list in lists:
            self.client.create_list(list)
