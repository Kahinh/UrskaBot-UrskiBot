import lib

try:
    _create_unverified_https_context = lib.ssl._create_unverified_context
except AttributeError:
    pass
else:
    lib.ssl._create_default_https_context = _create_unverified_https_context

token = lib.tokens.UrskaBot
prefix = "//"

intents = lib.discord.Intents.default()
intents.members = True

bot = lib.discord.ext.commands.Bot(command_prefix=prefix, intents=intents)
slash = lib.SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True, override_type=True)

bot.remove_command('help')

print('------------------------')
startup_extensions = [
    "UrskaBot_EN.Builds"
	]

@bot.event
async def on_ready():
    print('------------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------------')

for extension in startup_extensions:
    bot.load_extension(extension)

bot.run(token)