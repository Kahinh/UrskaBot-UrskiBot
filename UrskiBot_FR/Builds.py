import lib

print("Builds : √")
FileName = lib.GlobalFiles.file_BuildList

class BuildList(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__buildlist__ = lib.Pickles.LoadPickle(FileName)
        self.__names_json__ = lib.Builder_JSON.get_names_json("FR")
        self.__data_json__ = lib.Builder_JSON.get_data_json("FR")
        self.__count__ = 1
        self._channelanalysis_ = lib.GlobalDict.channel_BuildAnalysis

    @lib.cog_ext.cog_slash(name="Builds", description="Bibliothèque de builds optimisés & meta", options=[
                lib.create_option(
                    name="type",
                    description="which type of builds do you want ?",
                    option_type=3,
                    required=True,
                    choices=[
                       {'name': 'Iceborne', 'value': 'Iceborne'},
                       {'name': 'Bastion', 'value': 'Bastion'},
                       {'name': 'Discipline', 'value': 'Discipline'},
                       {'name': 'Tempest', 'value': 'Tempest'},
                       {'name': 'Revenant', 'value': 'Revenant'},
                       {'name': 'Catalyst', 'value': 'Catalyst'}
                    ]
                ),
                lib.create_option(
                  name="weapon",
                  description="Which weapon in your build ?",
                  option_type=3,
                  required=True,
                    choices=[
                       {'name': 'Sword', 'value': 'Sword'},
                       {'name': 'Warpike', 'value': 'War Pike'},
                       {'name': 'Aether Strikers', 'value': 'Aether Strikers'},
                       {'name': 'Chain Blades', 'value': 'Chain Blades'},
                       {'name': 'Axe', 'value': 'Axe'},
                       {'name': 'Hammer', 'value': 'Hammer'},
                       {'name': 'Repeaters', 'value': 'Repeater'}
                    ]
                ),
                lib.create_option(
                  name="element",
                  description="Which element in your build ?",
                  option_type=3,
                  required=True,
                    choices=[
                       {'name': 'Shock', 'value': 'Shock'},
                       {'name': 'Blaze', 'value': 'Blaze'},
                       {'name': 'Umbral', 'value': 'Umbral'},
                       {'name': 'Terra', 'value': 'Terra'},
                       {'name': 'Frost', 'value': 'Frost'},
                       {'name': 'Radiant', 'value': 'Radiant'}
                    ]
                )
             ])
    async def _builds(self, ctx: lib.SlashContext, type, weapon, element):

        build_link, embed, self.__count__ = lib.Builds_Tools.create_build_embed("EN", self.__buildlist__, self.__names_json__, self.__data_json__, self.__count__, type, weapon, element)

        if build_link != "":
            await lib.Tools.send_messages(ctx, embed, "embed")
        else:
            await lib.Tools.send_messages(ctx, "Je n'ai pas trouvé de builds convenant à votre requête.")

    async def updatebuilds(self):
        #ON LOAD GSHEET
        self.__buildlist__ = lib.Builds_Tools.get_buildsdata()

        #ON LOAD LES JSONS
        self.__names_json__ = lib.Builder_JSON.get_names_json("FR")
        self.__data_json__ = lib.Builder_JSON.get_data_json("FR")

    @lib.discord.ext.commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("//updatebuilds") and (message.author.id in lib.GlobalDict.ListAdmin or message.author.id in lib.GlobalDict.ListUrskaBot):
            await BuildList.updatebuilds(self)
            await lib.Tools.send_messages(message.channel , "Données Loadées")

def setup(bot):
    bot.add_cog(BuildList(bot))