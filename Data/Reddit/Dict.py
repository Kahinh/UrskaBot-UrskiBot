import lib

#SafeLoad
#Données Test/Prod
UrskaBot_redditchannels_safeLoad_env = {
    'Test' : [924236539511332926],
    'Prod' : [815634847657754624]
}
UrskaBot_redditchannels_SafeLoad = UrskaBot_redditchannels_safeLoad_env[lib.tokens.var_TestProd]

#Données Test/Prod
UrskaBot_redditchannels_env = {
    'Test' : [924236539511332926],
    'Prod' : [ \
    815634847657754624, #UrskaBot Server
    817073559007526983, #Cpt Maelstrom
    878390230376415252, #MrTrails
    915636122913230908, #Texas-Ranger
    917014765916815360, #DoriBallz
    939608457907154944, #Baguette
    ]
}
UrskaBot_redditchannels = UrskaBot_redditchannels_env[lib.tokens.var_TestProd]

UrskiBot_redditchannels_env = {
    'Test' : [924236539511332926],
    'Prod' : []
}
UrskiBot_redditchannels = UrskiBot_redditchannels_env[lib.tokens.var_TestProd]

if __name__ == "__main__":
    print(UrskaBot_redditchannels_env["Test"])