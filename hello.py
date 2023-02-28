from flask import Flask, make_response
from flask_cors import CORS
from flask import request

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
        print(request.form)
        # this will be a byte string with the JSON:
        #   technologyArea: string
        #   includeStartups: true | false
        print(request.get_data())
        return {
            "search_results": [
                {"cname": "Google", "url": 'google.com', 'matchScore': '5'},
                {"cname": "Microsoft", "url": 'microsoft.com', 'matchScore': '2'}
            ]
        }
