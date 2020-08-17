# region Imports and modules

import feedparser
import os
import json
import re
import sqlite3
from datetime import datetime

# endregion

# region stable variables


# dictionaries
NewsFeed = {}
first_level = {}
second_level = {}

# lists
FeedList = []
simpletaglist = [] 
entryDates = []
entryNames = []
entryID = []
entrySummaries = []
entryLink = []

# strings
get_input = ""
keyforuse = ""
simplekeytag = ""
entrytitle = ""
function_type = ""
unwanted = "!@#$;:!*%)(&^~?/" # list of unwanted characters for entrytitle

# ints
keyindex = 0

# endregion

# region functions

# function to output data for specific RSS entries
def non_simple(FeedList, keyindex):

    # global vars
    global first_level
    global second_level
    global function_type
    global entrytitle

    # set function type to non simple
    function_type = "non_simple"

    # find specific entry from entries list from user input, change this later to select by dates/title
    entryindex = 0
    entryindex = int(input("Please enter which entry you want to see, 0 for latest, -1 for oldest: "))
    output_entry = FeedList[keyindex]

    # set first_level to outputentry dict 
    if isinstance(output_entry, dict):
        first_level = output_entry.copy()

    # set second level to dict from specific entry that user requested
    output_entry_2 = output_entry[entryindex]
    if isinstance(output_entry_2, dict):
        second_level = output_entry_2.copy()

    # assign keys and values from output_entry_2 to seperate lists
    output_entry_keys = output_entry_2.keys()
    output_entry_values = output_entry_2.values()
    entry_keys = list(output_entry_keys)
    entry_values = list(output_entry_values)

    # ask user for which entry they want
    print("Keys found in entry: ")
    print(entry_keys)
    entry_use_key = input("Please enter the entry key you want to see: ")
    print("\n")

    # find indexes for title, and for key requested by user
    subkey = entry_keys.index(entry_use_key)
    subkey_title = entry_keys.index("title")

    # find values for index keys found above, temptitle value is assigned here
    temptitle = entry_values[subkey_title]
    entry_detail = entry_values[subkey]

    # assign entrytitle and remove unwanted characters from the title
    entrytitle = ''.join( c for c in temptitle if c not in unwanted )

    # return value user requested
    return entry_detail

# function to output data for non entries RSS tags
def simple(FeedList, keyindex):

    # global vars
    global first_level
    global function_type
    global simplekeytag
 
    # set function_type to simple, assign output_entry based on selected input key
    # also make first_level a copy of the output_entry dict
    function_type = "simple"
    output_entry = FeedList[keyindex]
    if isinstance(output_entry, dict):
        first_level = output_entry.copy()

    # if the output has tag, try the following, except no tags, just output the data
    try:

        # assign keys and values from output_entry to seperate lists
        output_entry_keys = output_entry.keys()
        output_entry_values = output_entry.values()
        entry_keys = list(output_entry_keys)
        entry_values = list(output_entry_values)

        # ask user for which entry they want, save entry to simplekeytag
        print("Keys found in entry: ")
        print("\n")
        print(entry_keys)
        print("\n")
        entry_use_key = input("Please enter the entry key you want to see: ")
        simplekeytag = entry_use_key.copy()

        # find specific key index from keys list based on index from user input
        subkey = entry_keys.index(entry_use_key)

        # find the value the user requests from subkey index var
        entry_detail = entry_values[subkey]

        # return the requested value
        return entry_detail

    # in the case there are no tags in feed
    except:

        # just output the values found
        return output_entry

# takes RSS url and organizes tags for sorting in simpletaglist
def find_url_tags(NewsFeed):

    # global vars
    global simpletaglist
    global FeedList
    global keyindex
    global keyforuse

    # convert values from Newsfeed into a list for use in output functions
    FeedList = list(NewsFeed.values())

    # store keys in simpletaglist and output them
    print("HTML Tags for in URL Feed: ")
    for keys in NewsFeed.keys():
        simpletaglist.append(keys)

    print(simpletaglist)

    # ask user for which key they want to see, and store the input/index value of input
    print("\n")
    print("__________________________________________________________________")
    keyforuse = input("Please enter the key you want to access within RSS feed: ")
    print("\n")
    keyindex = simpletaglist.index(keyforuse)

    # remove entries from simple tag list to avoid double function call
    simpletaglist.remove("entries")

# decided which function to use depending on selected key tag
def sorter():

    # decide which output function to call based upon key tag
    if keyforuse == "entries":
        print(non_simple(FeedList, keyindex))
    elif any(x == keyforuse for x in simpletaglist):
        print(simple(FeedList, keyindex))
    else:
        return "RSS Feed Read is done!"
    
    # debug for testing
    debug_dict(keyforuse, entrytitle)

# function to create database if not already made
def createDatabase():

    tableName = "Feed_Table"

    #searches for database with name provided to connect to, if no db found, it will create one
    conn = sqlite3.connect('Database.db')

    # create cursor to edit and work the database
    c = conn.cursor()

    # create table, execute function launches parameter commands to database, 
    # paranthesis in table name define the table dimensions and properties,
    # IF NOT EXISTS should return null instead of errors if the table already exists
    # also the string format matters alot to avoid syntax errors
    c.execute("""CREATE TABLE IF NOT EXISTS Feed_table (
        indx INTEGER, 
        title TEXT, 
        dates TEXT, 
        summary TEXT,
        id TEXT,
        link TEXT
        ) """)

    # commit changes to database
    conn.commit()

    #close database connection
    conn.close()

