import feedparser #pip3 install feedparser
import os

#clear the terminal
os.system('cls') # clears the terminal from code, use 'clear' on linux/Mac

# get RSS urls and store them in a dictionary
urls = {
    'Godot News': 'https://godotengine.org/rss.xml'
}

# function to return parse result from RSS url
def parsed(urls):
    return feedparser.parse(urls)

# takes in parsed RSS url result from above
# and outputs the source of the feed as
# dictionary object
def get_Source(urls):

    # list to store the return result
    channelItems = []

    # parse a dictionary from RSS feed input
    feed = parsed(urls)

    # parse another dict this time for the 'channel' section of RSS feed
    channel = feed['channel']

    # append title, link, and description from channel section to the channelItems list, 
    # entire appended dict will be one item at index 0 in list
    channelItems.append({
        'title': channel['title'],
        'link': channel['link'],
        'description': channel['description'],
    })

    # return the dict outputs in specific format defined below
    return 'Title = ' + channelItems[0]['title'] + "\n" + 'Link = ' + channelItems[0]['link'] + "\n" + 'Description = ' + channelItems[0]['description'] + "\n"

# return a list of articles from parsed feed
# articles found in feed ['entries] section
def get_Articles(urls):

    articles = []
    feed = parsed(urls)
    items = feed['items']

    # for each entry, append a dictionary
    # for id, link, title, summary, and
    # published for each entry
    for entry in items:
        articles.append({
            'Title': entry['title'],
            'Link': entry['link'],
        })
    
    return articles

# urls.get('Godot News'), 'published': entry['pubDate'],
print("RSS Feed Info: " + "\n")
print(get_Source(urls.get('Godot News')))
results = get_Articles(urls.get('Godot News'))
print("Results are printed from latest post first to oldest post bottom!" + "\n")
print(*results, sep = "\n") # instead of print(result), this prints items in new line