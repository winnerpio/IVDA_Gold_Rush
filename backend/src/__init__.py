from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from flask import request
from pymongo.collection import Collection
from .model import Athlete, Country, Sports_event_year
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
from collections import defaultdict
import random
from sklearn.cluster import KMeans

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

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
                output[sport] = sorted(output[sport]) # Inmediatly sort the events for each sport
        sorted_output = dict(sorted(output.items()))
        # Return the output as JSON
        return sorted_output

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
        sorted_countries_data = sorted(countries_data, key=lambda item: item["country"])

        result = get_cc2cn_dict(sorted_countries_data, year_lower, year_upper, sport, event)
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
            result_dict[key] = data
        else:
            if item_sport not in result_dict[key]['sports']:
                result_dict[key]['sports'].append(item_sport)
            if item_event not in result_dict[key]['events']:
                result_dict[key]['events'].append(item_event)
            result_dict[key]['medal_count'] += medal_value
    
    # Sort by name and secondly by year
    sorted_result = dict(sorted(result_dict.items(), key=lambda item: (item[1]["name"], item[1]["age"])))

    return sorted_result

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

# Task 1:
# API call that retrieves all data for a given year range
# output of call: dict of key: sport, value: list of all events

# 2nd API input: sport, event and year range,

# Output: dictionary: country key, values: total medals, nested dictionary with key year, and values dictionaries of bronze silver and gold keys with values count 


api.add_resource(SportEventList, '/SportEventList')
api.add_resource(MedalCount, '/MedalCount')


# Task 2

# Task 2
# 1st APi call: same as before

# 2nd API call: input sport event, and year range
# output: dictionary key is contry code, value is name of country

# 3rd API call: input sport, event, year range and country using country code,
# output: list of athelte, year objects, aggregate by year, counting medals

# api.add_resource(SportEventList, '/SportEventList')
api.add_resource(CountryCode2CountryName, '/CC2CN')
api.add_resource(CountryAthletes, '/CountryAthletes')


# Task 3
# 1st APi call: same as before
#api.add_resource(SportEventList, '/SportEventList')
medal_map = {
    0: "None",
    1: "Bronze",
    2: "Silver",
    3: "Gold"
}


def detect_outliers(data, x_key, y_key, top_n=500):

    top_entries = sorted(data.items(), key=lambda x: x[1]["medal_count"], reverse=True)[:top_n]
    

    x_values = [entry[1][x_key] for entry in top_entries]
    y_values = [entry[1][y_key] for entry in top_entries]
    

    def calculate_iqr(values):
        Q1 = np.percentile(values, 25)
        Q3 = np.percentile(values, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.3 * IQR
        upper_bound = Q3 + 1.3 * IQR
        return lower_bound, upper_bound

    x_lower, x_upper = calculate_iqr(x_values)
    y_lower, y_upper = calculate_iqr(y_values)
    
    output = []
    for entry, x, y in zip(top_entries, x_values, y_values):
        reasons = []
        if x < x_lower:
            reasons.append(f"{x_key} ({x}) is below the lower bound ({x_lower})")
        if x > x_upper:
            reasons.append(f"{x_key} ({x}) is above the upper bound ({x_upper})")
        if y < y_lower:
            reasons.append(f"{y_key} ({y}) is below the lower bound ({y_lower})")
        if y > y_upper:
            reasons.append(f"{y_key} ({y}) is above the upper bound ({y_upper})")
        entry[1]["outlier"] = False
        if reasons:
            entry[1]["outlier"] = True
        entry[1]["highest_medal"] = medal_map[entry[1]["highest_medal"]]
        output.append((entry[0], entry[1], reasons))
    
    return output

def convert_to_dict(data):
    result_dict = {}
    for entry in data:
        key = entry[0]
        value = {
            "data": entry[1],
            "reasons": entry[2]
        }
        result_dict[key] = value
    return result_dict


def get_outliers(athlete_data, year_lower, year_upper, sport=None, event=None, country_code=None, x_axis_variable=None, y_axis_variable=None):
    result_dict = {}
    
    for item in athlete_data:
        year = int(item["year"])
        current_medal_nr = 0
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
            if item_medal == "Bronze":
                current_medal_nr = 1
            if item_medal == "Silver":
                current_medal_nr = 2
            if item_medal == "Gold":
                current_medal_nr = 3



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
                'medal_count': medal_value,
                'highest_medal': current_medal_nr,
                'x_axis_variable_value': item[x_axis_variable],
                'y_axis_variable_value': item[y_axis_variable]
            }
            result_dict[key] = data
        else:
            if item_sport not in result_dict[key]['sports']:
                result_dict[key]['sports'].append(item_sport)
            if item_event not in result_dict[key]['events']:
                result_dict[key]['events'].append(item_event)
            result_dict[key]['medal_count'] += medal_value
            if current_medal_nr > result_dict[key]['highest_medal']:
                result_dict[key]['highest_medal'] = current_medal_nr

    outliers = detect_outliers(result_dict, x_axis_variable, y_axis_variable, 1000)
    
    return convert_to_dict(outliers)