# function to save entries in sql file
def save_entries(NewsFeed):

    foundEntries = NewsFeed["entries"]

    global entryDates
    global entryNames
    global entryID
    global entrySummaries
    global entryLink
    
    for item in foundEntries:

        id = item["id"] 

        entryDates.append(item["published"])
        entryNames.append(item["title"])
        entryID.append(id)
        entrySummaries.append(item["summary"])
        try:
            entryLink.append(item["link"])
        except KeyError:
            print(f"the link key for item {id} was not found!")

    # insert entries into sql table
    for indx, element in enumerate(entryNames):

        date = entryDates[indx]
        summarize = entrySummaries[indx]
        tagid = entryID[indx]
        link = entryID[indx]

        parameters = [indx, element, date, summarize, tagid, link]

        # Create a database or connect to one
        conn = sqlite3.connect('Database.db')
        # Create cursor
        c = conn.cursor()

        # update table, insert data to table
        c.execute("INSERT INTO Feed_table VALUES (?, ?, ?, ?, ?, ?)", parameters)

        #Commit Changes
        conn.commit()

        # Close Connection 
        conn.close()

# clears lists
def delLists():

    global simpletaglist
    global entryDates
    global entryNames
    global entryID
    global entrySummaries
    global entryLink

    del simpletaglist[:]
    del entryDates[:]
    del entryNames[:]
    del entryID[:]
    del entrySummaries[:]
    del entryLink[:]

# writes json file for non entries feeds
def write_json_one(data, name):

    # counts the number of repeated file names
    count = 0

    # if folder to store json_files is not found, create one
    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')
    
    # create json file if none exists, if there is already one with the same name
    # then create another json file with the value of count added to the name
    if os.path.isfile(f"Json_Files/{name}.json"):
        count += 1
        with open (f"Json_Files/{name}_{count}.json", "w") as f:
            json.dump(data, f, indent=4, default=str)     
    else:
        count = 0
        with open (f"Json_Files/{name}.json", "w") as f:
            json.dump(data, f, indent=4, default=str)

# writes json files for entries feeds only
def write_json_two(data, name):

    # if folder to store json_files is not found, create one
    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')
    
    # create json file if none exists, if there is already one with the same name
    # then create another json file with the value of count added to the name
    if not os.path.isfile(f"Json_Files/{name}.json"):   
        with open (f"Json_Files/{name}.json", "w") as f:
            json.dump(data, f, indent=4, default=str)

# writes json file for the url RSS feed itself
def write_basic_json(data, name):

    # remove "bozo_exception" key since that causes an error in json file
    data.pop("bozo_exception", None)

    # if folder to store json_files is not found, create one
    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')

    # create json file for url RSS feed
    with open(f"Json_Files/{name}.json", 'w') as fp:
        json.dump(data, fp, indent=4)

# debuging function, also controls outputs and which json functions are launched
def debug_dict(keyforuse, entrytitle):

    print("____________________________________________")
    print("\n")

    # if Newsfeed/first_level/second_level dicts are not empty
    # then do the following to create json files for each dict
    # and output availible keys for each dict
    if bool(NewsFeed):
        # print("First level keys: ")
        # print(NewsFeed.keys())
        write_basic_json(NewsFeed, "RSS_Feed")
        print("\n")
        if bool(first_level):
            # print("Second level keys: ")
            # print(first_level.keys())
            write_json_one(first_level, keyforuse)
        elif bool(second_level):
            # print("Third Level keys: ")
            # print(second_level.keys())
            write_json_two(second_level, entrytitle)
        else:
            print("Dictionary is empty on all levels except zero(First level)!")
    
    # empty function_type string var
    function_type = ""
    keyforuse = ""
    entrytitle = ""

# starting function, need to change this for user input function with flask html
def intro():

    # global variables
    global get_input
    global NewsFeed

    # clear the terminal 
    os.system('cls') # clears the terminal from code, use 'clear' on linux/Mac

    # get the RSS Feed URL from user
    print("Hello welcome to RSS Reader!")
    print("____________________________________________________________________________")
    # https://lukesmith.xyz/rss.xml
    get_input = input("Please enter the URL of the RSS file to read: ")

    # feed parse the RSS url feed into a dictionary called NewsFeed
    NewsFeed = feedparser.parse(get_input)

    # Invoke the find url tags function with NewsFeed as input, 
    # create a front end that does this via user request only
    find_url_tags(NewsFeed)

    # use sorter after find url tags function is ran,
    # create a front end that does this via user request only
    sorter()

    # save keys/value pairs in lists to be used in SQL table for all entries found
    save_entries(NewsFeed)

    # delete lists that need to be clear after script is done running,
    # create a front end that does this via user request only
    delLists()

# endregion

# region execution

intro()
createDatabase()

# endregion