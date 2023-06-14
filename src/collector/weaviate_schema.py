import weaviate
import json

client = weaviate.Client("http://localhost:8080")

# we will create the class "Question"
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
client.schema.create_class(class_obj)

# get the schema
schema = client.schema.get()

# print the schema
print(json.dumps(schema, indent=4))