class Outliers(Resource):
    def get(self, args=None):
        # Sample usage http://127.0.0.1:5000/GetOutliers?year_lower=1900&year_upper=2010&x_axis_variable=age&y_axis_variable=weight&country_code=US
        args = request.args.to_dict()
        print(args)
        sport = None
        event = None
        country_code = None
        country_filter = None
        x_axis_variable = None
        y_axis_variable = None
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
        x_axis_variable = args["x_axis_variable"]
        y_axis_variable = args["y_axis_variable"]
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])
        

        cursor = athletes.find(query)
        athlete_data = [Athlete(**doc).to_json() for doc in cursor]

        result = get_outliers(athlete_data, year_lower, year_upper, sport, event, country_code, x_axis_variable, y_axis_variable)
        # Filter
        return result

api.add_resource(Outliers, '/GetOutliers')
# 2nd call: input same as before, and two additional attributes
# return top 100 athletes by number of medals, athlete objects (name, year, y/n outlier, values for x and y attributes, highest medal they achieved for that event)

# Task 4
# 1st api call: given user atrributes sex, height, w, age, bmi, h2w, .... (2 of them) cluster based on all of the attributes
# return 100 most similar athletes: cluster they belong to and stuff 



# Clustering Task

def get_clustering(
    athlete_data, year_lower, year_upper, sport, event, country_code,
    x_axis_variable, y_axis_variable, sport1, sport2, sport3,
    user_age, user_bmi, user_height, user_weight, user_h2w, athlete_number
):
    # Filtering
    filtered_athletes = []
    for item in athlete_data:
        year = int(item["year"])
        country_filter = None
        if country_code:
            country_filter = cc2country[country_code]
        
        item_sport = item["sport"]
        item_event = item["event"]
        item_country = item["country"].strip()

        if not (year_lower <= year <= year_upper):
            continue
        if sport and sport != item_sport:
            continue
        if event and event != item_event:
            continue
        if country_filter and country_filter != item_country:
            continue

        filtered_athletes.append(item)
    
    # Randomly sampling athletes from sport1, sport2, and sport3
    random_athletes = []
    for sport_filter in [sport1, sport2, sport3]:
        sport_athletes = [athlete for athlete in filtered_athletes if athlete["sport"] == sport_filter]
        sampled_athletes = random.sample(sport_athletes, min(athlete_number, len(sport_athletes)))
        random_athletes.extend(sampled_athletes)

    # Add the user's data as an athlete
    user_data_mapping = {
    "age": user_age,
    "weight": user_weight,
    "height": user_height,
    "bmi": user_bmi,
    "h2w": user_h2w
    }

    # Use the dictionary to get the value
    user_x = user_data_mapping.get(x_axis_variable)
    user_y = user_data_mapping.get(y_axis_variable)


    user_data = {
        "name": "User",
        "age": user_age,
        "bmi": user_bmi,
        "height": user_height,
        "weight": user_weight,
        "h2w": user_h2w,
        "x_axis_variable_value": user_x,
        "y_axis_variable_value": user_y,
        "sport": "User"
    }
    random_athletes.append(user_data)

    clustering_data = [
        (athlete[x_axis_variable], athlete[y_axis_variable])
        for athlete in random_athletes
    ]
    clustering_data = np.array(clustering_data)
    clustering_data = scaler.fit_transform(clustering_data)
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_labels = kmeans.fit_predict(clustering_data)
    
    
    # Making return object
    for athlete, cluster in zip(random_athletes, cluster_labels):
        athlete["cluster"] = int(cluster)
        athlete["x_axis_value"] = athlete[x_axis_variable]
        athlete["y_axis_value"] = athlete[y_axis_variable]
    return random_athletes

