#!/usr/bin/env python3

# Python 2 is deprecated.  Be sure you are using Python 3 ONLY!

import requests
import sys
from datetime import datetime
#tab needed to seperate attribute name with it's data ie: alt-names and rating
tab = '        '
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
big_data = []

# Here we iterate over each object in the JSON object, and perform a new
# query based on the ID field to get more information from the API.
for d in data:
    URL2 = URL + endpoints[endpoint] + "/"
    r = requests.post(URL2, data='fields name,alternative_names,aggregated_rating,aggregated_rating_count,category,summary,dlcs,expansions,first_release_date,game_engines,genres; *; where id='+str(d['id'])+';', headers = HEADER)
    data = r.json()
    big_data.append(data)

#parses time stamp and makes it into readable date, void function
def parse_date(date_value):
    ts = int(date_value)
    print('initial release date:')
    print(tab,datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y'))
#takes category enum and converts it into its corresponding name, void function
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
#Prints the genre of the game you selected, void function
def parse_genre(genre):
    #https://api-v3.igdb.com/genres
    URL_Genre = URL + "genres/"
    print('Genre(s):')
    for i in genre:
        value = str(i)
        r = requests.post(URL_Genre, data='fields name; *; where id='+value+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])
#Takes a list of game id's and display them. Used for parsing alt-names, expansions, and dlc,
    #void function
def parse_games(games):
    for i in games:
        URL_dlc = 'https://api-v3.igdb.com/games'
        r = requests.post(URL_dlc, data='fields name; *; where id='+str(i)+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])
#Takes a list of game engine id's and parses them into its name, void function
def parse_engines(engines):
    print('Game Engine(s):')
    for i in engines:
        url_engine = 'https://api-v3.igdb.com/game_engines/'
        r = requests.post(url_engine, data='fields name; *; where id='+str(i)+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])
#Finds the alternative names of a game since the /games/:id != /alternative_names/:id, void function
def parse_altnames(altnames):
    urlalt = 'https://api-v3.igdb.com/alternative_names'
    for i in altnames:
        r = requests.post(urlalt, data='fields name; *; where id='+str(i)+';', headers = HEADER)
        string = r.json()
        print(tab, string[0]['name'])
print('Printing results...')
num = 1
#Prints game name and its alt names
for d in big_data:
    print(num,'. ', d[0]['name'])
    if('alternative_names' in d[0]):
        print('Alternative Name(s):')
        parse_altnames(d[0]['alternative_names'])
    num += 1
print('Please pick a search result')
user_number = int(input())
#Constraint to make sure user does not go over or under value
if(user_number > num or user_number < 1):
    print('Application error: number out of bounds')
    sys.exit(1)
else:
    #Accesses data of game and makes a temp list for easy access of just the specific game
    temp_list = big_data[user_number-1]
    #Nested loop responsible for calling functions for attributes ie: ['category'], ['genres']
    for item in temp_list:
        for i in item:
            if(not (i == 'id' or i == 'name')):
                if(i == 'aggregated_rating'):
                    print('IGDB Rating:')
                    print(tab, temp_list[0][i])
                elif(i == 'category'):
                    print('Category:')
                    parse_category(temp_list[0][i])
                elif(i == 'first_release_date'):
                    print('Release Date:')
                    parse_date(temp_list[0][i])
                elif(i == 'genres'):
                    print('Genre(s)')
                    parse_genre(temp_list[0][i])
                elif(i == 'dlcs'):
                    print('DLC(s):')
                    parse_games(temp_list[0][i])
                elif(i == 'expansions'):
                    print('Expansion(s):')
                    parse_games(temp_list[0][i])
                elif(i == 'game_engines'):
                    print('Game Engine(s):')
                    parse_engines(temp_list[0][i])
                elif(i == 'summary'):
                    print('Summary of Game:')
                    print(tab, temp_list[0][i])