# region Imports and modules

import feedparser
import os

# endregion

# region stable variables

# dictionaries
NewsFeed = {}

# lists
FeedList = []
simpletaglist = [] # "href", "status", "namespaces", "updated", "version", "headers", "bozo", "etag", "encoding"

# strings
get_input = ""
keyforuse = ""

# ints
keyindex = 0

# endregion

# region functions

def non_simple(FeedList, keyindex):

    entryindex = 0
    entryindex = int(input("Please enter which entry you want to see, 0 for latest, -1 for oldest: "))
    output_entry = FeedList[keyindex][entryindex]
    output_entry_keys = output_entry.keys()
    output_entry_values = output_entry.values()
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

    output_entry = FeedList[keyindex]

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