# Sample usage http://127.0.0.1:5000/GetClustering?year_lower=2000&year_upper=2010&country_code=US&x_axis_variable=age&y_axis_variable=weight&sport1=Swimming&sport2=Football&sport3=Athletics
class Clustering(Resource):
    def get(self, args=None):
        args = request.args.to_dict()
        print(args)

        # General Data
        sport = None
        event = None
        country_code = None
        country_filter = None
        x_axis_variable = None
        y_axis_variable = None
        sport1 = None
        sport2 = None
        sport3 = None
        
        # User Data
        user_age = 25
        user_bmi = 20
        user_height = 190
        user_weight = 90
        user_h2w = 2
        
        
        query = {}
        if args == {}:
            args = {'year_lower': 1800, "year_upper": 2024, "sport": None, "event": None, "country_code": None}
        if "sport" in args:
            sport = args["sport"]
        if "event" in args:
            event = args["event"]
        if "country_code" in args:
            country_code = args["country_code"]
            country_filter = cc2country[country_code]

        #updating user data using args
        if "user_age" in args:
            user_age = args["user_age"]
        if "user_bmi" in args:
            user_bmi = args["user_bmi"]
        if "user_height" in args:
            user_height = args["user_height"]
        if "user_weight" in args:
            user_weight = args["user_weight"]
        if "user_h2w" in args:
            user_h2w = args["user_h2w"]


        if country_filter:
            query["country"] = country_filter
        if sport:
            query["sport"] = sport
        if event:
            query["event"] = event
        x_axis_variable = args["x_axis_variable"]
        y_axis_variable = args["y_axis_variable"]
        sport1 = args["sport1"]
        sport2 = args["sport2"]
        sport3 = args["sport3"]
        
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])
        

        cursor = athletes.find(query)
        athlete_data = [Athlete(**doc).to_json() for doc in cursor]

        result = get_clustering(athlete_data, year_lower, year_upper, sport, event, country_code, x_axis_variable, y_axis_variable, 
                                sport1, sport2, sport3, user_age, user_bmi, user_height, user_weight, user_h2w, 100)
        # Filter
        return result

api.add_resource(Clustering, '/GetClustering')

dist_variable2units = {
    "age": "years",
    "weight": "kg",
    "height": "cm",
    "bmi": "",
    "h2w": ""
}

# Task 5
# api call with year, sport and event
#api.add_resource(SportEventList, '/SportEventList')

def get_distribution_data(athlete_data, year_lower, year_upper, sport=None, event=None, country_code=None, dist_variable=None, bins=None):
    result_dict = defaultdict(lambda: {"athlete_count": 0, "medal_count": 0})
    values = []
    if bins is None:
        bins = 20

    # Determine the unit for the dist_variable
    unit = dist_variable2units.get(dist_variable, "")  # Default to empty string if no unit is defined

    # Filter athlete data based on the given criteria
    for item in athlete_data:
        year = int(item["year"])
        country_filter = None
        if country_code:
            country_filter = cc2country[country_code]
        
        item_sport = item["sport"]
        item_event = item["event"]
        item_country = item["country"].strip()
        item_medal = item["medal"]
        medal_value = 1 if item_medal != "No" else 0

        if not (year_lower <= year <= year_upper):
            continue
        if sport and sport != item_sport:
            continue
        if event and event != item_event:
            continue
        if country_filter and country_filter != item_country:
            continue

        # Collect the dist_variable value
        if dist_variable in item:
            values.append((item[dist_variable], medal_value))

    variable_values, medal_values = zip(*values)

    # Determine bin edges
    min_val = int(np.floor(min(variable_values)))
    max_val = int(np.ceil(max(variable_values)))

    bin_edges = np.linspace(min_val, max_val, bins + 1)
    bin_edges = np.round(bin_edges).astype(int)
    bin_edges = np.unique(bin_edges)

    bin_indices = np.digitize(variable_values, bins=bin_edges, right=False)

    for idx, (value, medal) in enumerate(zip(variable_values, medal_values)):
        bin_index = bin_indices[idx]
        if bin_index == 0:
            bin_range = f"< {bin_edges[0]} {unit}".strip()
            bin_key = bin_edges[0] - 1
        elif bin_index >= len(bin_edges):
            bin_range = f">= {bin_edges[-1]} {unit}".strip()
            bin_key = bin_edges[-1] + 1
        else:
            bin_range = f"{bin_edges[bin_index - 1]} - {bin_edges[bin_index]} {unit}".strip()
            bin_key = bin_edges[bin_index - 1]
        
        result_dict[bin_key] = result_dict[bin_key]
        result_dict[bin_key]["bin_range"] = bin_range
        result_dict[bin_key]["athlete_count"] += 1
        result_dict[bin_key]["medal_count"] += medal

    # s
    sorted_result = dict(sorted(result_dict.items(), key=lambda x: x[0]))
    final_result = {
        v["bin_range"]: {
            "athlete_count": v["athlete_count"],
            "medal_count": v["medal_count"]
        }
        for k, v in sorted_result.items()
    }
    return final_result



