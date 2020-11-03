import json
import os
import feedparser

# region Variables

NewsFeed = {}

NewsFeed_Name = ""

# endregion

class JsonMaker:

    def __init__(self):

        # if folder to store json_files is not found, create one
        if not os.path.isdir('Json_Files/'):
            os.mkdir('Json_Files/')
        else:
            pass

    # this function will find a json file from given name, and set that to the appropriate dicts
    def readFromJson(self):

        if len(os.listdir('Json_Files/')) == 0:
            print("Directory is empty")
        else:    
            f = open(f"Json_Files/{NewsFeed_Name}.json")
            NewsFeed = json.load(f)
            f.close()
            print(NewsFeed.keys())

    def makeWholeJSON(self, name, feed):

        global NewsFeed
        global NewsFeed_Name

        NewsFeed_Name = name

        # feed parse the RSS url feed into a dictionary called NewsFeed
        NewsFeed = feedparser.parse(feed)

        print(NewsFeed.keys())

        # remove "bozo_exception" key since that causes an error in json file
        NewsFeed.pop("bozo_exception", None)

        # create json file for url RSS feed
        with open(f"Json_Files/{name}.json", 'w') as fp:
            json.dump(NewsFeed, fp, indent=4)
    
    def getEntries(self):

        print(NewsFeed.keys())

        entries = NewsFeed.entries

        print(entries[0].keys())

        for i in range(len(entries)):
            title = entries[i].published
            # create json file for url RSS feed
            with open(f"Json_Files/{i}.json", 'w') as fp:
                json.dump(entries[i], fp, indent=4)

        

