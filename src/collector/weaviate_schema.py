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
        {
            "dataType": ["text"],
            "description": "agent id",
            "name": "agent_id",
        },
        {
            "dataType": ["date"],
            "description": "date",
            "name": "date",
        },
        {
            "dataType": ["int"],
            "description": "follower count",
            "name": "follower_count",
        },
        {
            "dataType": ["int"],
            "description": "like count",
            "name": "like_count",
        },
            ],
    "vectorizer": "text2vec-openai",
}

# add the schema
# client.schema.create_class(class_obj)

add_prop = {
            "dataType": ["int"],
            "description": "like count",
            "name": "like_count",
        }


client.schema.property.create("Tweets", add_prop)

# get the schema
schema = client.schema.get()

# print the schema
print(json.dumps(schema, indent=4))
