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
simpletaglist = [] 

# strings
get_input = ""
keyforuse = ""
simplekeytag = ""
entrytitle = ""
function_type = ""

# ints
keyindex = 0

# endregion

# region functions

def non_simple(FeedList, keyindex):

    global first_level
    global second_level
    global function_type
    global entrytitle

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
    subkey_title = useful_subkeys.index("title")

    entrytitle = entry_values[subkey_title]
    entry_detail = entry_values[subkey]

    return entry_detail

def simple(FeedList, keyindex):

    global first_level
    global function_type
    global simplekeytag

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
        simplekeytag = entry_use_key.copy()

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
    
    debug_dict(keyforuse, entrytitle)

def deltaglist():
    global simpletaglist
    del simpletaglist[:]

def write_json_one(data, name):

    count = 0

    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')
    
    if os.path.isfile(f"Json_Files/{name}.json"):
        count += 1
        with open (f"Json_Files/{name}_{count}.json", "w") as f:
            json.dump(data, f, indent=4, default=str)     
    else:
        count = 0
        with open (f"Json_Files/{name}.json", "w") as f:
            json.dump(data, f, indent=4, default=str)

def write_json_two(data, name):

    count = 0

    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')
         
    else:
        if os.path.isfile(f"Json_Files/{name}.json"):
            count += 1
            with open (f"Json_Files/{name}_{count}.json", "w") as f:
                json.dump(data, f, indent=4, default=str)     
        else:
            count = 0
            with open (f"Json_Files/{name}.json", "w") as f:
                json.dump(data, f, indent=4, default=str)

def write_basic_json(data, name):

    data.pop("bozo_exception", None)

    if not os.path.isdir('Json_Files/'):
        os.mkdir('Json_Files/')

    with open(f"Json_Files/{name}.json", 'w') as fp:
        json.dump(data, fp, indent=4)

def debug_dict(keyforuse, entrytitle):

    print("____________________________________________")
    print("\n")
    if bool(NewsFeed):
        print("First level keys: ")
        print(NewsFeed.keys())
        write_basic_json(NewsFeed, "RSS_Feed")
        print("\n")
        if bool(first_level):
            print("Second level keys: ")
            print(first_level.keys())
            write_json_one(first_level, keyforuse)
        elif bool(second_level):
            print("Third Level keys: ")
            print(second_level.keys())
            write_json_two(second_level, entrytitle)
        else:
            print("Dictionary is empty on all levels except zero(First level)!")
    
    # empty function_type string var
    function_type = ""
    keyforuse = ""
    entrytitle = ""

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

# endregion

# region execution

intro()

# endregion