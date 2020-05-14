#!/usr/bin/env python3

# Python 2 is deprecated.  Be sure you are using Python 3 ONLY!

import requests
import sys
from datetime import datetime

# We will reuse this URL string a lot
URL = "https://api-v3.igdb.com/"
# You must register for your free key before you can complete this assignment
KEY =  "1d2106294868b4f37cfa91c4445cbad2"
# These are the headers we will send.  You may add additional if you need them.
HEADER = {'user-key':KEY, 'content-type':'application/json','fields':"*"}

# This is a Python dictionary (a hashmap) for a few endpoints I may query.
endpoints = { "1":"games", "2":"characters", "3":"genres" }

print("Thank you for using IGDB-CLI (Command Line Interface).")
print("Please enter your search term: ")
term = input()
print("Which endpoint do you wish to search?" )
print("1) Games\t2)Character\t3)Genre")
endpoint = input()

FULLURL = URL + endpoints[endpoint] + "/"
# This next line does a POST request.  It passes our headers, and then any
# Apicalypse query information in the data section.
r = requests.post(FULLURL, data='search "' + term +'";', headers = HEADER)

# Check the status code.  If it is not 200 - we have a problem!  Handle it
# appropriately.
print(r.status_code)
if r.status_code != 200:
    print("We have a problem!")
    sys.exit(1)

# Here, we declare a variable called 'data' and ask for it to parse the response
# into a json object.
data = r.json()
print(data)
big_data = []

# Here we iterate over each object in the JSON object, and perform a new
# query based on the ID field to get more information from the API.
for d in data:
    #print(d['id'])
    URL2 = URL + endpoints[endpoint] + "/"
    #print(URL2)
    r = requests.post(URL2, data='fields name,alternative_names,aggregated_rating,aggregated_rating_count,category,summary,dlcs,expansions,first_release_date,game_engines,genres; *; where id='+str(d['id'])+';', headers = HEADER)
    data = r.json()
    big_data.append(data)

#Functions for attributes that cant get their data from /games/ endpoint. ie: category
#parses time stamp and makes it into readable date
def parse_date(date_value):
    ts = int(date_value)
    print('initial release date:')
    print(tab,datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y'))
#takes category enum and converts it into its corresponding name
def parse_category(cat_enum):
    #NOTE: The documentation did not provide a url to get category enum name with its value and I tried finding it from the two links 
    # below with no luck so I just hard coded what the enums are with a conditional branch :(
        #URL_cat = 'https://api-v3.igdb.com/games/category/'
        #URL_cat = 'https://api-v3.igdb.com/category'
        #r = requests.post(URL_cat, data='fields name; *; where value='+str(cat_enum)+';', headers = HEADER)
    print('Category:')
    if(cat_enum == 0):
        print(tab, 'Main Game')
    elif(cat_enum == 1):
        print(tab, 'DLC Addon')
    elif(cat_enum == 2):
        print(tab, 'Expansion')
    elif(cat_enum == 3):
        print(tab, 'Bundle')
    elif(cat_enum == 4):
        print(tab, 'Standalone Expansion')
    elif(cat_enum == 5):
        print(tab, 'Mod')
    elif(cat_enum == 6):
        print(tab, 'Episode')
    else:
        print(tab, 'ERROR: cat_enum not between 0-6, chase really screwed the pooch on this one')

def parse_genre(genre):
    #https://api-v3.igdb.com/genres
    URL_Genre = URL + "genres/"
    print('Genre(s):')
    for i in genre:
        value = str(i)
        r = requests.post(URL_Genre, data='fields name; *; where id='+value+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])
#Takes a list of dlc id's and converts them into their name
def parse_dlc(dlcs):
    print('DLC(s):')
    for i in dlcs:
        URL_dlc = 'https://api-v3.igdb.com/games'
        r = requests.post(URL_dlc, data='fields name; *; where id='+str(i)+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])
def parse_expansion(expansions):
    print('Expansion(s):')
    for i in expansions:
        URL_exp = 'https://api-v3.igdb.com/games'
        r = requests.post(URL_exp, data='fields name; *; where id='+str(i)+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])
def parse_engines(engines):
    print('Game Engine(s):')
    for i in engines:
        url_engine = 'https://api-v3.igdb.com/game_engines/'
        r = requests.post(url_engine, data='fields name; *; where id='+str(i)+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])

    





#Interface to find more info
print('Printing results...')
num = 1
for d in big_data:
    print(num,'. ', d[0]['name'])
    #make a function to retrieve alt-names with its id
    num += 1
print('Please pick a search result')
user_number = int(input())
tab = '        '
if(user_number > num or user_number < 0):
    print('Application error: number out of bounds')
    sys.exit(1)
else:
    #Accesses data of game and makes a temp list for easy access
    #print(big_data[user_number-1])
    temp_list = big_data[user_number-1]
    #Since there its possible for some attributes to not be present ie: dlc, expansion
    #All attributes present will be added to a list to be viewed later from temp_list
    key_list = []
    for item in temp_list:
        for i in item:
            #TODO: MAKE CONDITIONALS TO FILTER string values
            if(not (i == 'id' or i == 'name')):
                #print(i)
                key_list.append(i)
    #Last loop for function calls to display attribute data and fetch enum names
    for key in key_list:
        if(key == 'aggregated_rating'):
            print('IGDB Rating:')
            print(tab, temp_list[0][key])
        elif(key == 'category'):
            parse_category(temp_list[0][key])
        elif(key == 'first_release_date'):
            parse_date(temp_list[0][key])
        elif(key == 'genres'):
            parse_genre(temp_list[0][key])
        elif(key == 'dlcs'):
            parse_dlc(temp_list[0][key])
        elif(key == 'expansions'):
            parse_expansion(temp_list[0][key])
        elif(key == 'game_engines'):
            parse_engines(temp_list[0][key])
        elif(key == 'summary'):
            print('Summary of Game:')
            print(tab, temp_list[0][key])



    #Print information
    #print('Information of Game:', temp_list[0]['name'])
    #print(tab,'Category: ',temp_list[0]['category'])
    #if(not(temp_list[0]['dlcs'] in temp_list)):
    #    print('Big weiner on campus')
    #print(tab,'DLC(s): ',temp_list[0]['dlcs'])
    #print(tab,'Expansion(s): ',temp_list[0]['expansions'])
    #print(tab,'Release Date: ',temp_list[0]['first_release_date'])
    #print(tab,'Game engine(s): ',temp_list[0]['game_engines'])
    #print(tab,'Genre(s): ',temp_list[0]['genres'])
    #print(tab,'IGDB Rating: ',temp_list[0]['aggregated_rating'])
    #print(tab,'Summary of Game: ',temp_list[0]['summary'])










