from typing import Dict
import lib

print("Reddit : √")

class Reddit(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__lang__ = "EN"
        self._channeladmin_ = lib.GlobalDict.channel_AdminReddit
        self.trackerredit.start()
            
    @lib.tasks.loop(minutes=30)
    async def trackerredit(self):
        await lib.Reddit_Tools.compare_PastFeed(self, lib.RedditDict.UrskaBot_redditchannels, lib.GlobalFiles.file_Reddit_UrskaBot)

    @trackerredit.before_loop
    async def before_trackerredit(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Reddit(bot))