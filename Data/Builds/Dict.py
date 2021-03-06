import lib

#Donnees MetaBuilds
Builds_Workbook = "1Y6CnmLKtJZZFWkTmrmrSMUZEjowmft0PgrrkimJzYI8"
Builds_Range_Push = "B5:G2000"
Builds_Range_Delete = "B5:F2000"
Builds_start_letter = "B"
Builds_end_letter = "F"
Builds_start_row = 5

#Données Test/Prod
Builds_Sheet_env = {
    'Test' : "ZBuilds",
    'Prod' : "BBuilds"
}
Builds_Sheet = Builds_Sheet_env[lib.tokens.var_TestProd]

#Données Test/Prod
Trials_Sheet_env = {
    'Test' : "ZTrials",
    'Prod' : "BTrials"
}
Trials_Sheet = Trials_Sheet_env[lib.tokens.var_TestProd]

#Données MetaBuilds
Meta_Workbook = '1-I4LQ_8uNqV9LuybXhz2wjmcPeTNNGWRZ-kFjsckwtk'
Meta_Range = "A1:Z1000"

#Données TrialBuilds
Trials_Workbook = "1Kv3nlr7y5DJB_olhATqXXh-jPCkDygNCVyHkDwllTsc"
Trials_Range = "A1:Z1000"
Builds_Trials_Range_Push = "B5:F2000"
Builds_Trials_Range_Delete = "B5:E2000"
Builds_Trials_start_letter = "B"
Builds_Trials_end_letter = "E"
Builds_Trials_start_row = 5

#Données EscaBuilds
Escas_Range_Push = "B5:F2000"
Escas_Range_Delete = "B5:E2000"
Escas_start_letter = "B"
Escas_end_letter = "E"
Escas_start_row = 5

#Données Test/Prod
Escas_Sheet_env = {
    'Test' : "ZEscas",
    'Prod' : "BEscas"
}
Escas_Sheet = Escas_Sheet_env[lib.tokens.var_TestProd]

#Dico Builds
OmniColor = {
    'Standard' : 0xFFFFFF,
    'Iceborne' : 0xC3E5FE,
    'Bastion' : 0x01EFFF,
    'Discipline' : 0xF95229,
    'Tempest' : 0xFDFE71,
    'Revenant' : 0x959FF0,
    'Catalyst' : 0xff85e3,
    'Artificer' : 0xd36bff
}

trad_Builds = {
    "Types" : {
        'Sang froid' : "Iceborne",
        'Bastion' : "Bastion",
        'Discipline' : "Discipline",
        'Tempête' : "Tempest",
        'Spectre' : "Revenant",
        'Catalyse' : "Catalyst",
        'Artificier' : "Artificer"
    },
    "Weapons" : {
        'Épée' : "Sword",
        'Aéthérolance' : "War Pike",
        'Cestes Aethériques' : "Aether Strikers",
        'Chaînes-lames' : "Chain Blades",
        'Hache' : "Axe",
        'Répéteurs' : "Repeater",
        'Marteau' : "Hammer"
    },
    "Elements" : {
        'Foudroyant' : "Shock",
        'Incandescent' : "Blaze",
        'Obscur' : "Umbral",
        'Tellurique' : "Terra",
        'Givrant' : "Frost",
        'Rayonnant' : "Radiant"
    },
}

ElementalAdvantage = {
        'Shock' : "Terra",
        'Blaze' : "Frost",
        'Umbral' : "Radiant",
        'Radiant' : "Umbral",
        'Frost' : "Blaze",
        'Terra' : "Shock"
    }


#Buttons