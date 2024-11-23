from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from flask import request
from pymongo.collection import Collection
from .model import Athlete, Country
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
uri = "mongodb+srv://olympic:gold@olympiccluster.yxmi4.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["olympic_db"]

# Get a reference to the collections
athletes: Collection = db["athletes"]
countries: Collection = db["countries"]
api = Api(app)

'''
Endpoints:
    - WorldMapList: List of pairs per country iso2 - total (medals)
    - AthleteList
    - SportList
    - EventList
    - RadarData
    - DistCorrData
    - AthleteCluster
    - OutlierData
'''

class WorldMapList(Resource):
    # Return a list of dictionaries {id: iso2, value: total_medals}
    # Possible arguments: None, sport, event
    def get(self, args=None):
        # Retrieve the arguments from the request
        args = request.args.to_dict()

        # Build the query based on the provided arguments
        query = {}
        if 'sport' in args:
            query['sport'] = args['sport']
        if 'event' in args:
            query['event'] = args['event']

        # Query the MongoDB collection with the constructed query
        cursor = countries.find(query)

        # Extract the data and format it as required
        countries_data = [Country(**doc).to_json() for doc in cursor]
        output = [{"id": c["country_iso2"], "value": c["total"]} for c in countries_data]

        # Return the output as JSON
        return output
        

class AthleteList(Resource):
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        print(args)

        # Example Usage: http://127.0.0.1:5000/athletes?id=65649
        # http://127.0.0.1:5000/athletes?sex=Male&medal=Gold
        
        # If the user specified category is "All" we retrieve all companies
        if args == None:
            args = {"id":65649}

        query = {}
        query = {key: value for key, value in request.args.items()}
        if 'id' in args:
            query['id'] = int(args['id'])
        if 'edition_id' in args:
            query['edition_id'] = int(args['edition_id'])
        if 'age' in args:
            query['age'] = int(args['age'])

        cursor = athletes.find(query)
        # Filter
        return [Athlete(**doc).to_json() for doc in cursor]

api.add_resource(WorldMapList, '/worldmap')
api.add_resource(AthleteList, '/athletes')