import feedparser #pip3 install feedparser

# function to return parse result from RSS url
def parse(url):
    return feedparser.parse(url)

# takes in parsed RSS url result from above
# and outputs the source of the feed as
# dictionary object
def get_Source(parsed):
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
    }

# return a list of articles from parsed feed
# articles found in feed ['entries] section
def get_Articles(parsed):

    articles = []
    entries = parsed['entries']

    # for each entry, append a dictionary
    # for id, link, title, summary, and
    # published for each entry
    for entry in entries:
        articles.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'summary': entry['summary'],
            'published': entry['published parsed'],
        })
    
    return articles
