import lib

ListAdmin = [
    247756105558523904, #Kahinh
    319109133271957505, #Seven
    593128975228993560 #Heathcliff
]

#Identifiants
ListUrskaBot = [
    701147779199926373, #Prod
    826824696590368818 #Dev
]

#Identifiants
ListUrskiBot = [
    923531479819112499, #Prod
    923531280149250128 #Dev
]

#Données Test/prod
channel_BuildAnalysis_env = {
    'Test' : 924236539511332926,
    'Prod' : 921059437664428102
}
channel_BuildAnalysis = channel_BuildAnalysis_env[lib.tokens.var_TestProd]

channel_AdminReddit_env = {
    'Test' : 924236539511332926,
    'Prod' : 816351837296918528
}
channel_AdminReddit = channel_AdminReddit_env[lib.tokens.var_TestProd]

#Channel Discussion Bot
#Données Test/prod
channel_BotDiscussion_env = {
    'Test' : 924236539511332926,
    'Prod' : 925676976042303519
}
channel_BotDiscussion = channel_BotDiscussion_env[lib.tokens.var_TestProd]