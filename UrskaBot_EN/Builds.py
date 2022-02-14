import lib

print("Builds : √")

class BuildList(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #Globals
        self.__lang__ = "EN"
        self.__count__ = 1
        self._channelanalysis_ = lib.GlobalDict.channel_BuildAnalysis

        #JSON
        self.__names_json__ = lib.Builder_JSON.get_names_json("EN")
        self.__data_json__ = lib.Builder_JSON.get_data_json("EN")

        self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")


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

        build_link, embed, self.__count__, component = lib.Builds_Tools.create_embed(self.__lang__, "MetaListe", self.__pkl__["Builds"]["MetaListe"], self.__names_json__, self.__data_json__, self.__count__, {type: "Type", weapon: "Weapon", element: "Element"})

        if build_link != "":
            await lib.Tools.send_messages(ctx, embed, "embed", lib.GlobalDict.Timer, component)
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))

    @lib.discord.ext.commands.command(name='updatebuilds', pass_context=True)
    async def updatebuild(self, ctx):
        if ctx.author.id in lib.GlobalDict.ListAdmin:
            #ON LOAD GSHEET
            self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

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

            #on met à jour si d'autres pages ont été mises à jour
            self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

            #Check l'arbre
            if "Builds" not in self.__pkl__: self.__pkl__["Builds"] = {}
            if "MetaListe" not in self.__pkl__["Builds"]: self.__pkl__["Builds"]["MetaListe"] = {}

            #On supprime tout pour commencer
            lib.GSheet.reset_trialdata(lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Builds_Sheet, lib.BuildsDict.Builds_Range_Delete)
            
            #First, on récup la liste des Omnis à récupérer
            SheetListe = list(lib.BuildsDict.trad_Builds["Types"].values())
            
            MetaSheetListe = lib.Builds_Tools.get_sheetdata("Meta", lib.BuildsDict.Meta_Workbook, lib.BuildsDict.Meta_Range, SheetListe)
            MetaBuildListe = []

            for Omni in MetaSheetListe:

                for row in MetaSheetListe[Omni]:

                    #Row = [link, name]
                    lien = row[0]
                    name = row[1]

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
                            
                            newRow = [Omnicell, Type, Element, lien, name]
                            MetaBuildListe.append(newRow)

                        else:
                            lien = lien.replace(".fr", ".com")
                            channel = self.bot.get_channel(self._channelanalysis_)
                            await channel.send(f"Meta : Anomalie identifié : \n{Omnicell}\n{lien}\n{BuildInfos}")

            isDone_Meta = lib.GSheet.pushData(MetaBuildListe,lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Builds_Sheet, lib.BuildsDict.Builds_start_letter, lib.BuildsDict.Builds_end_letter, lib.BuildsDict.Builds_start_row)
            if isDone_Meta == "Done":

                #ON LOAD GSHEET
                self.__pkl__["Builds"]["MetaListe"] = lib.Builds_Tools.get_GoogleData("Builds", lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Builds_Sheet, lib.BuildsDict.Builds_Range_Push)
                lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalPKL, self.__pkl__)
                
                await lib.Tools.send_messages(ctx, "Les données ont été chargées dans le GSheet")
                BotDiscussion_channel = self.bot.get_channel(lib.GlobalDict.channel_BotDiscussion)
                await lib.Tools.send_messages(BotDiscussion_channel, "//currentbuilds à ton tour UrskiBot")
            else:
                await lib.Tools.send_messages(ctx, "Ca a merdé chef")

    @lib.discord.ext.commands.command(name='trialsheet', pass_context=True)
    async def trialsheet(self, ctx):
        if ctx.author.id in lib.GlobalDict.ListAdmin:

            #on met à jour si d'autres pages ont été mises à jour
            self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

            #Check l'arbre
            if "Builds" not in self.__pkl__: self.__pkl__["Builds"] = {}
            if "TrialListe" not in self.__pkl__["Builds"]: self.__pkl__["Builds"]["TrialListe"] = {}

            #On supprime tout pour commencer
            lib.GSheet.reset_trialdata(lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Trials_Sheet, lib.BuildsDict.Builds_Trials_Range_Delete)
            
            #On récupère les onglets dispo dans la TrialSheet
            SheetListe = lib.GSheet.get_trialsheetlist(lib.BuildsDict.Trials_Workbook)

            #Puis on récupère les données
            TrialSheetListe = lib.Builds_Tools.get_sheetdata("Meta", lib.BuildsDict.Trials_Workbook, lib.BuildsDict.Trials_Range, SheetListe)
            TrialBuildListe = []

            for Behemoth in TrialSheetListe:

                for row in TrialSheetListe[Behemoth]:

                    #Row = [link, name]
                    lien = row[0]
                    name = row[1]

                    BuildInfos = lib.Builder_JSON.get_hash(lien)

                    #On check la version
                    if BuildInfos != ():
                        if BuildInfos[0] in lib.Builder_Config.omnicells:

                            #Weapon
                            Weapon = self.__names_json__["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
                            Type = self.__data_json__["weapons"][Weapon]["type"]

                            newRow = [Behemoth, Type, lien, name]
                            TrialBuildListe.append(newRow)

                        else:
                            channel = self.bot.get_channel(self._channelanalysis_)
                            await channel.send(f"Trials : Anomalie identifié : \n{Behemoth}\n{lien}\n{BuildInfos}")

            isDone_Trial = lib.GSheet.pushData(TrialBuildListe, lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Trials_Sheet, lib.BuildsDict.Builds_Trials_start_letter, lib.BuildsDict.Builds_Trials_end_letter, lib.BuildsDict.Builds_Trials_start_row)
            if isDone_Trial == "Done":

                #ON LOAD GSHEET
                self.__pkl__["Builds"]["TrialListe"] = lib.Builds_Tools.get_GoogleData("Builds", lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Trials_Sheet, lib.BuildsDict.Builds_Trials_Range_Push)
                lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalPKL, self.__pkl__)
                
                await lib.Tools.send_messages(ctx, "Les données ont été chargées dans le GSheet")
                BotDiscussion_channel = self.bot.get_channel(lib.GlobalDict.channel_BotDiscussion)
                await lib.Tools.send_messages(BotDiscussion_channel, "//currentbuilds à ton tour UrskiBot")
            else:
                await lib.Tools.send_messages(ctx, "Ca a merdé chef")

    @lib.discord.ext.commands.command(name='updatetrials', pass_context=True)
    async def updatetrials(self, ctx, behemoth="empty", pic_FR="", pic_EN=""):

        #on met à jour si d'autres pages ont été mises à jour
        self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

        #Check l'arbre
        if "Trials" not in self.__pkl__: self.__pkl__["Trials"] = {}
        if "CurrentTrials" not in self.__pkl__["Trials"]: self.__pkl__["Trials"]["CurrentTrials"] = ""
        if "TrialPics" not in self.__pkl__["Trials"]: self.__pkl__["Trials"]["TrialPics"] = {}

        exist = False
        for row in self.__pkl__["Builds"]["TrialListe"]:
            if behemoth == row[0]:
                exist = True
                break

        if exist or behemoth == "empty":

            if exist:
                if pic_FR !="" or pic_EN != "":
                    if behemoth not in self.__pkl__["Trials"]["TrialPics"]:
                        self.__pkl__["Trials"]["TrialPics"][behemoth] = {}
                        self.__pkl__["Trials"]["TrialPics"][behemoth]["EN"] = ""
                        self.__pkl__["Trials"]["TrialPics"][behemoth]["FR"] = ""
                    if pic_FR !="":
                        self.__pkl__["Trials"]["TrialPics"][behemoth]["FR"] = pic_FR
                    if pic_EN !="":
                        self.__pkl__["Trials"]["TrialPics"][behemoth]["EN"] = pic_EN

            self.__pkl__["Trials"]["CurrentTrials"] = behemoth

            lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalPKL, self.__pkl__)

            await lib.Tools.send_messages(ctx, f"Update : Le current Trial est : {behemoth}")
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

        TrialExist, image = lib.Builds_Tools.get_trials_pic(self.__pkl__["Trials"]["CurrentTrials"], self.__pkl__["Trials"]["TrialPics"], self.__lang__)
        if TrialExist:
        
            build_link, embed, self.__count__, component = lib.Builds_Tools.create_embed(self.__lang__, "TrialListe", self.__pkl__["Builds"]["TrialListe"], self.__names_json__, self.__data_json__, self.__count__, {self.__pkl__["Trials"]["CurrentTrials"]: "Behemoth", weapon: "Weapon"}, image)

            if build_link != "":
                await lib.Tools.send_messages(ctx, embed, "embed", lib.GlobalDict.Timer, component)
            else:
                await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "TrialNotSetup", self.__lang__))

    @lib.discord.ext.commands.Cog.listener()
    async def on_component(self, ctx: lib.ComponentContext):
        if ctx.bot == self.bot:
            #ctx.custom_id = NextPage/PreviousPage
            nbr = int(ctx.custom_id.split("/")[0])
            book = ctx.custom_id.split("/")[1]
            criterias = lib.ast.literal_eval(ctx.custom_id.split("/")[2])
            int_toadd = int(ctx.custom_id.split("/")[3])

            if book == "TriaListe":
                TrialExist, image = lib.Builds_Tools.get_trials_pic(self.__pkl__["Trials"]["CurrentTrials"], self.__pkl__["Trials"]["TrialPics"], self.__lang__)
            else:
                image = ""

            build_link, embed, self.__count__, component = lib.Builds_Tools.create_embed(self.__lang__, book, self.__pkl__["Builds"][book], self.__names_json__, self.__data_json__, self.__count__, criterias, image, nbr + int_toadd)

            if component == {}:
                await ctx.edit_origin(embed=embed, delete_after=lib.GlobalDict.Timer)
            else:
                await ctx.edit_origin(embed=embed, components=[component], delete_after=lib.GlobalDict.Timer)

    @lib.discord.ext.commands.command(name='escasheet', pass_context=True)
    async def escasheet(self, ctx):
        if ctx.author.id in lib.GlobalDict.ListAdmin:

            #on met à jour si d'autres pages ont été mises à jour
            self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

            #Check l'arbre
            if "Builds" not in self.__pkl__: self.__pkl__["Builds"] = {}
            if "EscaListe" not in self.__pkl__["Builds"]: self.__pkl__["Builds"]["EscaListe"] = {}

            #On supprime tout pour commencer
            lib.GSheet.reset_trialdata(lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Escas_Sheet, lib.BuildsDict.Escas_Range_Delete)
            
            #First, on récup la liste des Omnis à récupérer
            SheetListe = ["Escalations"]
            
            EscasSheetListe = lib.Builds_Tools.get_sheetdata("Meta", lib.BuildsDict.Meta_Workbook, lib.BuildsDict.Meta_Range, SheetListe)
            EscaBuildListe = []

            for Esca in EscasSheetListe:

                for row in EscasSheetListe[Esca]:

                    #Row = [link, name]
                    lien = row[0]
                    name = row[1]

                    #ON GET LES BUILDINFOS
                    BuildInfos = lib.Builder_JSON.get_hash(lien)

                    #On check la version
                    if BuildInfos != ():
                        if BuildInfos[0] in lib.Builder_Config.omnicells:

                            #Weapon
                            Weapon = self.__names_json__["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
                            #Element
                            Element = self.__data_json__["weapons"][Weapon]["elemental"]
                            Element = lib.BuildsDict.ElementalAdvantage[Element]
                            #Type
                            Type = self.__data_json__["weapons"][Weapon]["type"]
                            
                            newRow = [Type, Element, lien, name]
                            EscaBuildListe.append(newRow)

                        else:
                            lien = lien.replace(".fr", ".com")
                            channel = self.bot.get_channel(self._channelanalysis_)
                            await channel.send(f"Meta : Anomalie identifié : \n{lien}\n{BuildInfos}")

            isDone_Esca = lib.GSheet.pushData(EscaBuildListe,lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Escas_Sheet, lib.BuildsDict.Escas_start_letter, lib.BuildsDict.Escas_end_letter, lib.BuildsDict.Escas_start_row)
            if isDone_Esca == "Done":

                #ON LOAD GSHEET
                self.__pkl__["Builds"]["EscaListe"] = lib.Builds_Tools.get_GoogleData("Builds", lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Escas_Sheet, lib.BuildsDict.Escas_Range_Push)
                lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalPKL, self.__pkl__)
                
                await lib.Tools.send_messages(ctx, "Les données ont été chargées dans le GSheet")
                BotDiscussion_channel = self.bot.get_channel(lib.GlobalDict.channel_BotDiscussion)
                await lib.Tools.send_messages(BotDiscussion_channel, "//currentbuilds à ton tour UrskiBot")
            else:
                await lib.Tools.send_messages(ctx, "Ca a merdé chef")

    @lib.cog_ext.cog_slash(name="Esca", description="Library of builds for Escas.", options=[
                lib.create_option(
                    name="esca",
                    description="which Escalation do you want ?",
                    option_type=3,
                    required=True,
                    choices=[
                       {'name': 'Shock', 'value': 'Shock'},
                       {'name': 'Blaze', 'value': 'Blaze'},
                       {'name': 'Umbral', 'value': 'Umbral'},
                       {'name': 'Terra', 'value': 'Terra'},
                       {'name': 'Frost', 'value': 'Frost'}
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
                )
             ])
    async def _escas(self, ctx: lib.SlashContext, esca, weapon):

        build_link, embed, self.__count__, component = lib.Builds_Tools.create_embed(self.__lang__, "EscaListe", self.__pkl__["Builds"]["EscaListe"], self.__names_json__, self.__data_json__, self.__count__, {weapon: "Weapon", esca: "Escalation"})
        
        if build_link != "":
            await lib.Tools.send_messages(ctx, embed, "embed", lib.GlobalDict.Timer, component)
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))

def setup(bot):
    bot.add_cog(BuildList(bot))