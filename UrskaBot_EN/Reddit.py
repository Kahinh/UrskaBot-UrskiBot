from typing import Dict
import lib

print("Reddit : √")

class Reddit(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__lang__ = "EN"
        self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")
        self._channeladmin_ = lib.GlobalDict.channel_AdminReddit
        self.trackerredit.start()
            
    @lib.tasks.loop(minutes=30)
    async def trackerredit(self):
        await lib.Reddit_Tools.compare_PastFeed(self, lib.RedditDict.UrskaBot_redditchannels, lib.GlobalFiles.file_Reddit_UrskaBot)

    @trackerredit.before_loop
    async def before_trackerredit(self):
        await self.bot.wait_until_ready()

    @lib.discord.ext.commands.command(name='reddit', pass_context=True)
    async def reddit(self, ctx, action="", feed="", picture=""):
        if ctx.author.id in lib.GlobalDict.ListAdmin:
            if action != "":

                #Check l'arbre
                if "Reddit" not in self.__pkl__: self.__pkl__["Reddit"] = {}
                if "Feeds" not in self.__pkl__["Reddit"]: self.__pkl__["Reddit"]["Feeds"] = {}

                if action.lower() == "add" and feed != "" :
                    self.__pkl__["Reddit"]["Feeds"][feed] = picture
                    await lib.Tools.send_messages(ctx, "C'est fait chef")

                elif action.lower() == "del":
                    self.__pkl__["Reddit"]["Feeds"].pop(feed)
                    await lib.Tools.send_messages(ctx, "C'est fait chef")
            
                elif action.lower() == "print":
                    Feed_list = ""
                    for feed in self.__pkl__["Reddit"]["Feeds"]:
                        Feed_list += feed
                        if self.__pkl__["Reddit"]["Feeds"][feed] != "":
                            Feed_list += " : :white_check_mark:\n"
                        else:
                            Feed_list += " : :red_square:\n"
                    
                    await lib.Tools.send_messages(ctx, Feed_list)
            
            #On dump le Pickles
            lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalPKL, self.__pkl__)
            self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

def setup(bot):
    bot.add_cog(Reddit(bot))