from flask import Flask, make_response
from flask_cors import CORS
from flask import request
from wordhoard import Synonyms
from pymongo import MongoClient
from nltk.corpus import wordnet as wn
import ast

app = Flask(__name__)
CORS(app)


@app.route('/search_companies', methods=['POST'])
def hello():
    # the result object must be in this format:
    #     # key: search_results
    #     # value: array of dictionaries with cname, url, and matchScore
    #     #       as attributes
    if request.method == 'POST':
        #MongoDB credentials
        user = "samg54"  # NEED TO ADD UR OWN USER
        passw = "mongo999"  # NEED TO ADD UR OWN PASS
        
        #Create a mongo client to read/write to db
        client = MongoClient(
        f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

        #Use client to access my current cluster

        db = client.companiesDB
        # request.json will be a dictionary with the following two keys and values:
        #   technologyArea: string
        #   includeStartups: true | false

        #list of collections in the db that we want to use in the search
        collections = []

        if request.json['includeStartups']:
            collections.append(db.angel_list)
            collections.append(db.github_sanfran)
        
        collections.append(db.venture_capital)
        collections.append(db.fortune500)


        query = request.json['technologyArea']
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

        print(synonym_results)

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
        


        
                        
        #sort the freqency map's entries by the match score 
        sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: (-item[1][0] - 100 * item[1][2]))) # give partial weight to length penalizing 

        #make an output dict to match the formatting of the result flask expects to feed to the frontend
        output_dict = dict()
        output_dict['search_results'] = []

        #For each of the top 10 companies by match score, make an inner dictionary containing company name and attributes
        for cname in list(sorted_freq_map.keys())[:10]:
            inner_dict = dict()
            #Check if I need to capitalize any letters in the string
            contains_uppercase = any(char.isupper() for char in cname)
            if contains_uppercase:
                inner_dict['cname'] = cname
            else:
                inner_dict['cname'] = cname.title()

            # pull attributes from the original dictionary's tuples
            inner_dict['url'] = sorted_freq_map[cname][3]
            inner_dict['matchScore'] = int(100 *(sorted_freq_map[cname][2]) + sorted_freq_map[cname][0])
            # Append result to the output dictionary
            output_dict['search_results'].append(inner_dict)
        
        return output_dict

