# RSS_Project
 A Python project to get RSS Feeds without needing a terminal, convenient for windows users!

 <b>Requirements:</b> <br />
 
 Python 3.8.5 or above <br />
 feedparser - pip3 install feedparser - https://pypi.org/project/feedparser/<br />
 pandas - pip3 install pandas - https://pypi.org/project/pandas/<br />
 sqlite3 - pip3 install pysqlite3 - https://docs.python.org/3/library/sqlite3.html<br />
 pyperclip - pip install pyperclip - https://pypi.org/project/pyperclip/<br />
 Beautiful Soup 4 - pip install beautifulsoup4 - https://pypi.org/project/beautifulsoup4/<br />
 Path - pip install pathlib - https://pypi.org/project/pathlib/<br />
 Shutil - pip install shutil - https://docs.python.org/3/library/shutil.html<br />
 
 On Linux:
 
 tkinter: sudo apt-get install python3-tk

 <b>Credits</b><br />

 Icons made by Freepik from www.flaticon.com<br />

 <b>Debugging Tools</b><br />
 
 sqlitebrowser - https://sqlitebrowser.org/<br />

 <b>Notes: </b><br />
 NewsFeed = feedparser.parse(get_input): gets html parsed data from input RSS url<br />
 NewsFeed.keys() for full list of html tags in RSS feed, doesn't include html tags for an entry <br />
 NewsFeed.entries[0] for latest entry, NewsFeed.entries[-1] for oldest entry<br />
 len(NewsFeed[entries]) to get the number of items or entries in feed<br />
 entry = NewsFeed.entries[#] will assign a specific article/item/entry to the variable entry<br />
 entry.keys() will out the html tags for that specific entry<br />

 <b>Creating the .exe:</b><br />
 - Open CMD prompt as admin in the project folder in windows!
 - ensure pip is installed and python version is atleast 3.8.5 or higher (for current build 3.8.5 is ideal)!
 - run 'pip install pyinstaller'
 - to build the executable: run 'pyinstaller --onefile --windowed --icon="Icons/RSS_Icon.ico" main.py'
 - after it runs, delete 'binaries' folder, 'main.spec' file, and move executable to the main directory and delete 'dist' folder to keep it tidy
 
 <b>Program Features List:</b><br />
 <ul>
  <li> Have a button to convert the entire page to JSON </li>
  <li> Create a JSON file that only contains the header data </li>
  <li> Have a button to delete all JSON files from JSON folder that the app creates</li>
  <li> Have a button to delete specific JSON entry when selected in listbox</li>
  <li> A button to create a list of entries by index to JSON (while showing entry name and date on GUI) </li>
  <li> Have a button to create database by given name (upon creation add in all data from header) </li>
  <li> A button to update the database with entries (and header data) from JSON entries list (and JSON header data) </li>
  <li> Include list box showing the database (Index, Title, Date, Link) with capabilities to left click on database row and have index selected in focus </li>
  <li> Have buttons to update, read, and delete entries after a row is focused on and pushing the corresponding button </li>
  <li> Have a box to show summary, title, and date upon left clicking the entry in list box </li>
  <li> Also have displays that show all the other info that is in the header related to the RSS page </li>
 </ul><br />

 <b>TO DO List:</b><br />
 <ul>
  <li> Make the program clear Databases folder when there is more then one Database, currently can only delete the database when there is only one DB! </li>
  <li> Add functionality to the 'Find Directory' function to select database and table by name when button is clicked, need to update table in GUI as well! </li>
  <li> Add functionaltiy to add new entries to all relevant Databases when new entries are found in RSS Feed, need to make the whole process more automated as well! </li>
  <li> Need to create a new list box and database file to store header data from RSS feed about the feed itself, not just the entries data! </li>
 <li> Need to change the tkinter icon line to make it functional with Linux, the tkinter iconbitman function seems to be bugged for Linux OS! </li>
 </ul><br />

