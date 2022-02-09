import lib

print("Builds : √")

class BuildList(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__lang__ = "EN"
        self.__buildlist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_BuildList)
        self.__triallist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialList)
        self.__currenttrial__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_CurrentTrial,"Str")
        self.__trialpics__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialPics,"Dict")
        self.__names_json__ = lib.Builder_JSON.get_names_json("EN")
        self.__data_json__ = lib.Builder_JSON.get_data_json("EN")
        self.__count__ = 1
        self._channelanalysis_ = lib.GlobalDict.channel_BuildAnalysis

    @lib.cog_ext.cog_slash(name="Build", description="Library of meta builds.", options=[
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

        build_link, embed, self.__count__ = lib.Builds_Tools.create_embed(self.__lang__, "Meta_Builds", self.__buildlist__, self.__names_json__, self.__data_json__, self.__count__, {type: "Type", weapon: "Weapon", element: "Element"})

        if build_link != "":
            await lib.Tools.send_messages(ctx, embed, "embed")
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))

    @lib.discord.ext.commands.command(name='updatebuilds', pass_context=True)
    async def updatebuild(self, ctx):
        if ctx.author.id in lib.GlobalDict.ListAdmin:
            #ON LOAD GSHEET
            self.__buildlist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_BuildList)
            self.__triallist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialList)
            self.__currenttrial__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_CurrentTrial,"Str")
            self.__trialpics__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialPics,"Dict")

            #ON LOAD LES JSONS
            self.__names_json__ = lib.Builder_JSON.get_names_json("EN")
            self.__data_json__ = lib.Builder_JSON.get_data_json("EN")

            await lib.Tools.send_messages(ctx, lib._("DataLoaded", self.__lang__))
            BotDiscussion_channel = self.bot.get_channel(lib.GlobalDict.channel_BotDiscussion)
            await lib.Tools.send_messages(BotDiscussion_channel, "//currentbuilds A ton tour UrskiBot !")

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

            #First, on récup la liste des Omnis à récupérer
            SheetListe = list(lib.BuildsDict.trad_Builds["Types"].values())
            
            MetaSheetListe = lib.Builds_Tools.get_sheetdata("Meta", lib.BuildsDict.Meta_Workbook, lib.BuildsDict.Meta_Range, SheetListe)
            AlreadyUpdated = []

            for Omni in MetaSheetListe:

                for lien in MetaSheetListe[Omni]:

                    #ON GET LES BUILDINFOS
                    BuildInfos = lib.Builder_JSON.get_hash(lien)

                    #On check la version
                    if BuildInfos != ():
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
                            
                                current_Build, build_exist = lib.Builds_Tools.get_link(self.__buildlist__, [Omnicell, Type, Element])
                                AlreadyUpdated.append([Omnicell, Type, Element])

                                if build_exist == True:
                                    self.__buildlist__ = lib.Builds_Tools.update_build_link(self.__buildlist__, lien, Omnicell, Type, Element)

                                else:
                                    newRow = [Omnicell, Type, Element, lien]
                                    self.__buildlist__.append(newRow)

                        else:
                            lien = lien.replace(".fr", ".com")
                            channel = self.bot.get_channel(self._channelanalysis_)
                            await channel.send(f"Meta : Anomalie identifié : \n{Omnicell}\n{lien}\n{BuildInfos}")

            isDone_Meta = lib.GSheet.pushData(self.__buildlist__,lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Builds_Sheet, lib.BuildsDict.Builds_start_letter, lib.BuildsDict.Builds_end_letter, lib.BuildsDict.Builds_start_row)
            if isDone_Meta == "Done":
                #ON LOAD GSHEET
                self.__buildlist__ = lib.Builds_Tools.get_GoogleData("Builds", lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Builds_Sheet, lib.BuildsDict.Builds_Range, lib.GlobalFiles.file_BuildList)
                await lib.Tools.send_messages(ctx, "Les données ont été chargées dans le GSheet")
                BotDiscussion_channel = self.bot.get_channel(lib.GlobalDict.channel_BotDiscussion)
                await lib.Tools.send_messages(BotDiscussion_channel, "//currentbuilds à ton tour UrskiBot")
            else:
                await lib.Tools.send_messages(ctx, "Ca a merdé chef")

    @lib.discord.ext.commands.command(name='trialsheet', pass_context=True)
    async def trialsheet(self, ctx):
        if ctx.author.id in lib.GlobalDict.ListAdmin:

            #On supprime tout pour commencer
            lib.GSheet.reset_trialdata(lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Trials_Sheet, lib.BuildsDict.Builds_Trials_Range_Delete)
            
            #On récupère les onglets dispo dans la TrialSheet
            SheetListe = lib.GSheet.get_trialsheetlist(lib.BuildsDict.Trials_Workbook)

            #Puis on récupère les données
            TrialSheetListe = lib.Builds_Tools.get_sheetdata("Meta", lib.BuildsDict.Trials_Workbook, lib.BuildsDict.Trials_Range, SheetListe)
            AlreadyUpdated = []
            TrialBuildListe = []

            for Behemoth in TrialSheetListe:

                for lien in TrialSheetListe[Behemoth]:

                    BuildInfos = lib.Builder_JSON.get_hash(lien)

                    #On check la version
                    if BuildInfos != ():
                        if BuildInfos[0] in lib.Builder_Config.omnicells:

                            #Weapon
                            Weapon = self.__names_json__["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
                            Type = self.__data_json__["weapons"][Weapon]["type"]

                            if [Behemoth, Type] not in AlreadyUpdated:
                                AlreadyUpdated.append([Behemoth, Type])
                                newRow = [Behemoth, Type, lien]
                                TrialBuildListe.append(newRow)

                        else:
                            channel = self.bot.get_channel(self._channelanalysis_)
                            await channel.send(f"Trials : Anomalie identifié : \n{Behemoth}\n{lien}\n{BuildInfos}")

            isDone_Trial = lib.GSheet.pushData(TrialBuildListe, lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Trials_Sheet, lib.BuildsDict.Builds_Trials_start_letter, lib.BuildsDict.Builds_Trials_end_letter, lib.BuildsDict.Builds_Trials_start_row)
            if isDone_Trial == "Done":
                #ON LOAD GSHEET
                self.__triallist__ = lib.Builds_Tools.get_GoogleData("Builds", lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Trials_Sheet, lib.BuildsDict.Builds_Trials_Range_Push, lib.GlobalFiles.file_TrialList)
                await lib.Tools.send_messages(ctx, "Les données ont été chargées dans le GSheet")
                BotDiscussion_channel = self.bot.get_channel(lib.GlobalDict.channel_BotDiscussion)
                await lib.Tools.send_messages(BotDiscussion_channel, "//currentbuilds à ton tour UrskiBot")
            else:
                await lib.Tools.send_messages(ctx, "Ca a merdé chef")

    @lib.discord.ext.commands.command(name='updatetrials', pass_context=True)
    async def updatetrials(self, ctx, behemoth="empty", pic_FR="", pic_EN=""):
        exist = False
        for row in self.__triallist__:
            if behemoth == row[0]:
                exist = True
                break

        if exist or behemoth == "empty":

            if exist:
                if pic_FR !="" or pic_EN != "":
                    if behemoth not in self.__trialpics__:
                        self.__trialpics__[behemoth] = {}
                        self.__trialpics__[behemoth]["EN"] = ""
                        self.__trialpics__[behemoth]["FR"] = ""
                    if pic_FR !="":
                        self.__trialpics__[behemoth]["FR"] = pic_FR
                    if pic_EN !="":
                        self.__trialpics__[behemoth]["EN"] = pic_EN
                    
                    lib.Pickles.DumpPickle(lib.GlobalFiles.file_TrialPics, self.__trialpics__)

            self.__currenttrial__ = behemoth
            lib.Pickles.DumpPickle(lib.GlobalFiles.file_CurrentTrial, self.__currenttrial__)

            await lib.Tools.send_messages(ctx, f"Update : Le current Trial est : {self.__currenttrial__}")
            BotDiscussion_channel = self.bot.get_channel(lib.GlobalDict.channel_BotDiscussion)
            await lib.Tools.send_messages(BotDiscussion_channel, f"//currenttrials A toi UrskiBot !")
        else:
            await lib.Tools.send_messages(ctx, f"FAIL : Le Behemoth suivant n'existe pas en trial : {behemoth}")

    @lib.cog_ext.cog_slash(name="Trial", description="Library of Builds for current Trial.", options=[
                lib.create_option(
                  name="weapon",
                  description="Which weapon do you want to play ?",
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
                )
             ])
    async def _trials(self, ctx: lib.SlashContext, weapon):
        if self.__currenttrial__ != "" and self.__currenttrial__ != "empty":

            #On récupère le lien de l'image du trial
            if self.__currenttrial__ in self.__trialpics__:
                image = self.__trialpics__[self.__currenttrial__][self.__lang__]
            else:
                image = ""
            
            build_link, embed, self.__count__ = lib.Builds_Tools.create_embed(self.__lang__, "Trial_Builds", self.__triallist__, self.__names_json__, self.__data_json__, self.__count__, {self.__currenttrial__: "Behemoth", weapon: "Weapon"}, image)

            if build_link != "":
                await lib.Tools.send_messages(ctx, embed, "embed")
            else:
                await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "TrialNotSetup", self.__lang__))


def setup(bot):
    bot.add_cog(BuildList(bot))