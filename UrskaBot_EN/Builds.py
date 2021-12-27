import lib

print("Builds : √")
FileName = lib.GlobalFiles.file_BuildList

class BuildList(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__lang__ = "EN"
        self.__buildlist__ = lib.Pickles.LoadPickle(FileName)
        self.__names_json__ = lib.Builder_JSON.get_names_json("EN")
        self.__data_json__ = lib.Builder_JSON.get_data_json("EN")
        self.__count__ = 1
        self._channelanalysis_ = lib.GlobalDict.channel_BuildAnalysis

    @lib.cog_ext.cog_slash(name="Builds", description="Library of meta builds (EN)", options=[
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

    @lib.discord.ext.commands.command(name='updatebuilds', pass_context=True)
    async def updatebuild(self, ctx):
        if ctx.author.id in lib.GlobalDict.ListAdmin:
            #ON LOAD GSHEET
            self.__buildlist__ = lib.Builds_Tools.get_buildsdata()

            #ON LOAD LES JSONS
            self.__names_json__ = lib.Builder_JSON.get_names_json("EN")
            self.__data_json__ = lib.Builder_JSON.get_data_json("EN")

            await lib.Tools.send_messages(ctx, lib._("DataLoaded", self.__lang__))

    @lib.discord.ext.commands.command(name="infobuild", pass_context=True)
    async def pushbuild(self, ctx, *, lien):
        if ctx.author.id in lib.GlobalDict.ListAdmin:
            #ON GET LES BUILDINFOS
            BuildInfos = lib.Builder_JSON.get_hash(lien)
            #On push en réponse
            await lib.Tools.send_messages(ctx, f"{BuildInfos}")

    @lib.discord.ext.commands.command(name='metasheet', pass_context=True)
    async def metasheet(self, ctx):
        if ctx.author.id in lib.GlobalDict.ListAdmin:

            MetaSheetListe = lib.Builds_Tools.get_metasheetdata()
            AlreadyUpdated = []

            for Omni in MetaSheetListe:

                for lien in MetaSheetListe[Omni]:
                
                    #On utilise le builder FR
                    lien = lien.replace(".com", ".fr")

                    #ON GET LES BUILDINFOS
                    BuildInfos = lib.Builder_JSON.get_hash(lien)

                    #On check la version
                    if BuildInfos[0] in lib.Builder_Config.omnicells:

                        #Omnicell
                        Omnicell = Omni
                        #Weapon
                        Weapon = self.__names_json__["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
                        #Element
                        Element = self.__data_json__["weapons"][Weapon]["elemental"]
                        #Type
                        Type = self.__data_json__["weapons"][Weapon]["type"]

                        if [Omnicell, Type, Element] not in AlreadyUpdated:
                        
                            current_Build, build_exist = lib.Builds_Tools.get_build_link(self.__buildlist__, Omnicell, Type, Element)
                            AlreadyUpdated.append([Omnicell, Type, Element])

                            if build_exist == True:
                                self.__buildlist__ = lib.Builds_Tools.update_build_link(self.__buildlist__, lien, Omnicell, Type, Element)

                            else:
                                newRow = [Omnicell, Type, Element, lien]
                                self.__buildlist__.append(newRow)

                    else:
                        lien = lien.replace(".fr", ".com")
                        channel = self.bot.get_channel(self._channelanalysis_)
                        await channel.send(f"Anomalie identifié : \n{Omni}\n{lien}\n{BuildInfos}")
                
            isDone = lib.GSheet.pushData(self.__buildlist__,lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Builds_Sheet, lib.BuildsDict.Builds_start_letter, lib.BuildsDict.Builds_end_letter, lib.BuildsDict.Builds_start_row)
            if isDone == "Done":
                await lib.Tools.send_messages(ctx, "Les données ont été chargées dans le GSheet")
                await lib.Tools.send_messages(ctx, "//updatebuilds à ton tour UrskiBot")
            else:
                await lib.Tools.send_messages(ctx, "Ca a merdé chef")

            #ON LOAD GSHEET
            self.__buildlist__ = lib.Builds_Tools.get_buildsdata()

def setup(bot):
    bot.add_cog(BuildList(bot))