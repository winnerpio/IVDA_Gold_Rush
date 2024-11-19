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

class AthleteList(Resource):
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        print(args)
        # If the user specified category is "All" we retrieve all companies
        cursor = athletes.find()
        return [Athlete(**doc).to_json() for doc in cursor]

class CountryList(Resource):
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        print(args)
        # If the user specified category is "All" we retrieve all companies
        cursor = countries.find()
        return [Country(**doc).to_json() for doc in cursor]


api.add_resource(AthleteList, '/athletes')
api.add_resource(AthleteList, '/countries')