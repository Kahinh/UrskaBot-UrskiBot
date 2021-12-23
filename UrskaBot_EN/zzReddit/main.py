import discord
from discord import channel
from discord.ext import commands
from discord.ext import tasks

import os

from zzReddit.DictData import PHXL_Feeds
from zzReddit.DictData import Reddit_Channels
import zzReddit.Tools as Tools

FileName = os.path.abspath(os.curdir) + '/gitignore/FeedRedditID.pkl'

print("RedditV2 : √")


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__PastFeed__ = Tools.LoadPickle(FileName)
        self._channeladmin_ = 816351837296918528
        self.trackerredit.start()

    #Fonction post sur Discord
    async def EmbedDiscord(self, label, feedtitle, content, thumbnail, feed_url, time):
        for channel_id in Reddit_Channels:
            try:
                channel = self.bot.get_channel(channel_id)
                if label == "r/dauntless":
                    embed=discord.Embed(title=f"{feedtitle}", \
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
            

    @tasks.loop(minutes=30)
    async def trackerredit(self):
        channeladmin = self.bot.get_channel(self._channeladmin_)
        await channeladmin.send("Initialisation de la récupération des flux RSS Reddit.")

        #First step, on récupère les flux Reddit.
        FluxReddits = Tools.get_FluxReddit(PHXL_Feeds)

        #Second step, on check si c'est déjà dans le oldFeed
        for feed in PHXL_Feeds:

            #On vérifie quand même que ce qu'on remonte est cohérent
            if FluxReddits[feed] != {}:

                #Si jamais c'est la première fois qu'on voit le bonhomme
                if feed not in self.__PastFeed__:
                    self.__PastFeed__[feed] = []

                #On get le content
                for entry in reversed(FluxReddits[feed].entries):
                    id = entry['id']

                    #Si le message a pas encore été posté
                    if id not in self.__PastFeed__[feed]:
                        self.__PastFeed__[feed].append(id)
                        if len(self.__PastFeed__[feed]) > 100:
                            self.__PastFeed__[feed].pop(0)

                        #On get le contenu
                        media_thumbnail, soupContent = Tools.get_Soup_and_Thumbnail(entry)

                        #Si le media_thumbnail est vide, on essaie de foutre l'icone de l'user.
                        if media_thumbnail == "":
                            if feed in PHXL_Feeds:
                                media_thumbnail = PHXL_Feeds[feed]

                        #On fait appel à la fonction pour publier le post.
                        try:
                            await self.EmbedDiscord(entry.tags[0].label, entry.title, soupContent, media_thumbnail, entry.link, entry.updated)
                        except:
                            pass

        #Pour finir, on sauvegarde dans le pickle
        Tools.DumpPickle(FileName, self.__PastFeed__)

        await channeladmin.send("Flux RSS Reddit récupérés.")

    @trackerredit.before_loop
    async def before_trackerredit(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Reddit(bot))