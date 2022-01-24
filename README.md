# UrskaBot-UrskiBot

**DISCLAIMER :**
Bot can have some issues on Phone because the phone will try to add a space at the end of your last choice.
So in place of "Shock" your phone will try to push "Shock " and then it won't work. The issue comes from Discord. Not from the Bot itself.

**This bot extracts its data directly from the amazing websites:**
- https://dauntless-builder.fr/ by Medaey
- https://www.dauntless-builder.com/ by atomicptr

**Data about builds comes from:**
- [MetaSheet](https://docs.google.com/spreadsheets/d/1-I4LQ_8uNqV9LuybXhz2wjmcPeTNNGWRZ-kFjsckwtk/edit#gid=0)
- [TrialSheet](https://docs.google.com/spreadsheets/d/1Kv3nlr7y5DJB_olhATqXXh-jPCkDygNCVyHkDwllTsc/edit)
Maintained by the Official Dauntless Community, mainly Nthngnss

Thanks to all of them to let me use their works/websites/data to run the bot.

__The Bot exists in two versions, one French and one English:__
- UrskaBot (EN) - [ADD THE EN BOT TO MY DISCORD](https://discord.com/api/oauth2/authorize?client_id=701147779199926373&permissions=294205323264&scope=bot%20applications.commands)
- UrskiBot (FR) - [ADD THE FR BOT TO MY DISCORD](https://discord.com/api/oauth2/authorize?client_id=923531479819112499&permissions=294205323264&scope=bot%20applications.commands)

UrskaBot / UrskiBot is the best solution to access Dauntless Meta Builds directly into Discord !

## Features:
### For Users: 
- /Build : Allowing you to select your Omni/Weapon/Element to get a build with those criterias directly into Discord.
- /Trial : Allowing you to select your Weapon to get a build for Trials Solo with this criteria directly into Discord.
- RedditTracker : The bot follows PHXL post on Reddit and post it on your server (This feature is not automated yet, so if you are interested, please contact me on Discord : ESkateFr#6704)

## About:
I have a Discord to share my projects around Dauntless, and so you can come there and discuss/share suggestions about the bot here : https://discord.gg/EeCMDavcDu

Thanks for sharing and using the bot !

### 😄

## TodoList:
There is still a lot to do, mainly to clean and optimize the bot. But I didn't plan any new major features to add into the bot, as the features already available are the ones I wanted to bring in.
- [] Automate Reddit - Currently Reddit Feature is manual (I need to add Channels & PHXL RSS feeds manually)
- [X] Revamp get_build_link() & get_trial_link()
- [X] All Trad_Items from Builds Dict into one dictionnary. In Create_Embed, improve the looping of reversed trad.
- [X] Revamp create_build_embed() & create_trial_embed()
- [X] Revamp get_buildsdata() & get_trialsdata()
- [X] Revamp get_metasheetdata() & get_trialsheetdata()
- [X] Revamp Trads with Books
- [X] Bots playing a game
- [X] Better date for Reddit Posts
- [X] Solve lib.GlobalDict.Timer on Global Tools
- [] Only one PKL
- [] Add a /command for Esca Builds