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

if __name__ == "__main__":
    PHXL_Feeds = [ \
        'http://www.reddit.com/user/CreatureTech-PHX/.rss', \
        ]
    FluxReddit = get_FluxReddit(PHXL_Feeds)
    print(FluxReddit)

#Fonction post sur Discord
async def EmbedDiscord(self, label, feedtitle, content, thumbnail, feed_url, time):
    for channel_id in lib.RedditDict.UrskaBot_redditchannels:
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