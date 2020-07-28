import feedparser
import os

os.system('cls') # clears the terminal from code, use 'clear' on linux/Mac
# https://lukesmith.xyz/rss.xml
get_input = input("Please enter the URL of the RSS file to read: ")

NewsFeed = feedparser.parse(get_input)

# len(NewsFeed[entries])
# NewsFeed.entries[0] for latest entry, NewsFeed.entries[-1] for last entry
# NewsFeed.keys() for full html tags in RSS feed
print(NewsFeed.entries[-1])