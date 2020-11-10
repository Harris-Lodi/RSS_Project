import json
import os
import feedparser
from pandas import DataFrame 
from bs4 import BeautifulSoup
import sqlite3
from pathlib import Path
import shutil

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
        
        # if folder to store csv files is not found, create one
        if not os.path.isdir('CSV_Files/'):
            os.mkdir('CSV_Files/')
        else:
            pass

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
                entries = NewsFeed['entries']
                self.makeCSV(entries)
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

        # if folder to store csv files is not found, create one
        if os.path.isdir('CSV_Files/'):
            # saving the DataFrame as a CSV file 
            save_csv_data = df.to_csv(f'CSV_Files/{NewsFeed_Name}.csv', index = True)
            print("Dataframe made!")
        else:
            os.mkdir('CSV_Files/')
            print("Run makeCSV function again!")

    # function to clear JSON Files
    def wipeJSON(self):

        # if folder to store json_files is not found, pass
        # create a list for all children in directory, and delete them using shutil
        if os.path.isdir('Json_Files/'):

            myjsondir = [ f.path for f in os.scandir('Json_Files/') if f.is_dir() ]
            # print(myjsondir)
            # print(type(myjsondir))
            try:
                for i in myjsondir:
                    jpath = Path(f'{i}')
                    shutil.rmtree(jpath)
            except OSError as e:
                print("Error: %s : %s" % (myjsondir, e.strerror))
        else:
            print("Something went wrong deleting json")
    
    # function to delete all CSV files
    def wipeCSV(self):

        # function to delete csv files
        if os.path.isdir('CSV_Files/'):

            mycsvdir = [ f.path for f in os.scandir('CSV_Files/') if f.is_file() ]
            # print(mycsvdir)
            # print(type(mycsvdir))
            try:
                for i in mycsvdir:
                    cpath = Path(f'{i}')
                    os.remove(f'{cpath}')
            except OSError as e:
                print("Error: %s : %s" % (mycsvdir, e.strerror))
        else:
            print("Something went wrong deleting csv")

    # region Database functions

    # function to create database
    def makeDB(self, db, table):

        # Create a database or connect to one
        conn = sqlite3.connect(f'{db}.db')
        # Create cursor
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {table}")
        c.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
                ID INTEGER, 
                Titles TEXT, 
                Published TEXT, 
                Link TEXT,
                Summary TEXT
                ) """)
        #Commit Changes
        conn.commit()
        # Close Connection 
        conn.close()

    # function to convert Dataframe to SQL
    def convertToSQL(self, db, table):
        # if the dataframe is not empty:
        if not df.empty:
            # Create a database or connect to one
            conn = sqlite3.connect(f'{db}.db')
            # Create cursor
            c = conn.cursor()
            # convert dataframe to sql
            df.to_sql(f'{table}', conn, if_exists='replace', index=False)
            # Commit Changes
            conn.commit()
            # Close Connection 
            conn.close()
        else:
            print("Dataframe was empty!")

    # delete query from record
    def deleteDatabaseEntry(self, db, table, orderID):

        # Create a database or connect to one
        conn = sqlite3.connect(f'{db}.db')
        # Create cursor
        c = conn.cursor()

        #delete a row from the table
        entry = (orderID,)
        c.execute(f"DELETE FROM {table} WHERE ID = ?;",entry)

        #Commit Changes
        conn.commit()
        # Close Connection 
        conn.close()

    # update table function
    def updateTable(db, tableName, orderID, _title = None, _date = None, _summary = None, _link = None):

        # Create a database or connect to one
        conn = sqlite3.connect(f'{db}.db')
        # Create cursor
        c = conn.cursor()

        # update table, insert data to table
        c.execute(f"""UPDATE {tableName} SET
        Titles = :title,
        Published = :date,
        Summary = :sum,
        Link = :link
        WHERE ID = :tID""", 
        {
            'title': _title,
            'date': _date,
            'sum': _summary,
            'link': _link,
            'tID': orderID
        })

        #Commit Changes
        conn.commit()
        # Close Connection 
        conn.close()

    # endregion

    # Test variables values for debugging and testing
    def testVariables(self):

        if not NewsFeed == {}:

            print(NewsFeed.keys())
            print(NewsFeed_Name)
        
        if df.empty:
            print('is null')
        else:
            print("not null!")
