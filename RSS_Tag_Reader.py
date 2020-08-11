# region Imports and modules

import feedparser
import os
import json

# endregion

# region stable variables

# dictionaries
NewsFeed = {}
first_level = {}
second_level = {}

# lists
FeedList = []
simpletaglist = [] # "href", "status", "namespaces", "updated", "version", "headers", "bozo", "etag", "encoding"

# strings
get_input = ""
keyforuse = ""
function_type = ""

# ints
keyindex = 0

# endregion

# region functions

def non_simple(FeedList, keyindex):

    global first_level
    global second_level
    global function_type

    function_type = "non_simple"

    entryindex = 0
    entryindex = int(input("Please enter which entry you want to see, 0 for latest, -1 for oldest: "))
    output_entry = FeedList[keyindex]

    if isinstance(output_entry, dict):
        first_level = output_entry.copy()

    output_entry_2 = output_entry[entryindex]
    if isinstance(output_entry_2, dict):
        second_level = output_entry_2.copy()

    output_entry_keys = output_entry_2.keys()
    output_entry_values = output_entry_2.values()
    entry_keys = list(output_entry_keys)
    entry_values = list(output_entry_values)

    print("Keys found in entry: ")
    print(entry_keys)
    entry_use_key = input("Please enter the entry key you want to see: ")
    print("\n")

    useful_subkeys = []
    for keys in output_entry_keys:
        useful_subkeys.append(keys)

    subkey = useful_subkeys.index(entry_use_key)

    entry_detail = entry_values[subkey]

    return entry_detail

def simple(FeedList, keyindex):

    global first_level
    global function_type

    function_type = "simple"
    output_entry = FeedList[keyindex]
    if isinstance(output_entry, dict):
        first_level = output_entry.copy()

    try:
        output_entry_keys = output_entry.keys()
        output_entry_values = output_entry.values()
        entry_keys = list(output_entry_keys)
        entry_values = list(output_entry_values)

        print("Keys found in entry: ")
        print("\n")
        print(entry_keys)
        print("\n")
        entry_use_key = input("Please enter the entry key you want to see: ")

        useful_subkeys = []
        for keys in output_entry_keys:
            useful_subkeys.append(keys)

        subkey = useful_subkeys.index(entry_use_key)

        entry_detail = entry_values[subkey]

        return entry_detail

    except:
        return output_entry

def find_url_tags(NewsFeed):

    global simpletaglist
    global FeedList
    global keyindex
    global keyforuse

    FeedList = list(NewsFeed.values())

    print("HTML Tags for in URL Feed: ")
    for keys in NewsFeed.keys():
        simpletaglist.append(keys)

    print(simpletaglist)

    print("\n")
    print("__________________________________________________________________")
    keyforuse = input("Please enter the key you want to access within RSS feed: ")
    print("\n")
    keyindex = simpletaglist.index(keyforuse)

    simpletaglist.remove("entries")

def sorter():

    if keyforuse == "entries":
        print(non_simple(FeedList, keyindex))
    elif any(x == keyforuse for x in simpletaglist):
        print(simple(FeedList, keyindex))
    else:
        return "RSS Feed Read is done!"

def deltaglist():
    global simpletaglist
    del simpletaglist[:]

def debug_dict():

    print("____________________________________________")
    print("\n")
    if bool(NewsFeed):
        print("First level keys: ")
        print(NewsFeed.keys())
        write_basic_json(NewsFeed, "NewsFeed.json")
        print("\n")
        if bool(first_level):
            print("Second level keys: ")
            print(first_level.keys())
            write_json_one(first_level, "level_one.json")
        elif bool(second_level):
            print("Third Level keys: ")
            print(second_level.keys())
            write_json_two(second_level, "level_two.json")
        else:
            print("Dictionary is empty on all levels except zero(First level)!")
    
    # empty function_type string var
    function_type = ""

def write_json_one(data, name):

    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')
    
    if os.path.isfile(f"Json_Files/{name}"):
        with open (f"Json_Files/{name}", "r+") as f:
            g = json.load(f)
            g.update(data) 
            f.seek(2)
            json.dump(g, f, indent=4, default=str)     
    else:
        with open (f"Json_Files/{name}", "w") as f:
            json.dump(data, f, indent=4, default=str)

def write_json_two(data, name):

    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')
         
    else:
        with open (f"Json_Files/{name}", "w") as f:
            json.dump(data, f, indent=4, default=str)

def write_basic_json(data, name):

    data.pop("bozo_exception", None)

    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')

    with open(f"Json_Files/{name}", 'w') as fp:
        json.dump(data, fp, indent=4)

def intro():

    global get_input
    global NewsFeed

    os.system('cls') # clears the terminal from code, use 'clear' on linux/Mac

    print("Hello welcome to RSS Reader!")
    print("____________________________________________________________________________")
    # https://lukesmith.xyz/rss.xml
    get_input = input("Please enter the URL of the RSS file to read: ")

    NewsFeed = feedparser.parse(get_input)

    find_url_tags(NewsFeed)

    sorter()

    deltaglist()

    debug_dict()

# endregion

# region execution

intro()

# endregion