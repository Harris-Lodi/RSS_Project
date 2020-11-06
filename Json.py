import json
import os
import feedparser
from pandas import DataFrame 
from bs4 import BeautifulSoup

# region Variables

df = DataFrame()

NewsFeed = {}

NewsFeed_Name = ""

# endregion

class JsonMaker:

    def __init__(self):

        global NewsFeed_Name
        global df

        NewsFeed_Name = ""
        df = DataFrame()

        # if folder to store json_files is not found, create one
        if not os.path.isdir('Json_Files/'):
            os.mkdir('Json_Files/')
        else:
            self.readFromJson(0)

    # this function will find a json file from given name, and set that to the appropriate dicts
    def readFromJson(self, directory_Index):

        global NewsFeed
        global NewsFeed_Name

        names_list = []
        d_Index = int()

        # print(d_Index)
        # print(NewsFeed_Name)

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
            # print(d_Index)
            # print(names_list)
            # if d_Index is positive and names_list is not empty:
            if not names_list == []:
                # assign a specific name to NewsFeed_names bases on index value!
                NewsFeed_Name = names_list[d_Index]
                # print(NewsFeed_Name)
                # recursivly re-try re-loading NewsFeed
                self.readFromJson(d_Index)
            else:
                pass

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

            self.makeCSV(entries)

            print(entries[0].keys())

            for i in range(len(entries)):
                # create json file for url RSS feed
                with open(f"Json_Files/{NewsFeed_Name}/{i}.json", 'w') as fp:
                    json.dump(entries[i], fp, indent=4)
        else:
            print('NewsFeed was not set to main.json!')

    # function to make a Pandas DataFrame with the Feed entries, and then save that dataframe to CSV file
    def makeCSV(self, entries):

        global df

        ID = []
        Link = []
        Name = []
        Date = []
        Summary = []

        for id in range(len(entries)):

            # clean summary text with BS4
            raw_html = entries[id]["summary"]
            cleantext = BeautifulSoup(raw_html, "lxml").text
            
            # try setting link to 'link' key from JSON, if keyerror, use 'id', else "N/A"
            try:
                link = entries[id]["link"]
            except KeyError:
                link = entries[id]["id"]
            except:
                link = "N/A"

            ID.append(id)
            Link.append(link)
            Name.append(entries[id]["title"])
            Date.append(entries[id]["published"])
            Summary.append(cleantext)

        JSON_Dict = {
            'ID': ID,
            'Titles': Name,
            'Published': Date,
            'Link': Link,
            'Summary': Summary,
        }

        df = DataFrame(JSON_Dict)

        # saving the DataFrame as a CSV file 
        save_csv_data = df.to_csv('Entries.csv', index = True) 

    # Test variables values for debugging and testing
    def testVariables(self):

        if not NewsFeed == {}:

            print(NewsFeed.keys())
            print(NewsFeed_Name)
        
        if df.empty:
            print('is null')
        else:
            print("not null!")