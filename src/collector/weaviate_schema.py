import weaviate
import json

client = weaviate.Client("http://localhost:8080")

class_obj = {
    "class": "Tweets",
    "description": "Recent tweet from the timeline",  # description of the class
    "properties": [
        {
            "dataType": ["text"],
            "description": "tweet text",
            "name": "tweet",
        },
        {
            "dataType": ["text"],
            "description": "tweet id",
            "name": "tweet_id",
        },
            ],
    "vectorizer": "text2vec-openai",
}

# add the schema
# client.schema.create_class(class_obj)

add_prop = {
            "dataType": ["text"],
            "description": "agent id",
            "name": "agent_id",
        }

client.schema.property.create("Tweets", add_prop)

# get the schema
schema = client.schema.get()

# print the schema
print(json.dumps(schema, indent=4))
