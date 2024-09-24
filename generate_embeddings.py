from openai import OpenAI
import pandas as pd
from sklearn import metrics
import pprint
client = OpenAI()
input_datapath = "data/titles.json"  # to save space, we provide a pre-filtered dataset
titles = pd.read_json(input_datapath)
import pprint

current_embedding = 1

def get_title_data(title, model="text-embedding-3-large"):
   return """
      This is a description of a tv show that we want to recommend to users with questions such as, "What should I watch?".
      I want to ask about drama films or such and get examples.
   """ +pprint.pformat(dict(
      name= title['name'],
      tags= [x["name"]  for x in title['tags']],
      search_tags = title['searchTags'],
      additional_search_tags = title['prioritizedSearchTags'],
      production_counties = [x['name'] for x in title['countriesOfOriginWithNames']],
      main_languages = [x['name'] for x in title['mainLanguages']],
      type_of_programme = title['titleType'],
      languages = title['languages'],
      longDescription = title['longDescription'],
      shortDescription = title['shortDescription'],
   ))
   # return (title, client.embeddings.create(input = [str(title)], model=model).data[0].embedding

def get_embedding(text, model="text-embedding-3-large"):
   global current_embedding
   print(f"Getting embedding {current_embedding} of {len(titles)}")
   current_embedding = current_embedding + 1
   return client.embeddings.create(input = [text], model=model).data[0].embedding


data = titles.map(lambda x: (x, get_embedding(get_title_data(x, model='text-embedding-3-large'))))

data.to_json("data/embeddings_take_2.json")