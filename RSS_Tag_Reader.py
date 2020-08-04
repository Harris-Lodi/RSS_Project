import feedparser
import os

os.system('cls') # clears the terminal from code, use 'clear' on linux/Mac
# https://lukesmith.xyz/rss.xml
get_input = input("Please enter the URL of the RSS file to read: ")

NewsFeed = feedparser.parse(get_input)
# "href", "status", "namespaces", "updated", "version", "headers", "bozo", "etag", "encoding"
simpletaglist = []

def non_simple(FeedList, keyindex):

    entryindex = 0
    print("\n")
    entryindex = int(input("also please enter which entry you want to see, 0 for latest, -1 for oldest: "))
    output_entry = FeedList[keyindex][entryindex]
    output_entry_keys = output_entry.keys()
    output_entry_values = output_entry.values()
    entry_keys = list(output_entry_keys)
    entry_values = list(output_entry_values)

    print(output_entry)
    print("\n")
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

    print(entry_detail)

def simple(FeedList, keyindex):

    output_entry = FeedList[keyindex]

    try:
        output_entry_keys = output_entry.keys()
        output_entry_values = output_entry.values()
        entry_keys = list(output_entry_keys)
        entry_values = list(output_entry_values)

        print(output_entry)
        print("\n")
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

        print(entry_detail)

    except:
        print(output_entry)

def find_url_tags():

    global simpletaglist

    FeedList = list(NewsFeed.values())

    print("HTML Tags for in URL Feed: ")
    useful_key = []
    for keys in NewsFeed.keys():
        useful_key.append(keys)

    simpletaglist = useful_key.copy()
    simpletaglist.remove("entries")
    print(useful_key)

    print("\n")
    print("__________________________________________________________________")
    keyforuse = input("Please enter the key you want to access within RSS feed: ")
    print("\n")
    keyindex = useful_key.index(keyforuse)

    if keyforuse == useful_key[keyindex] == "entries":
        non_simple(FeedList, keyindex)
    elif any(x == keyforuse for x in simpletaglist):
        simple(FeedList, keyindex)
    else:
        return "RSS Feed Read is done!"

    del simpletaglist[:]

find_url_tags()