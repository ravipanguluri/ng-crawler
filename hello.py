from flask import Flask, make_response
from flask_cors import CORS
from flask import request
from wordhoard import Synonyms
from pymongo import MongoClient
import ast

app = Flask(__name__)
CORS(app)


@app.route('/search_companies', methods=['POST'])
def hello():
    # the result object must be in this format:
    #     # key: search_results
    #     # value: array of dictionaries with cname, url, and matchScore
    #     #       as attributes
    # TODO: implement the search algorithm here
    if request.method == 'POST':
        user = "samg54"  # NEED TO ADD UR OWN USER
        passw = "mongo999"  # NEED TO ADD UR OWN PASS
        
        client = MongoClient(
        f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

        db = client.companiesDB
        print(request.json['includeStartups'])
        # this will be a byte string with the JSON:
        #   technologyArea: string
        #   includeStartups: true | false
        collections = []
        if request.json['includeStartups']:
            collections.append(db.angel_list)
            collections.append(db.github_sanfran)
        collections.append(db.venture_capital)
        collections.append(db.fortune500)

        
        synonyms_obj = Synonyms(search_string=request.json['technologyArea'])
        synonym_results = synonyms_obj.find_synonyms()[:10]
        synonym_results.insert(0, request.json['technologyArea'])

        freq_map = dict()

        for synonym in synonym_results:
    
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
                    if synonym == request.json['technologyArea']:
                        count *= 10
                    if cname not in freq_map:
                        try:
                            freq_map[cname] = (count, company_dict['length'], count / company_dict['length'], company_dict['website'])
                        except:
                            pass
                    else:
                        attrs = list(freq_map[cname])
                        attrs[0] += count
                        freq_map[cname] = tuple(attrs)
        
        print(freq_map)

        
                        

        sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: -item[1][2]))


        output_dict = dict()
        output_dict['search_results'] = []


        for cname in list(sorted_freq_map.keys())[:10]:
            inner_dict = dict()
            inner_dict['cname'] = cname
            inner_dict['url'] = sorted_freq_map[cname][3]
            inner_dict['matchScore'] = sorted_freq_map[cname][0]
            inner_dict['matchFrequency'] = round(sorted_freq_map[cname][2], 3) 
            output_dict['search_results'].append(inner_dict)
        print(output_dict)
        
        return output_dict

