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
            self.readFromJson(0)

    # this function will find a json file from given name, and set that to the appropriate dicts
    def readFromJson(self, directory_Index):

        global NewsFeed
        global NewsFeed_Name

        NewsFeed_Name = ""
        names_list = []
        d_Index = int()

        print(d_Index)
        print(NewsFeed_Name)

        if not NewsFeed_Name == "":
            if not len(os.listdir('Json_Files/')) == 0:   
                f = open(f"Json_Files/{NewsFeed_Name}/main.json")
                NewsFeed = json.load(f)
                f.close()
                # print(NewsFeed.keys())
            else:
                pass 
        else:
            # get the names of the immediate child directories of 'Json_Files'
            names_list = next(os.walk('Json_Files/'))[1]
            # set index based on the directory name given, if input is not an integer:
            if isinstance(directory_Index, str):
                d_Index = names_list.index(directory_Index)
                # print("if: ", d_Index)
            else:
                d_Index = directory_Index
                # print("else: ", d_Index)
            # assign a specific name to NewsFeed_names bases on index value!
            NewsFeed_Name = names_list[d_Index]
            # print(NewsFeed_Name)
            # recursivly re-try re-loading NewsFeed
            self.readFromJson(d_Index)

    # create main.json file from the entire JSON file!
    def makeWholeJSON(self, name, feed):

        global NewsFeed
        global NewsFeed_Name

        NewsFeed_Name = name

        # feed parse the RSS url feed into a dictionary called NewsFeed
        NewsFeed = feedparser.parse(feed)

        # remove "bozo_exception" key since that causes an error in json file
        NewsFeed.pop("bozo_exception", None)

        # create json file for url RSS feed
        if not os.path.isdir(f'Json_Files/{name}'):
            os.mkdir(f'Json_Files/{name}')
            with open(f"Json_Files/{name}/main.json", 'w') as fp:
                json.dump(NewsFeed, fp, indent=4)
        else:
            pass
    
    # create JSON files for each entry in RSS feed
    def getEntries(self):

        if not NewsFeed == {}:

            # print(NewsFeed.keys())

            entries = NewsFeed['entries']

            print(entries[0].keys())

            for i in range(len(entries)):
                # create json file for url RSS feed
                with open(f"Json_Files/{NewsFeed_Name}/{i}.json", 'w') as fp:
                    json.dump(entries[i], fp, indent=4)
        else:
            print('NewsFeed was not set to main.json!')

    # Test variables values for debugging and testing
    def testVariables(self):

        if not NewsFeed == {}:

            print(NewsFeed.keys())
            print(NewsFeed_Name)
