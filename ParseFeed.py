import feedparser #pip3 install feedparser
import os

#region variables

# getSource variables
sourceLocation = ''
stitle = ''
slink = ''
scontent = ''

# getArticle variables
articleItems = ''
atitle = ''
alink = ''

# url variables
key = ''
url = ''

# get RSS urls and store them in a dictionary
urls = {}

#endregion

#clear the terminal
os.system('cls') # clears the terminal from code, use 'clear' on linux/Mac

# function to get RSS site links and tags from user
def getInput():
    
    # update script variables using function
    global key
    global url
    global urls
    global sourceLocation
    global stitle
    global slink
    global scontent
    global articleItems
    global atitle
    global alink

    # interact with user to update variables
    key = input("What is the name of the site you are logging? : ")
    url = input("Please enter the URL of the RSS feed: ")
    print("Please find the feed channel and enter the following info: ")
    sourceLocation = input("Please enter the channel feed tag, enter *channel* if it is just channel: ")
    stitle = input("Please enter the source title tag: ")
    slink = input("Please enter the source link tag: ")
    scontent = input("Please enter the source description tag or equivalent if availible: ")
    print("Please find the items you wish to feed in, enter *items* if they are multiple *item* tagged entries: ")
    articleItems = input("Enter *items* if you are tagging multiple item tags, or equivalent: ")
    atitle = input("Please enter the name or title tag found in each item: ")
    alink = input("Please enter the link tag for the entries found in each item: ")

    # update dictionary with new key and RSS Feed URL value
    urls.update({key: url})

    print("Thank You for the feed, calculating! " + "\n")

# function to return parse result from RSS url
def parsed(urls):
    return feedparser.parse(urls)

# takes in parsed RSS url result from above
# and outputs the source of the feed as
# dictionary object
def get_Source(urls):

    # function variables to show the result properly: 
    # first to capatilize the keys 
    firstEntry = stitle.title()
    secondEntry = slink.title()
    thirdEntry = scontent.title()

    # second to prepare for output
    firstOutput = firstEntry + " = "
    secondOutput = secondEntry + " = "
    thirdOutput = thirdEntry + " = "

    # list to store the return result
    channelItems = []

    # parse a dictionary from RSS feed input
    feed = parsed(urls)

    # parse another dict this time for the 'channel' section of RSS feed
    channel = feed[sourceLocation]

    # append title, link, and description from channel section to the channelItems list, 
    # entire appended dict will be one item at index 0 in list
    channelItems.append({
        firstEntry: channel[stitle],
        secondEntry: channel[slink],
        thirdEntry: channel[scontent],
    })

    # return the dict outputs in specific format defined below
    return firstOutput + channelItems[0][firstEntry] + "\n" + secondOutput + channelItems[0][secondEntry] + "\n" + thirdOutput + channelItems[0][thirdEntry] + "\n"

# return a list of articles from parsed feed
# articles found in feed ['entries] section
def get_Articles(urls):

    articles = []
    feed = parsed(urls)
    items = feed[articleItems]

    # for each entry, append a dictionary
    # for id, link, title, summary, and
    # published for each entry
    for entry in items:
        articles.append({
            atitle.title(): entry[atitle],
            alink.title(): entry[alink],
        })
    
    return articles

# main function
def main():

    getInput()
    print("RSS Feed Info: " + "\n")
    print(get_Source(urls.get(key)))
    results = get_Articles(urls.get(key))
    print("Results are printed from latest post first to oldest post bottom!" + "\n")
    print(*results, sep = "\n") # instead of print(result), this prints items in new line

# define main function to compiler on run
if __name__ == "__main__":
    main()

#region misc comments and notes

    # urls.get('Godot News'), 'published': entry['pubDate'],

#endregion