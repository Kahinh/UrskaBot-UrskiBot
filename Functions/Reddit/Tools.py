import lib

def get_Soup_and_Thumbnail(entry):
    media_thumbnail = ""
    soupContent = ""
    if "md" in entry.content[0].value:
        soupContent = lib.BeautifulSoup(entry.content[0].value, features='html.parser')
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
            if hasattr(lib.ssl, '_create_unverified_context'):
                lib.ssl._create_default_https_context = lib.ssl._create_unverified_context
            FluxReddit[feed] = lib.feedparser.parse(feed)
        except: 
            FluxReddit[feed] = {}
    return FluxReddit

#Fonction post sur Discord
async def EmbedDiscord(self, label, feedtitle, content, thumbnail, feed_url, time, redditchannels):
    for channel_id in redditchannels:
        try:
            channel = self.bot.get_channel(channel_id)
            if label == "r/dauntless":
                embed=lib.discord.Embed(title=f"{feedtitle}", \
                url=f"{feed_url}", \
                description=f"{content[:1000]}", \
                color=0xFFC866)
                if content == "":
                    embed.set_image(url=f"{thumbnail}")
                else:
                    embed.set_thumbnail(url=f"{thumbnail}")
                embed.set_footer(text=f"Date : {time}")

                #Puis on poste le embed
                await channel.send(embed=embed)
        except:
            pass

def launch_tracker():

    print("Initialisation de la récupération des flux RSS Reddit.")

    PastFeed = {}

    #First step, on récupère les flux Reddit.
    FluxReddits = get_FluxReddit(lib.RedditDict.PHXL_Feeds)

    #Second step, on check si c'est déjà dans le oldFeed
    for feed in lib.RedditDict.PHXL_Feeds:

        #On vérifie quand même que ce qu'on remonte est cohérent
        if FluxReddits[feed] != {}:

            #Si jamais c'est la première fois qu'on voit le bonhomme
            if feed not in PastFeed:
                PastFeed[feed] = {}

            #On get le content
            for entry in reversed(FluxReddits[feed].entries):
                id = entry['id']

                #Si le message a pas encore été posté
                if id not in PastFeed[feed]:

                    #On Init pour mettre les datas
                    PastFeed[feed][id] = {}

                    #On get le contenu
                    media_thumbnail, soupContent = get_Soup_and_Thumbnail(entry)

                    #Si le media_thumbnail est vide, on essaie de foutre l'icone de l'user.
                    if media_thumbnail == "":
                        if feed in lib.RedditDict.PHXL_Feeds:
                            media_thumbnail = lib.RedditDict.PHXL_Feeds[feed]

                    date = lib.datetime.fromisoformat(entry.updated).strftime('%d %b %Y | %Hh%M')

                    PastFeed[feed][id]["label"] = entry.tags[0].label
                    PastFeed[feed][id]["title"] = entry.title
                    PastFeed[feed][id]["content"] = soupContent
                    PastFeed[feed][id]["thumbnail"] = media_thumbnail
                    PastFeed[feed][id]["link"] = entry.link
                    PastFeed[feed][id]["date"] = date

    #Pour finir, on sauvegarde dans le pickle
    lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalReddit, PastFeed)

    print("Flux RSS Reddit récupérés.")

async def compare_PastFeed(self, redditchannels, FeedRedditID_Bot):

    channeladmin = self.bot.get_channel(lib.GlobalDict.channel_AdminReddit)
    await lib.Tools.send_messages(channeladmin, "C'est parti", "standard", 7200)

    #On récupère les PastFeed
    Global_PastFeed = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalReddit, "Dict")
    Bot_PastFeed = lib.Pickles.LoadPickle(FeedRedditID_Bot, "Dict")

    if Global_PastFeed != {}:

        #Second step, on check si c'est déjà dans le oldFeed
        for feed in Global_PastFeed:

            #Si jamais c'est la première fois qu'on voit le bonhomme
            if feed not in Bot_PastFeed:
                Bot_PastFeed[feed] = []

            #On get le content
            for id in Global_PastFeed[feed]:

                #Si le message a pas encore été posté
                if id not in Bot_PastFeed[feed]:

                    Bot_PastFeed[feed].append(id)
                    if len(Bot_PastFeed[feed]) > 50:
                        Bot_PastFeed[feed].pop(0)

                    await EmbedDiscord(self, Global_PastFeed[feed][id]["label"], Global_PastFeed[feed][id]["title"], Global_PastFeed[feed][id]["content"], Global_PastFeed[feed][id]["thumbnail"], Global_PastFeed[feed][id]["link"], Global_PastFeed[feed][id]["date"], redditchannels)

    #Pour finir, on sauvegarde dans le pickle
    lib.Pickles.DumpPickle(FeedRedditID_Bot, Bot_PastFeed)

    await lib.Tools.send_messages(channeladmin, "C'est fini", "standard", 7200)