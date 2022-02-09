import lib

print("Builds : √")

class BuildList(lib.discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__lang__ = "FR"
        self.__buildlist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_BuildList)
        self.__triallist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialList)
        self.__currenttrial__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_CurrentTrial, "Str")
        self.__trialpics__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialPics,"Dict")
        self.__names_json__ = lib.Builder_JSON.get_names_json("FR")
        self.__data_json__ = lib.Builder_JSON.get_data_json("FR")
        self.__count__ = 1
        self._channelanalysis_ = lib.GlobalDict.channel_BuildAnalysis

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
                       {'name': 'Catalyse - Expérimenté : Offensif & Potions', 'value': 'Catalyse'}
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

        build_link, embed, self.__count__ = lib.Builds_Tools.create_embed(self.__lang__, "Meta_Builds", self.__buildlist__, self.__names_json__, self.__data_json__, self.__count__, {type: "Type", weapon: "Arme", element: "Élément"})

        if build_link != "":
            await lib.Tools.send_messages(ctx, embed, "embed")
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))

    async def updatebuilds(self):
        #ON LOAD GSHEET
        self.__buildlist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_BuildList)
        self.__triallist__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialList)
        self.__currenttrial__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_CurrentTrial, "Str")
        self.__trialpics__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialPics,"Dict")

        #ON LOAD LES JSONS
        self.__names_json__ = lib.Builder_JSON.get_names_json("FR")
        self.__data_json__ = lib.Builder_JSON.get_data_json("FR")

    @lib.discord.ext.commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("//currentbuilds") and (message.author.id in lib.GlobalDict.ListAdmin or message.author.id in lib.GlobalDict.ListUrskaBot):
            await BuildList.updatebuilds(self)
            await lib.Tools.send_messages(message.channel , lib._("DataLoaded", self.__lang__))
        if message.content.startswith("//currenttrials") and (message.author.id in lib.GlobalDict.ListAdmin or message.author.id in lib.GlobalDict.ListUrskaBot):
            self.__currenttrial__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_CurrentTrial, "Str")
            self.__trialpics__ = lib.Pickles.LoadPickle(lib.GlobalFiles.file_TrialPics,"Dict")
            await lib.Tools.send_messages(message.channel, f"Update : Bien reçu, le current Trial est : {self.__currenttrial__}")

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
        if self.__currenttrial__ != "" and self.__currenttrial__ != "empty":

            #On récupère le lien de l'image du trial
            if self.__currenttrial__ in self.__trialpics__:
                image = self.__trialpics__[self.__currenttrial__][self.__lang__]
            else:
                image = ""

            weapon = lib.BuildsDict.trad_Builds["Weapons"][arme]
            build_link, embed, self.__count__ = lib.Builds_Tools.create_embed(self.__lang__, "Trial_Builds", self.__triallist__, self.__names_json__, self.__data_json__, self.__count__, {self.__currenttrial__: "Behemoth", weapon: "Arme"}, image)

            if build_link != "":
                await lib.Tools.send_messages(ctx, embed, "embed")
            else:
                await lib.Tools.send_messages(ctx, lib._("Global", "CantFindBuild", self.__lang__))
        else:
            await lib.Tools.send_messages(ctx, lib._("Global", "TrialNotSetup", self.__lang__))

def setup(bot):
    bot.add_cog(BuildList(bot))