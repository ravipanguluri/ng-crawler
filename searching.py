import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
from collections import OrderedDict
from sentence_transformers import SentenceTransformer, util
import torch
from wordhoard import Synonyms
import sys

def get_database():
    user = "samg54"  # NEED TO ADD UR OWN USER
    passw = "mongo999"  # NEED TO ADD UR OWN PASS

    client = MongoClient(
        f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://" + user + ":" + passw + "@ngcluster.sbambjh.mongodb.net/test"

    # # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client.companiesDB


query = input("Please enter a search query:\n")

db = get_database()
collection = db.aidan_gov_companies

# get synonyms of words to run the search on
synonyms_obj = Synonyms(search_string=query)
synonym_results = synonyms_obj.find_synonyms()[:10]
synonym_results.insert(0, query)

freq_map = dict()

 #MongoDB code to get exact matches
for synonym in synonym_results:
    
    pipeline = [
    {'$project': {'occurences': { '$regexFindAll': { 'input': "$html", 'regex': synonym }}, 'cname' : 1, 'website': 1}},
    {'$unwind': '$occurences'},
    {'$group' : { '_id' : {'cname' : '$cname', 'website' : '$website'}, 'count' : {'$sum' : 1}}},
    {'$sort': {'count': -1}}
    ]
    
    matches = list(collection.aggregate(pipeline))[:10]

    for match in matches:
        company_dict = match['_id']
        cname = company_dict['cname']
        count = match['count']
        if cname not in freq_map:
            freq_map[cname] = count
        else:
            freq_map[cname] += count

sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: -item[1]))

print("\n\n======================\n\n")
print("Query:", query)
print("\nTop 10 most relevant companies to keyword:\n")

for i, key in enumerate(sorted_freq_map.keys()):
    if i == 10:
        break
    print(f"Company Name: {key}")
    print(f"Number of Synonym Matches: {sorted_freq_map[key]}")


    

# def get_all_site_text():
#     site_text = []
#     cnames = []
#     items = collection.find()
#     for item in items: 
#         site_text.append(item['html'])
#         cnames.append(item['cname'])
#     return cnames, site_text


# model = SentenceTransformer('msmarco-roberta-base-ance-firstp')


# query_embedding = model.encode(query)
# cnames, site_text = get_all_site_text()
# top_10 = min(10, len(site_text))
# passage_embeddings = model.encode(site_text, convert_to_tensor = True)
# dot_scores = util.dot_score(query_embedding, passage_embeddings)[0]
# top_results = torch.topk(dot_scores, k=top_10)
# print(top_results)
