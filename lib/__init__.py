#librairies
import os
import ssl
import discord
import discord.ext
from discord.ext import tasks
from discord_slash import SlashCommand, cog_ext, SlashContext # Importing the newly installed library.
from discord_slash.utils.manage_commands import create_option, create_choice
import pickle
import gspread
import urllib.request, json 
import time

from bs4 import BeautifulSoup
import feedparser

#folders & files
import gitignore.tokens as tokens

#FUNCTIONS
import Functions.Global.Pickles as Pickles
import Functions.Global.Tools as Tools

import Functions.Builds.Builder_JSON as Builder_JSON
import Functions.Builds.GSheet as GSheet
import Functions.Builds.Tools as Builds_Tools
import Functions.Builds.get_Effects as get_Effects

import Functions.Reddit.Tools as Reddit_Tools

#DATA
import Data.Global.Files as GlobalFiles
import Data.Global.Dict as GlobalDict

import Data.Builds.Dict as BuildsDict
import Data.Builds.Builder_Config as Builder_Config

import Data.Reddit.Dict as RedditDict

#HASH
from hashids import Hashids
hashids = Hashids(salt='spicy')

#Localisation
from Localisation.Tools import _
import Localisation.Trads as Trads

#A check
from asyncio import DefaultEventLoopPolicy