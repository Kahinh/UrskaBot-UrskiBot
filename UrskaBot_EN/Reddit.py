from typing import Dict
import lib

print("Reddit : √")
FileName = lib.GlobalFiles.file_Reddit

class Reddit(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__lang__ = "EN"
        self.__PastFeed__ = lib.Pickles.LoadPickle(FileName, "Dict")
        self._channeladmin_ = lib.GlobalDict.channel_AdminReddit
        self.trackerredit.start()
            
    @lib.tasks.loop(minutes=30)
    async def trackerredit(self):
        channeladmin = self.bot.get_channel(self._channeladmin_)
        self.__PastFeed__ = await lib.Reddit_Tools.launch_tracker(self, channeladmin, self.__PastFeed__, lib.RedditDict.UrskaBot_redditchannels)

    @trackerredit.before_loop
    async def before_trackerredit(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Reddit(bot))