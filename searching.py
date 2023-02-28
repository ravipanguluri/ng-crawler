import os
from pymongo import MongoClient
from collections import OrderedDict
from wordhoard import Synonyms
from nltk.corpus import wordnet as wn
import scipy
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

startups = input('if you would like to include startups in the query, please type y below:\n')

db = get_database()
if startups == "y":
    collections.append(db.angel_list)
    collections.append(db.github_sanfran)
collections.append(db.venture_capital)
collections.append(db.fortune500)
# collections.append(db.aidan_gov_companies)

syns = wn.synsets(query)


synonyms = set()

for syn in syns:
    for l in syn.lemmas():
        synonyms.add(" ".join(l.name().split("_")))

synonyms = list(synonyms)

print(synonyms)

# collections = [db.aidan_gov_companies,  db.venture_capital, db.fortune500]

words = query.split()
# get synonyms of words to run the search on
synonym_results = []
for i in words:
    synonyms_obj = Synonyms(search_string=i)
    synonym_results.extend(synonyms_obj.find_synonyms()[:(int(10/len(words))+1)])

synonym_results.extend(synonyms)
synonym_results.extend(words)

print(synonym_results)
for j in synonym_results:
    if(len(str(j)) <= 4):
        synonym_results.remove(j)
        print("rem", j)
    print(j)

synonym_results.insert(0, query)
freq_map = dict()



 #MongoDB code to get exact matches
for synonym in set(synonym_results):
    
    pipeline = [
    {'$project': {'occurences': { '$regexFindAll': { 'input': "$html", 'regex': synonym }}, 'cname' : 1, 'website': 1, 'length': 1}},
    {'$unwind': '$occurences'},
    {'$group' : { '_id' : {'cname' : '$cname', 'website' : '$website', 'length' : '$length'}, 'count' : {'$sum' : 1}}},
    {'$sort': {'count': -1}}
    ]

    for collection in collections:
        matches = list(collection.aggregate(pipeline))[:20]

        for match in matches:
            company_dict = match['_id']
            cname = company_dict['cname']
            count = match['count']

            if(len(query) > 3):         # if the query is normal length (not short)
                if synonym == query:    
                    count *= 25         # heavily weight original wording
                elif synonym in words:
                    count *= 2          # reasonable weight to subwords
                else: count *= 1/len(words)/5   # low weight to synonyms
            else:   
                if synonym == query:     # if query short (often could be abbreviation)
                    count*=10   
                elif synonym in words:  # heavier relative  weighting for synonyms
                    count *=2
                else:
                    count *=1
                

            if cname not in freq_map:
                try:
                    freq_map[cname] = (count, company_dict['length'], count / company_dict['length'], company_dict['website'])
                except:
                    pass
            else:
                attrs = list(freq_map[cname])
                attrs[0] += count
                freq_map[cname] = tuple(attrs)
 
                

# sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: -item[1][0]))
sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: (-item[1][0] - 100 * item[1][2]))) # give partial weight to length penalizing 


print("\n\n======================\n\n")
print("Query:", query)
print("\nTop 10 most relevant companies to keyword:\n")

for i, key in enumerate(sorted_freq_map.keys()):
    if i == 10:
        break
    print(f"Company Name: {key}")
    print(f"Number of Synonym Matches: {sorted_freq_map[key][0]}")
    print(f"Match Frequency: {sorted_freq_map[key][2]:.2%}")
    print(f"Company Website: {sorted_freq_map[key][3]}\n")


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
