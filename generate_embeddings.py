from openai import OpenAI
import pandas as pd
from sklearn import metrics
import pprint
client = OpenAI()
input_datapath = "data/titles.json"  # CHANGE THIS TO USE OTHER DATA TO BUILD NEW EMBEDDINGS
inputData = pd.read_json(input_datapath)
import pprint

current_embedding = 1

def get_input_data(inputData):
   return """
      This is a description of a tv show that we want to recommend to users with questions such as, "What should I watch?".
      I want to ask about drama films or such and get examples.
   """ +pprint.pformat(dict(
      name= inputData['name'],
      tags= [x["name"]  for x in inputData['tags']],
      search_tags = inputData['searchTags'],
      additional_search_tags = inputData['prioritizedSearchTags'],
      production_counties = [x['name'] for x in inputData['countriesOfOriginWithNames']],
      main_languages = [x['name'] for x in inputData['mainLanguages']],
      type_of_programme = inputData['titleType'],
      languages = inputData['languages'],
      longDescription = inputData['longDescription'],
      shortDescription = inputData['shortDescription'],
      freetext = inputData['freeText']
   ))

def get_embedding(text, model="text-embedding-3-large"):
   global current_embedding
   print(f"Getting embedding {current_embedding} of {len(inputData)}")
   current_embedding = current_embedding + 1
   return client.embeddings.create(input = [text], model=model).data[0].embedding


data = inputData.map(lambda x: (x, get_embedding(get_input_data(x))))

data.to_json("data/new_embeddings.json")