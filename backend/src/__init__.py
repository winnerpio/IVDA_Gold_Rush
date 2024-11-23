from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from flask import request
from pymongo.collection import Collection
from .model import Athlete, Country, Sports_event_year
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
sports_event_years: Collection = db["sports_event_year"]
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
        print(args)
        if args == None:
            args = {'year': 1920}
        
        query = {}
        query = {key: value for key, value in request.args.items()}
        if 'year' in args:
            query['year'] = int(args['year'])
        if 'total' in args:
            query['total'] = int(args['total'])
        if 'silver' in args:
            query['silver'] = int(args['silver'])
        if 'gold' in args:
            query['gold'] = int(args['gold'])
        if 'bronze' in args:
            query['bronze'] = int(args['bronze'])
        if 'edition_id' in args:
            query['edition_id'] = int(args['edition_id'])
        
        print(query)

        # Query the MongoDB collection with the constructed query
        cursor = countries.find(query)

        # Extract the data and format it as required
        countries_data = [Country(**doc).to_json() for doc in cursor]
        output = [{"id": c["country_iso2"], "total": c["total"], "sport": c["sport"]} for c in countries_data]

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



class SportEventList(Resource):
    # Return a list of dictionaries {id: iso2, value: total_medals}
    # Possible arguments: None, sport, event
    def get(self, args=None):
        # Retrieve the arguments from the request
        args = request.args.to_dict()
        print(args)
        if args == {}:
            args = {'year_lower': 1920, "year_upper": 1928}
        year_lower = args["year_lower"]
        year_upper = args["year_upper"]

        
        # Query the MongoDB collection with the constructed query
        cursor = sports_event_years.find()

        # Extract the data and format it as required
        sports_event_years_data = [Sports_event_year(**doc).to_json() for doc in cursor]
        print(type(sports_event_years_data))
        output = {}

        for entry in sports_event_years_data:
            sport = entry['sport']
            event = entry['event']
            
            if entry['year'] > year_upper:
                continue
            if entry['year'] < year_lower:
                continue
            if sport not in output:
                output[sport] = []
            if event not in output[sport]:
                output[sport].append(event)

        # Return the output as JSON
        return output

def get_medal_count(countries_data, year_lower, year_upper, sport=None, event=None):
    result = {}
    
    for item in countries_data:
        year = item["year"]
        country_noc = item["country_noc"]
        item_sport = item["sport"][0]  
        item_event = item["sport"][1]

        if not (year_lower <= year <= year_upper):
            continue
        if sport and sport != item_sport:
            continue
        if event and event != item_event:
            continue  



        if country_noc not in result:
            result[country_noc] = {}  

        if year not in result[country_noc]:
            result[country_noc][year] = {"gold": 0, "silver": 0, "bronze": 0, "total": 0}

        result[country_noc][year]["gold"] += item["gold"]
        result[country_noc][year]["silver"] += item["silver"]
        result[country_noc][year]["bronze"] += item["bronze"]
        result[country_noc][year]["total"] += item["total"]

    return result


class MedalCount(Resource):
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        print(args)

        # Example Usage: http://127.0.0.1:5000/athletes?id=65649
        # http://127.0.0.1:5000/athletes?sex=Male&medal=Gold
        
        # If the user specified category is "All" we retrieve all companies
        if args == {}:
            args = {'year_lower': 1920, "year_upper": 1928, "sport": "Athletics", "event": None}
        year_lower = args["year_lower"]
        year_upper = args["year_upper"]
        sport = args["sport"]
        event = args["event"]
        

        cursor = countries.find()
        countries_data = [Country(**doc).to_json() for doc in cursor]


        result = get_medal_count(countries_data, year_lower, year_upper, sport, event)
        # Filter
        return result


api.add_resource(WorldMapList, '/worldmap')
api.add_resource(AthleteList, '/athletes')
api.add_resource(SportEventList, '/SportEventList')
api.add_resource(MedalCount, '/MedalCount')


# Task 1:
# API call that retrieves all data for a given year range
# output of call: dict of key: sport, value: list of all events

# 2nd API input: sport, event and year range,

# Output: dictionary: country key, values: total medals, nested dictionary with key year, and values dictionaries of bronze silver and gold keys with values count 

# Task 2
# 1st APi call: same as before

# 2nd API call: input sport event, and year range
# output: dictionary key is contry code, value is name of country

# 3rd API call: input sport, event, year range and country using country code,
# output: list of athelte, year objects, aggregate by year, counting medals

# Task 3
# 1st APi call: same as before

# 2nd call: input same as before, and two additional attributes
# return top 100 athletes by number of medals, athlete objects (name, year, y/n outlier, values for x and y attributes, highest medal they achieved for that event)

# Task 4
# 1st api call: given user atrributes sex, height, w, age, bmi, h2w, .... (2 of them) cluster based on all of the attributes
# return 100 most similar athletes: cluster they belong to and stuff 

# Task 5
# api call with year, sport and event


# api call with input attribute
# ouptut: distribution and number of medals