from openai import OpenAI
import pandas as pd
from sklearn import metrics
import pprint
client = OpenAI()
input_datapath = "output-formatted.json"  # CHANGE THIS TO USE OTHER DATA TO BUILD NEW EMBEDDINGS
inputData = pd.read_json(input_datapath)
import pprint

current_embedding = 1

def get_input_data(inputData):
   return """
      This is different sections from the employee handbook. Answers to questions should be searched for in the paragraphs, and you should reference the section title.
   """ +pprint.pformat(dict(
      section_title= inputData['section_title'],
      paragraphs= [x["paragraph"]  for x in inputData['content']],
   ))

def get_embedding(text, model="text-embedding-3-large"):
   global current_embedding
   print(f"Getting embedding {current_embedding} of {len(inputData)}")
   current_embedding = current_embedding + 1
   return client.embeddings.create(input = [text], model=model).data[0].embedding


data = inputData.map(lambda x: (x, get_embedding(get_input_data(x))))

data.to_json("data/new_embeddings.json")
