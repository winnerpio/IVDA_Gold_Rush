from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from flask import request
from pymongo.collection import Collection
from .model import Athlete, Country, Sports_event_year
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

cc2country = {
    "US": "United States",
    "GR": "Greece",
    "DE": "Germany",
    "FR": "France",
    "GB": "Great Britain",
    "HU": "Hungary",
    "AT": "Austria",
    "AU": "Australia",
    "DK": "Denmark",
    "CH": "Switzerland",
    "BE": "Belgium",
    "IT": "Italy",
    "NL": "Netherlands",
    "CU": "Cuba",
    "ES": "Spain",
    "NO": "Norway",
    "IN": "India",
    "CZ": "Bohemia",
    "SE": "Sweden",
    "CA": "Canada",
    "RU": "Russian Federation",
    "FI": "Finland",
    "ZA": "South Africa",
    "EE": "Estonia",
    "BR": "Brazil",
    "JP": "Japan",
    "LU": "Luxembourg",
    "NZ": "New Zealand",
    "AR": "Argentina",
    "UY": "Uruguay",
    "IE": "Ireland",
    "PL": "Poland",
    "HT": "Haiti",
    "MC": "Monaco",
    "PT": "Portugal",
    "RO": "Romania",
    "EG": "Egypt",
    "CL": "Chile",
    "PH": "Philippines",
    "MX": "Mexico",
    "LV": "Latvia",
    "TR": "Turkiye",
    "JM": "Jamaica",
    "PE": "Peru",
    "LK": "Sri Lanka",
    "TT": "Trinidad and Tobago",
    "PA": "Panama",
    "KR": "Republic of Korea",
    "IR": "Islamic Republic of Iran",
    "PR": "Puerto Rico",
    "LB": "Lebanon",
    "BG": "Bulgaria",
    "VE": "Venezuela",
    "IS": "Iceland",
    "PK": "Pakistan",
    "BS": "The Bahamas",
    "ET": "Ethiopia",
    "TW": "Chinese Taipei",
    "GH": "Ghana",
    "MA": "Morocco",
    "SG": "Singapore",
    "IQ": "Iraq",
    "TN": "Tunisia",
    "KE": "Kenya",
    "NG": "Nigeria",
    "MN": "Mongolia",
    "UG": "Uganda",
    "CM": "Cameroon",
    "KP": "Democratic People's Republic of Korea",
    "CO": "Colombia",
    "NE": "Niger",
    "BM": "Bermuda",
    "TH": "Thailand",
    "ZW": "Zimbabwe",
    "TZ": "United Republic of Tanzania",
    "GY": "Guyana",
    "CN": "People's Republic of China",
    "CI": "C\u00f4te d'Ivoire",
    "SY": "Syrian Arab Republic",
    "DZ": "Algeria",
    "DO": "Dominican Republic",
    "ZM": "Zambia",
    "SR": "Suriname",
    "CR": "Costa Rica",
    "ID": "Indonesia",
    "SN": "Senegal",
    "VI": "United States Virgin Islands",
    "DJ": "Djibouti",
    "LT": "Lithuania",
    "NA": "Namibia",
    "HR": "Croatia",
    "IL": "Israel",
    "SI": "Slovenia",
    "MY": "Malaysia",
    "QA": "Qatar",
    "UA": "Ukraine",
    "KZ": "Kazakhstan",
    "BY": "Belarus",
    "SK": "Slovakia",
    "AM": "Armenia",
    "BI": "Burundi",
    "EC": "Ecuador",
    "HK": "Hong Kong, China",
    "MD": "Republic of Moldova",
    "UZ": "Uzbekistan",
    "AZ": "Azerbaijan",
    "TO": "Tonga",
    "GE": "Georgia",
    "MZ": "Mozambique",
    "SA": "Kingdom of Saudi Arabia",
    "VN": "Vietnam",
    "BB": "Barbados",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "MK": "North Macedonia",
    "AE": "United Arab Emirates",
    "PY": "Paraguay",
    "ER": "Eritrea",
    "RS": "Serbia",
    "TJ": "Tajikistan",
    "WS": "Samoa",
    "SD": "Sudan",
    "AF": "Afghanistan",
    "MU": "Mauritius",
    "TG": "Togo",
    "BH": "Bahrain",
    "GD": "Grenada",
    "BW": "Botswana",
    "CY": "Cyprus",
    "GA": "Gabon",
    "GT": "Guatemala",
    "ME": "Montenegro",
    "FJ": "Fiji",
    "JO": "Jordan",
    "XK": "Kosovo",
    "SM": "San Marino",
    "TM": "Turkmenistan",
    "BF": "Burkina Faso",
    "LI": "Liechtenstein"
}

country2cc = {value: key for key, value in cc2country.items()}

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
    # Sample Use: http://127.0.0.1:5000/SportEventList?year_lower=2000&year_upper=2010
    def get(self, args=None):
        # Retrieve the arguments from the request
        args = request.args.to_dict()
        print(args)
        if args == {}:
            args = {'year_lower': 1800, "year_upper": 2024}
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])

        
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
        country_noc = item["country_iso2"]
        item_sport = item["sport"][0]  
        item_event = item["sport"][1]

        if not (year_lower <= year <= year_upper):
            continue
        if sport and sport != item_sport:
            continue
        if event and event != item_event:
            continue  



        if country_noc not in result:
            result[country_noc] = {"all": {"gold": 0, "silver": 0, "bronze": 0, "total": 0}}

        if year not in result[country_noc]:
            result[country_noc][year] = {"gold": 0, "silver": 0, "bronze": 0, "total": 0}

        result[country_noc][year]["gold"] += item["gold"]
        result[country_noc][year]["silver"] += item["silver"]
        result[country_noc][year]["bronze"] += item["bronze"]
        result[country_noc][year]["total"] += item["total"]

        result[country_noc]["all"]["gold"] += item["gold"]
        result[country_noc]["all"]["silver"] += item["silver"]
        result[country_noc]["all"]["bronze"] += item["bronze"]
        result[country_noc]["all"]["total"] += item["total"]

    return result


