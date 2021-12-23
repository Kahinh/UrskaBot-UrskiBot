#librairies
import os
import ssl
import discord
import discord.ext
from discord_slash import SlashCommand, cog_ext, SlashContext # Importing the newly installed library.
from discord_slash.utils.manage_commands import create_option, create_choice
import pickle
import gspread
import urllib.request, json 

#folders & files
import gitignore.tokens as tokens

#FUNCTIONS
import Functions.Global.Pickles as Pickles
import Functions.Global.Tools as Tools

import Functions.Builds.Builder_JSON as Builder_JSON
import Functions.Builds.GSheet as GSheet
import Functions.Builds.Tools as Builds_Tools
import Functions.Builds.get_Effects as get_Effects

#DATA
import Data.Global.Files as GlobalFiles
import Data.Global.Dict as GlobalDict

import Data.Builds.Dict as BuildsDict
import Data.Builds.Builder_Config as Builder_Config

#HASH
from hashids import Hashids
hashids = Hashids(salt='spicy')


#A check
from asyncio import DefaultEventLoopPolicy