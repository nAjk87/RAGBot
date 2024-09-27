from openai import OpenAI
import pandas as pd
from sklearn import metrics
import pprint

client = OpenAI()


data = pd.read_json("data/embeddings.json")


def get_question_embedding(question, model="text-embedding-3-small"):
    return client.embeddings.create(input=[question], model=model).data[0].embedding


def get_recommendations(question: str):
    similarity = data.map(
        lambda x: (
            x[0],
            metrics.pairwise.cosine_similarity([x[1]], [question])[0][0],
        )
    )

    result = sorted(similarity["item"], key=lambda x: x[1], reverse=True)
    return [(i[0]["name"], i[0]["longDescription"]) for i in result[:10]]
