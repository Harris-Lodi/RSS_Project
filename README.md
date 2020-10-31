# RSS_Project
 A Python project to get RSS Feeds without needing a terminal, convenient for windows users!

 <b>Requirements:</b> <br />

 feedparser - pip3 install feedparser<br />
 pandas - pip3 install pandas<br />
 sqlite3 - pip3 install pysqlite3<br />
 pyperclip - pip install pyperclip<br />

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

 <b> Haitus Update: (Back from Haitus!)</b><br />

 Need to make static variables that can be set from GUI and Get from backend and front end as well.<br />
 This will require rewriting the entire back end into a class, and initializing the variables in an init function.<br />
 Also need to re-write the front end to work with the new back end and remove all redundant functions and code from the project.<br />
 This is a lot of work, thus this project is in haitus until I have enough time to come back to it(until further notice)!<br />
 
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

