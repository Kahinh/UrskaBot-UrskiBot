import feedparser
import ssl
import pickle
from bs4 import BeautifulSoup

def LoadPickle(FileName):
    try:
        with open(FileName, 'rb') as picklefile:
            data = pickle.load(picklefile)
            picklefile.close()
    except:
        data = {}
    
    return data

def DumpPickle(FileName, data):
    with open(FileName, 'wb') as picklefile:
        pickle.dump(data, picklefile)
        picklefile.close()

def get_Soup_and_Thumbnail(entry):
    media_thumbnail = ""
    soupContent = ""
    if "md" in entry.content[0].value:
        soupContent = BeautifulSoup(entry.content[0].value, features='html.parser')
        soupContent = soupContent.get_text('\n')
        if "media_thumbnail" in entry:
            media_thumbnail = entry.media_thumbnail[0]['url']
    else:
        if "media_thumbnail" in entry:
            media_thumbnail = entry.media_thumbnail[0]['url']

    return media_thumbnail, soupContent

def get_FluxReddit(PHXL_Feeds):
    FluxReddit = {}
    for feed in PHXL_Feeds:
        try: 
            if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
            FluxReddit[feed] = feedparser.parse(feed)
        except: 
            FluxReddit[feed] = {}
    return FluxReddit

if __name__ == "__main__":
    PHXL_Feeds = [ \
        'http://www.reddit.com/user/CreatureTech-PHX/.rss', \
        ]
    FluxReddit = get_FluxReddit(PHXL_Feeds)
    print(FluxReddit)