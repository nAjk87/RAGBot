from openai import OpenAI
import pandas as pd
from sklearn import metrics
import pprint
client = OpenAI()
input_datapath = "data/recept.json"  # CHANGE THIS TO USE OTHER DATA TO BUILD NEW EMBEDDINGS
inputData = pd.read_json(input_datapath)
import pprint

current_embedding = 1

def get_input_data(recipe):
   return """
      This is a description of a food recipe, to recommend to users with questions such as "what should i cook tonight" or "I have brocolli at home can you give me some good recipes with brocolli in them?" or "I really like salmon, got any good salmon recipes?".
   """ +pprint.pformat(dict(
      titel= recipe['titel'],
      ingredienser= recipe['ingredienser'],
      tillagning = recipe['tillagning'],
      portioner = recipe['portioner'],
      svarighetsgrad = recipe['svårighetsgrad'],
      tillagningstid = recipe['tillagningstid'],
      sasong = recipe['säsong'],
   ))

def get_embedding(text, model="text-embedding-3-large"):
   global current_embedding
   print(f"Getting embedding {current_embedding} of {len(inputData)}")
   current_embedding = current_embedding + 1
   return client.embeddings.create(input = [text], model=model).data[0].embedding


data = inputData.map(lambda x: (x, get_embedding(get_input_data(x))))

data.to_json("data/new_embeddings.json")