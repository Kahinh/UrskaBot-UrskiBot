import lib

print("RedditV2 : √")
FileName = lib.GlobalFiles.file_Reddit

class Reddit(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__PastFeed__ = lib.Pickles.LoadPickle(FileName)
        self._channeladmin_ = lib.GlobalDict.channel_AdminReddit
        self.trackerredit.start()
            
    @lib.tasks.loop(minutes=30)
    async def trackerredit(self):
        channeladmin = self.bot.get_channel(self._channeladmin_)
        await channeladmin.send("Initialisation de la récupération des flux RSS Reddit.")

        #First step, on récupère les flux Reddit.
        FluxReddits = lib.Reddit_Tools.get_FluxReddit(lib.RedditDict.PHXL_Feeds)

        #Second step, on check si c'est déjà dans le oldFeed
        for feed in lib.RedditDict.PHXL_Feeds:

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
                        media_thumbnail, soupContent = lib.Reddit_Tools.get_Soup_and_Thumbnail(entry)

                        #Si le media_thumbnail est vide, on essaie de foutre l'icone de l'user.
                        if media_thumbnail == "":
                            if feed in lib.RedditDict.PHXL_Feeds:
                                media_thumbnail = lib.RedditDict.PHXL_Feeds[feed]

                        #On fait appel à la fonction pour publier le post.
                        try:
                            await lib.Reddit_Tools.EmbedDiscord(entry.tags[0].label, entry.title, soupContent, media_thumbnail, entry.link, entry.updated)
                        except:
                            pass

        #Pour finir, on sauvegarde dans le pickle
        lib.Pickles.DumpPickle(FileName, self.__PastFeed__)

        await channeladmin.send("Flux RSS Reddit récupérés.")

    @trackerredit.before_loop
    async def before_trackerredit(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Reddit(bot))