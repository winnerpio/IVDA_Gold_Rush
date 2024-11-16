# Here we want to define the goal tables that are to be acheived

0) Database

| Column | Type (value) | Pre-process |
| :-: | :-: | :-- |
| athlete_id      | int                ||
| name            | str                ||
| sex             | str (Male/Female)  ||
| born            | str (date)         | Standarize format (datetime, default 01/01/YYYY) |
| height          | int (cm)           ||
| weight          | int (kg)           ||
| country         | str (country_name) ||
| country_noc     | str (country_noc)  ||
| description     | str (info)         ||
| spetial_notes   | str (info)         ||
: Athlete Biography :

| Column | Type (value) | Pre-process |
| :-: | :-: | :-- |
| edition     | str (year + event)      ||
| edition_id  | int                     ||
| country_noc | str (of the athlete)    ||
| sport       | str (of the athlete)    ||
| event       | str (within the sport)  ||
| result_id   | int (results)           ||
| athlete     | str (name)              ||
: Athlete Event Details :

| Column | Type (value) | Pre-process |
| :-: | :-: | :-- |
| noc       | str (3-letter word)   ||
| country   | str (name)            | Remove ROC |
: Country Profiles :

| Column | Type (value) | Pre-process |
| :-: | :-: | :-- |
| result_id             | int                               ||
| event_title           | str (title, sex)                  ||
| edition               | str (year + event)                ||
| edition_id            | int                               ||
| sport                 | str (of the event)                ||
| sport_url             | web (/editions/DD/sports/SSS)     ||
| result_date           | str (date + time)                 | Standarize format (datetime) |
| result_location       | str (loc info)                    | Standarize format (city, country) |
| result_participants   | str (number of people)            ||
| result_format         | str (description on how to win)   ||
: Event Results :

| Column | Type (value) | Pre-process |
| :-: | :-: | :-- |
| edition           | str (year + event)    ||
| edition_id        | int                   ||
| edition_url       | web (/editiond/DD)    ||
| year              | int                   ||
| city              | str (name)            ||
| country_flag_url  | url (https://...)     ||
| country_noc       | str (3-letter word)   ||
| start date        | str (datetime)        | Standarize format (datetime)
| end_date          | str (datetime)        | Standarize format (datetime)
| competition_date  | str (datetimes)       | Standarize format (datetime)
: Games Summary :

| Column | Type (value) | Pre-process |
| :-: | :-: | :-- |
| edition           | str (year + event)    ||
| edition_id        | int                   ||
| year              | int                   ||
| country           | str (name)            ||
| country_noc       | str (3-letter word)   ||
| gold              | int                   ||
| silver            | int                   ||
| bronze            | int                   ||
| total             | int (sum of previous) ||
: Medal Tally History :

1) Map Data

HeatMap
Country, Sport, Discipline, Medal Tally

When Clicked
Country, Athlete, Medal Tally, Sport


2) Athlete Distributions



Notes


Make the frontend people tell us what kind of data they need to encode the visualizations they need to encode

custering on outliers, compute some extra features that are not accessible to the user otherwise, for isntance how long into their careers people were before getting their succeess

do some analysis on how many clusters to show

when preparing clusters make many different ones and make it so the user can go through the same journey?

search for specific hero
make it easy to do an exploration that is targeted


1) compare

2) task 2 is historical

focus on supporting one core visualization that is core the the analysis

focus on user success over general success

show the similarity to distributions and traits not necessaarily a specific user (similarity that the user can retrieve insights from)

