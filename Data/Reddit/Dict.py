import lib

PHXL_Feeds = {
    'https://www.reddit.com/user/CreatureTech-PHX/.rss' : "https://styles.redditmedia.com/t5_24l3xq/styles/profileIcon_o0frpu7ywro31.jpg?width=256&height=256&crop=256:256,smart&s=7b4d77320f92ee6a7608d01aebf1413d06cfa697",
    'https://www.reddit.com/user/EuanReid/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_0.png",
    'https://www.reddit.com/user/Ahrelia-PHX/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_4.png",
    'https://www.reddit.com/user/bunheadwhat/.rss' : "https://styles.redditmedia.com/t5_1rfxeo/styles/profileIcon_1xbc7tgts7t41.jpg?width=256&height=256&crop=256:256,smart&s=a7efc61ebeb20a17442e477c8fca16a9be444c71",
    'https://www.reddit.com/user/crash7800/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_5.png",
    'https://www.reddit.com/user/tinouti/.rss' : "https://styles.redditmedia.com/t5_d3tzt/styles/profileIcon_fijph7h1lyg11.jpg?width=256&height=256&crop=256:256,smart&s=4d39ad5e84f2f1c7bbac9e1cb0d05e69f0b637dd",
    'https://www.reddit.com/user/meatocracy/.rss' : "https://i.redd.it/snoovatar/avatars/e6eef126-528d-4819-856b-d9371940b39a.png",
    'https://www.reddit.com/user/jordanpowpow/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_7.png",
    'https://www.reddit.com/user/Proteus505/.rss' : "https://i.redd.it/snoovatar/avatars/2204907a-8df8-4b18-b615-498e18ace539.png",
    'https://www.reddit.com/user/Curiousaur/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_3.png",
    'https://www.reddit.com/user/Princess_CMoney/.rss' : "https://styles.redditmedia.com/t5_22gp86/styles/profileIcon_juzilpod54e31.jpg?width=256&height=256&crop=256:256,smart&s=51050aa4a773e47f415d692f8ca709225858ff25",
    'https://www.reddit.com/user/gtez/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_5.png",
    'https://www.reddit.com/user/joshlhood/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_6.png",
    'https://www.reddit.com/user/ChandyPHX/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_1.png",
    'https://www.reddit.com/user/orz-PHX/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_6.png",
    'https://www.reddit.com/user/C4_PHX/.rss' : "https://i.redd.it/snoovatar/avatars/7025ad3c-8513-418e-868b-b236b70c77b1.png",
    'https://www.reddit.com/user/ForgedPixel/.rss' : "https://styles.redditmedia.com/t5_jf4ji/styles/profileIcon_bbtgy44hh2z01.png?width=256&height=256&crop=256:256,smart&s=dab9151feeb9fa9936d014eafb0f523b5a0b11a2",
    'https://www.reddit.com/user/theLegendLarry/.rss' : "https://i.redd.it/snoovatar/avatars/71c05c31-542d-4897-a87d-9fd6c670a8c6.png",
    'https://www.reddit.com/user/situatedmango/.rss' : "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_4.png",
    'https://www.reddit.com/user/JulioNicoletti/.rss' : "https://i.redd.it/snoovatar/avatars/ed341f0a-b2ce-44d1-a9cc-aa9db3dcce8d.png",
    'http://www.reddit.com/user/slayerdk-PHX/.rss' : "https://styles.redditmedia.com/t5_4ojgbo/styles/profileIcon_ur6mtihdb1e71.png?width=256&height=256&crop=256:256,smart&s=7a9fa4d2b4d45b7c1a3cc3526600f33bbbc0e580"
    }

#Données Test/Prod
UrskaBot_redditchannels_env = {
    'Test' : [924236539511332926],
    'Prod' : [ \
    815634847657754624, #UrskaBot Server
    817073559007526983, #Cpt Maelstrom
    878390230376415252, #MrTrails
    915636122913230908, #Texas-Ranger
    917014765916815360, #DoriBallz
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