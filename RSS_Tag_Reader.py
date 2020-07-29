import feedparser
import os

os.system('cls') # clears the terminal from code, use 'clear' on linux/Mac
# https://lukesmith.xyz/rss.xml
get_input = input("Please enter the URL of the RSS file to read: ")

NewsFeed = feedparser.parse(get_input)

# len(NewsFeed[entries])
# NewsFeed.entries[0] for latest entry, NewsFeed.entries[-1] for last entry
# NewsFeed.keys() for full html tags in RSS feed
print("HTML Tags for in URL Feed: ")
useful_key = []
for keys in NewsFeed.keys():
    useful_key.append(keys)

print(useful_key)

print("\n")
print("__________________________________________________________________")
keyforuse = input("Please enter the key you want to access within RSS feed: ")
entryindex = int(input("also please enter which entry you want to see, 0 for latest, -1 for oldest: "))

keyindex = useful_key.index(keyforuse)
values = NewsFeed.values()
new_param = list(values)[keyindex][entryindex]
print(new_param)