class Distribution(Resource):
    def get(self, args=None):
        # Sample usage http://127.0.0.1:5000/GetDistribution?year_lower=2000&year_upper=2010&dist_variable=age&country_code=US&bins=13
        args = request.args.to_dict()
        print(args)
        sport = None
        event = None
        country_code = None
        country_filter = None
        dist_variable = None
        bins = None
        query = {}
        # If the user specified category is "All" we retrieve all companies
        if args == {}:
            args = {'year_lower': 1800, "year_upper": 2024, "sport": None, "event": None, "country_code": None}
        if "sport" in args:
            sport = args["sport"]
        if "event" in args:
            event = args["event"]
        if "bins" in args:
            bins = int(args["bins"])
        if "country_code" in args:
            country_code = args["country_code"]
            country_filter = cc2country[country_code]
        if country_filter:
            query["country"] = country_filter
        if sport:
            query["sport"] = sport
        if event:
            query["event"] = event
        
        dist_variable = args["dist_variable"]
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])
        

        cursor = athletes.find(query)
        athlete_data = [Athlete(**doc).to_json() for doc in cursor]

        result = get_distribution_data(athlete_data, year_lower, year_upper, sport, event, country_code, dist_variable, bins)
        # Filter
        return result

def get_distribution_data2(
    athlete_data, year_lower, year_upper, sport=None, event=None, country_code=None, dist_variable=None, bins=None
):
    overall_result = defaultdict(lambda: defaultdict(lambda: {"athlete_count": 0, "medal_count": 0}))
    if bins is None:
        bins = 20

    unit = dist_variable2units.get(dist_variable, "")

    filtered_data = []
    for item in athlete_data:
        year = int(item["year"])
        country_filter = None
        if country_code:
            country_filter = cc2country[country_code]
        
        item_sport = item["sport"]
        item_event = item["event"]
        item_country = item["country"].strip()
        item_medal = item["medal"]
        medal_value = 1 if item_medal != "No" else 0

        if not (year_lower <= year <= year_upper):
            continue
        if sport and sport != item_sport:
            continue
        if event and event != item_event:
            continue
        if country_filter and country_filter != item_country:
            continue

        # Collect the dist_variable value
        if dist_variable in item:
            filtered_data.append((year, item[dist_variable], medal_value))

    years = set([entry[0] for entry in filtered_data])
    for year in sorted(years):
        year_data = [(value, medal) for y, value, medal in filtered_data if y == year]

        if not year_data:
            continue

        variable_values, medal_values = zip(*year_data)

        min_val = int(np.floor(min(variable_values)))
        max_val = int(np.ceil(max(variable_values)))

        bin_edges = np.linspace(min_val, max_val, bins + 1)
        bin_edges = np.round(bin_edges).astype(int)
        bin_edges = np.unique(bin_edges)

        bin_indices = np.digitize(variable_values, bins=bin_edges, right=False)

        for idx, (value, medal) in enumerate(zip(variable_values, medal_values)):
            bin_index = bin_indices[idx]
            if bin_index == 0:
                bin_range = f"< {bin_edges[0]} {unit}".strip()
                bin_key = bin_edges[0] - 1
            elif bin_index >= len(bin_edges):
                bin_range = f">= {bin_edges[-1]} {unit}".strip()
                bin_key = bin_edges[-1] + 1
            else:
                bin_range = f"{bin_edges[bin_index - 1]} - {bin_edges[bin_index]} {unit}".strip()
                bin_key = bin_edges[bin_index - 1]
            
            overall_result[year][bin_range]["athlete_count"] += 1
            overall_result[year][bin_range]["medal_count"] += medal

    final_result = {}
    for year, bins in overall_result.items():
        final_result[year] = dict(sorted(bins.items()))

    return final_result



class Distribution2(Resource):
    def get(self, args=None):
        # Sample usage http://127.0.0.1:5000/GetDistribution?year_lower=2000&year_upper=2010&dist_variable=age&country_code=US&bins=13
        args = request.args.to_dict()
        print(args)
        sport = None
        event = None
        country_code = None
        country_filter = None
        dist_variable = None
        bins = None
        query = {}
        # If the user specified category is "All" we retrieve all companies
        if args == {}:
            args = {'year_lower': 1800, "year_upper": 2024, "sport": None, "event": None, "country_code": None}
        if "sport" in args:
            sport = args["sport"]
        if "event" in args:
            event = args["event"]
        if "bins" in args:
            bins = int(args["bins"])
        if "country_code" in args:
            country_code = args["country_code"]
            country_filter = cc2country[country_code]
        if country_filter:
            query["country"] = country_filter
        if sport:
            query["sport"] = sport
        if event:
            query["event"] = event
        
        dist_variable = args["dist_variable"]
        year_lower = int(args["year_lower"])
        year_upper = int(args["year_upper"])
        

        cursor = athletes.find(query)
        athlete_data = [Athlete(**doc).to_json() for doc in cursor]

        result = get_distribution_data2(athlete_data, year_lower, year_upper, sport, event, country_code, dist_variable, bins)
        # Filter
        return result


api.add_resource(Distribution, '/GetDistribution')
api.add_resource(Distribution2, '/GetDistribution2')
# api call with input attribute
# ouptut: distribution and number of medals