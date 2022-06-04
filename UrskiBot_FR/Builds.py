import lib

print("Builds : √")

class BuildList(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #Globals
        self.__lang__ = "FR"
        self._channelanalysis_ = lib.GlobalDict.channel_BuildAnalysis

        #JSON
        self.__names_json__ = lib.Builder_JSON.get_names_json("FR")
        self.__data_json__ = lib.Builder_JSON.get_data_json("FR")

        self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

    @lib.cog_ext.cog_slash(name="Build", description="Bibliothèque de builds optimisés & meta.", options=[
                lib.create_option(
                    name="type",
                    description="Quel type de builds souhaitez-vous ?",
                    option_type=3,
                    required=True,
                    choices=[
                       {'name': 'Sang-Froid - Débutant : Défense et Vol de vie', 'value': 'Sang froid'},
                       {'name': 'Bastion - Intermédiaire : Bouclier et Dégâts Critiques', 'value': 'Bastion'},
                       {'name': 'Discipline - Expérimenté : Offensif & Dégâts Critiques', 'value': 'Discipline'},
                       {'name': 'Tempête - Intermédiaire : Célérité et Esquive', 'value': 'Tempête'},
                       {'name': 'Spectre - Expérimenté : Transfert Vie/Dégâts', 'value': 'Spectre'},
                       {'name': 'Catalyse - Expérimenté : Offensif & Potions', 'value': 'Catalyse'},
                       {'name': 'Artificier - Intermédiaire : Support & Offensif/Défensif', 'value': 'Artificier'}
                    ]
                ),
                lib.create_option(
                  name="arme",
                  description="Pour quelle arme souhaitez-vous ce build ?",
                  option_type=3,
                  required=True,
                    choices=[
                       {'name': 'Épée', 'value': 'Épée'},
                       {'name': 'Aéthérolance', 'value': 'Aéthérolance'},
                       {'name': 'Cestes Aéthériques', 'value': 'Cestes Aethériques'},
                       {'name': 'Chaîne-lames', 'value': 'Chaînes-lames'},
                       {'name': 'Hache', 'value': 'Hache'},
                       {'name': 'Marteau', 'value': 'Marteau'},
                       {'name': 'Répéteurs', 'value': 'Répéteurs'}
                    ]
                ),
                lib.create_option(
                  name="élément",
                  description="Quel sera l'élément de votre build ?",
                  option_type=3,
                  required=True,
                    choices=[
                       {'name': 'Foudroyant', 'value': 'Foudroyant'},
                       {'name': 'Incandescent', 'value': 'Incandescent'},
                       {'name': 'Obscur', 'value': 'Obscur'},
                       {'name': 'Tellurique', 'value': 'Tellurique'},
                       {'name': 'Givrant', 'value': 'Givrant'},
                       {'name': 'Rayonnant', 'value': 'Rayonnant'}
                    ]
                )
             ])
    async def _builds(self, ctx: lib.SlashContext, type, arme, élément):

        #Trad
        type = lib.BuildsDict.trad_Builds["Types"][type]
        weapon = lib.BuildsDict.trad_Builds["Weapons"][arme]
        element = lib.BuildsDict.trad_Builds["Elements"][élément]

        build_link, embed, self.__pkl__["Builds"]["UrskiCount"], component = lib.Builds_Tools.create_embed(self.__lang__, "MetaListe", self.__pkl__["Builds"]["MetaListe"], self.__names_json__, self.__data_json__, self.__pkl__["Builds"]["UrskiCount"], {type: "Type", weapon: "Arme", element: "Élément"})

        if build_link != "":
            await lib.Tools.send_messages(ctx, embed, "embed", lib.GlobalDict.Timer, component)
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))

    async def updatebuilds(self):
        #ON LOAD GSHEET
        self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")

        #ON LOAD LES JSONS
        self.__names_json__ = lib.Builder_JSON.get_names_json("FR")
        self.__data_json__ = lib.Builder_JSON.get_data_json("FR")

    @lib.discord.ext.commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("//currentbuilds") and (message.author.id in lib.GlobalDict.ListAdmin or message.author.id in lib.GlobalDict.ListUrskaBot):
            count = self.__pkl__["Builds"]["UrskiCount"]
            await BuildList.updatebuilds(self)
            await lib.Tools.send_messages(message.channel , lib._("Global", "DataLoaded", self.__lang__))
            self.__pkl__["Builds"]["UrskiCount"] = count
            lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalPKL, self.__pkl__)
        if message.content.startswith("//currenttrials") and (message.author.id in lib.GlobalDict.ListAdmin or message.author.id in lib.GlobalDict.ListUrskaBot):
            count = self.__pkl__["Builds"]["UrskiCount"]
            self.__pkl__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_GlobalPKL, "Dict")
            behemoth = self.__pkl__["Trials"]["CurrentTrials"]
            self.__pkl__["Builds"]["UrskiCount"] = count
            lib.Pickles.DumpPickle(lib.GlobalFiles.file_GlobalPKL, self.__pkl__)
            await lib.Tools.send_messages(message.channel, f"Update : Bien reçu, le current Trial est : {behemoth}")

    @lib.cog_ext.cog_slash(name="Trial", description="Bibliothèque de builds optimisés pour l'épreuve en cours.", options=[
                lib.create_option(
                  name="arme",
                  description="Quelle arme souhaitez-vous jouer ?",
                  option_type=3,
                  required=True,
                    choices=[
                       {'name': 'Épée', 'value': 'Épée'},
                       {'name': 'Aéthérolance', 'value': 'Aéthérolance'},
                       {'name': 'Cestes Aéthériques', 'value': 'Cestes Aethériques'},
                       {'name': 'Chaîne-lames', 'value': 'Chaînes-lames'},
                       {'name': 'Hache', 'value': 'Hache'},
                       {'name': 'Marteau', 'value': 'Marteau'},
                       {'name': 'Répéteurs', 'value': 'Répéteurs'}
                    ]
                )
             ])
    async def _trials(self, ctx: lib.SlashContext, arme):

        TrialExist, image = lib.Builds_Tools.get_trials_pic(self.__pkl__["Trials"]["CurrentTrials"], self.__pkl__["Trials"]["TrialPics"], self.__lang__)
        if TrialExist:

            weapon = lib.BuildsDict.trad_Builds["Weapons"][arme]
            build_link, embed, self.__pkl__["Builds"]["UrskiCount"], component = lib.Builds_Tools.create_embed(self.__lang__, "TrialListe", self.__pkl__["Builds"]["TrialListe"], self.__names_json__, self.__data_json__, self.__pkl__["Builds"]["UrskiCount"], {self.__pkl__["Trials"]["CurrentTrials"]: "Behemoth", weapon: "Arme"}, image)

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

            build_link, embed, self.__pkl__["Builds"]["UrskiCount"], component = lib.Builds_Tools.create_embed(self.__lang__, book, self.__pkl__["Builds"][book], self.__names_json__, self.__data_json__, self.__pkl__["Builds"]["UrskiCount"], criterias, image, nbr + int_toadd)

            if component == {}:
                await ctx.edit_origin(embed=embed, delete_after=lib.GlobalDict.Timer)
            else:
                await ctx.edit_origin(embed=embed, components=[component], delete_after=lib.GlobalDict.Timer)

    @lib.cog_ext.cog_slash(name="Esca", description="Bibliothèque de builds pour les Ascensions.", options=[
                lib.create_option(
                    name="ascension",
                    description="Pour quelle Ascension souhaitez-vous un build ?",
                    option_type=3,
                    required=True,
                    choices=[
                       {'name': 'Foudroyant', 'value': 'Foudroyant'},
                       {'name': 'Incandescent', 'value': 'Incandescent'},
                       {'name': 'Obscur', 'value': 'Obscur'},
                       {'name': 'Tellurique', 'value': 'Tellurique'},
                       {'name': 'Givrant', 'value': 'Givrant'},
                       {'name': 'Rayonnant', 'value': 'Rayonnant'}
                    ]
                ),
                lib.create_option(
                  name="arme",
                  description="Quelle arme pour votre build ?",
                  option_type=3,
                  required=True,
                    choices=[
                       {'name': 'Épée', 'value': 'Épée'},
                       {'name': 'Aéthérolance', 'value': 'Aéthérolance'},
                       {'name': 'Cestes Aéthériques', 'value': 'Cestes Aethériques'},
                       {'name': 'Chaîne-lames', 'value': 'Chaînes-lames'},
                       {'name': 'Hache', 'value': 'Hache'},
                       {'name': 'Marteau', 'value': 'Marteau'},
                       {'name': 'Répéteurs', 'value': 'Répéteurs'}
                    ]
                )
             ])
    async def _escas(self, ctx: lib.SlashContext, ascension, arme):

        esca = lib.BuildsDict.trad_Builds["Elements"][ascension]
        weapon = lib.BuildsDict.trad_Builds["Weapons"][arme]

        build_link, embed, self.__pkl__["Builds"]["UrskiCount"], component = lib.Builds_Tools.create_embed(self.__lang__, "EscaListe", self.__pkl__["Builds"]["EscaListe"], self.__names_json__, self.__data_json__, self.__pkl__["Builds"]["UrskiCount"], {weapon: "Arme", esca: "Ascension"})
        
        if build_link != "":
            await lib.Tools.send_messages(ctx, embed, "embed", lib.GlobalDict.Timer, component)
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))

def setup(bot):
    bot.add_cog(BuildList(bot))