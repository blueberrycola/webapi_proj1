#!/usr/bin/env python3

# Python 2 is deprecated.  Be sure you are using Python 3 ONLY!

import requests
import sys

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
    #Print information
    print('Information of Game:', temp_list[0]['name'])
    print(tab,'Category: ',temp_list[0]['category'])
    #print(tab,'DLC(s): ',temp_list[0]['dlcs'])
    #print(tab,'Expansion(s): ',temp_list[0]['expansions'])
    print(tab,'Release Date: ',temp_list[0]['first_release_date'])
    #print(tab,'Game engine(s): ',temp_list[0]['game_engines'])
    print(tab,'Genre(s): ',temp_list[0]['genres'])
    print(tab,'IGDB Rating: ',temp_list[0]['aggregated_rating'])
    print(tab,'Summary of Game: ',temp_list[0]['summary'])










