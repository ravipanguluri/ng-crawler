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

        #Create a synonym object for all synonyms of the user's input string
        synonyms_obj = Synonyms(search_string=request.json['technologyArea'])
        synonym_results = synonyms_obj.find_synonyms()[:10] #Take only the first 10 synonyms to reduce runtime

        #Prepend original query to the list of synonyms 
        synonym_results.insert(0, request.json['technologyArea'])

        freq_map = dict()

        for synonym in synonym_results:

            #Create a pipeline of instructions for the db that count the number of times the user's input string appears in the site's html
    
            pipeline = [
            {'$project': {'occurences': { '$regexFindAll': { 'input': "$html", 'regex': synonym }}, 'cname' : 1, 'website': 1, 'length': 1}},
            {'$unwind': '$occurences'},
            {'$group' : { '_id' : {'cname' : '$cname', 'website' : '$website', 'length' : '$length'}, 'count' : {'$sum' : 1}}},
            {'$sort': {'count': -1}}
            ]


            for collection in collections:
                #Apply the pipeline to every collections that the user has indicated that they want
                matches = list(collection.aggregate(pipeline))[:20]

                #matches will return a list of dictionaries with the ObjectId as a key and attributes about match stored as an inner dictionary
                for match in matches:
                    company_dict = match['_id']
                    cname = company_dict['cname']
                    count = match['count']

                    # Giving greater weight to original query, so we add a multiplier to the count
                    if synonym == request.json['technologyArea']:
                        count *= 10

                    #Add entry to frequency map that will contanin cname and a tuple of attributes for that cname
                    if cname not in freq_map:
                        try:
                            freq_map[cname] = (count, company_dict['length'], count / company_dict['length'], company_dict['website'])
                        except:
                            pass
                    else:
                        #If the company has already matched with a previous synonym, just increment the counr
                        attrs = list(freq_map[cname])
                        attrs[0] += count
                        freq_map[cname] = tuple(attrs)
        
                        
        #sort the freqency map's entries by the match score 
        sorted_freq_map = dict(sorted(freq_map.items(), key=lambda item: -item[1][2]))

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
            inner_dict['matchScore'] = sorted_freq_map[cname][0]
            # Append result to the output dictionary
            output_dict['search_results'].append(inner_dict)
        
        return output_dict

