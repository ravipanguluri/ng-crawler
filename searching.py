import os
from pymongo import MongoClient
from collections import OrderedDict
from wordhoard import Synonyms
from nltk.corpus import wordnet as wn
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
collections = []
vc = input("If you want to include venture capital firms in your search, please type y below:\n")
gov_companies = input("If you want to include government companies in your search, please type y below:\n")
fortune_500 = input("If you want to include fortune 500 companies in your search, please type y below:\n")

syns = wn.synsets(query)


synonyms = set()

for syn in syns:
    for l in syn.lemmas():
        synonyms.add(" ".join(l.name().split("_")))

synonyms = list(synonyms)

db = get_database()
collections = [db.aidan_gov_companies,  db.venture_capital, db.fortune500]

# get synonyms of words to run the search on
synonyms_obj = Synonyms(search_string=query)
synonym_results = synonyms_obj.find_synonyms()[:10]
synonym_results.insert(0, query)

freq_map = dict()

 #MongoDB code to get exact matches
for synonym in synonyms:
    
    pipeline = [
    {'$project': {'occurences': { '$regexFindAll': { 'input': "$html", 'regex': synonym }}, 'cname' : 1, 'website': 1}},
    {'$unwind': '$occurences'},
    {'$group' : { '_id' : {'cname' : '$cname', 'website' : '$website'}, 'count' : {'$sum' : 1}}},
    {'$sort': {'count': -1}}
    ]

    for collection in collections:
        matches = list(collection.aggregate(pipeline))[:10]

        for match in matches:
            company_dict = match['_id']
            cname = company_dict['cname']
            count = match['count']
            if synonym == query:
                count *= 5
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


#Some ML Stuff do not worry about this
    

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