class MedalCount(Resource):
    def get(self, args=None):
        # Sample usage http://127.0.0.1:5000/MedalCount?year_lower=2000&year_upper=2010
        args = request.args.to_dict()
        print(args)
        sport = None
        event = None
        # If the user specified category is "All" we retrieve all companies
        if args == {}:
            args = {'year_lower': 1800, "year_upper": 2024, "sport": None, "event": None}
        if "sport" in args:
            sport = args["sport"]
        if "event" in args:
            event = args["event"]
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])
        

        cursor = countries.find()
        countries_data = [Country(**doc).to_json() for doc in cursor]


        result = get_medal_count(countries_data, year_lower, year_upper, sport, event)
        # Filter
        return result

def get_cc2cn_dict(countries_data, year_lower, year_upper, sport=None, event=None):
    result = {}
    
    for item in countries_data:
        year = item["year"]
        country_noc = item["country_iso2"]
        item_sport = item["sport"][0]  
        item_event = item["sport"][1]

        if not (year_lower <= year <= year_upper):
            continue
        if sport and sport != item_sport:
            continue
        if event and event != item_event:
            continue
    
        if country_noc not in result:
            result[country_noc] = item["country"]
    return result

class CountryCode2CountryName(Resource):
    def get(self, args=None):
        # Sample usage http://127.0.0.1:5000/CC2CN?year_lower=2000&year_upper=2010
        args = request.args.to_dict()
        print(args)
        sport = None
        event = None
        # If the user specified category is "All" we retrieve all companies
        if args == {}:
            args = {'year_lower': 1800, "year_upper": 2024, "sport": None, "event": None}
        if "sport" in args:
            sport = args["sport"]
        if "event" in args:
            event = args["event"]
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])
        

        cursor = countries.find()
        countries_data = [Country(**doc).to_json() for doc in cursor]


        result = get_cc2cn_dict(countries_data, year_lower, year_upper, sport, event)
        # Filter
        return result

def get_athletes(athlete_data, year_lower, year_upper, sport=None, event=None, country_code=None):
    result_dict = {}
    for item in athlete_data:
        year = int(item["year"])
        country_filter = None
        if country_code:
            country_filter = cc2country[country_code]
        
        item_sport = item["sport"]
        item_event = item["event"]
        item_country = item["country"].strip()
        item_medal = item["medal"]
        medal_value = 0
        if item_medal != "No":
            medal_value = 1

        if not (year_lower <= year <= year_upper):
            continue
        if sport and sport != item_sport:
            continue
        if event and event != item_event:
            continue
        if country_filter and country_filter != item_country:
            continue
            # here we add a list of athlete objects
        key = item["name"] + " " + str(year)

        if key not in result_dict:
            data = {
                'name': item["name"],
                'country': item_country,
                'sports': [item_sport],
                'events': [item_event],
                'weight': item["weight"],
                'height': item["height"],
                'bmi': item["bmi"],
                'h2w': item["h2w"],
                'sex': item["sex"],
                'age': item["age"],
                'medal_count': medal_value
            }
        else:
            if item_sport not in result_dict[key]['sports']:
                result_dict[key]['sports'].append(item_sport)
            if item_event not in result_dict[key]['events']:
                result_dict[key]['events'].append(item_event)
            result_dict[key]['medal_count'] += medal_value
            
        result_dict[key] = data


    return result_dict

class CountryAthletes(Resource):
    def get(self, args=None):
        # Sample usage http://127.0.0.1:5000/CountryAthletes?year_lower=2000&year_upper=2010&sport=Athletics&country_code=US
        args = request.args.to_dict()
        print(args)
        sport = None
        event = None
        country_code = None
        country_filter = None
        query = {}
        # If the user specified category is "All" we retrieve all companies
        if args == {}:
            args = {'year_lower': 1800, "year_upper": 2024, "sport": None, "event": None, "country_code": None}
        if "sport" in args:
            sport = args["sport"]
        if "event" in args:
            event = args["event"]
        if "country_code" in args:
            country_code = args["country_code"]
            country_filter = cc2country[country_code]
        if country_filter:
            query["country"] = country_filter
        if sport:
            query["sport"] = sport
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])
        

        cursor = athletes.find(query)
        athlete_data = [Athlete(**doc).to_json() for doc in cursor]

        result = get_athletes(athlete_data, year_lower, year_upper, sport, event, country_code)
        # Filter
        return result

api.add_resource(WorldMapList, '/worldmap')
api.add_resource(AthleteList, '/athletes')

# Task 1
api.add_resource(SportEventList, '/SportEventList')
api.add_resource(MedalCount, '/MedalCount')


# Task 2
api.add_resource(CountryCode2CountryName, '/CC2CN')
api.add_resource(CountryAthletes, '/CountryAthletes')

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