from http import client
from unicodedata import name
from discord import Guild, Interaction
import discord
import nextcord
from nextcord.ext import commands
import os
import questionary

from tmdb3 import tmdb_api

from dotenv import load_dotenv

from utils.mongodb import MongoDB
from utils.settings import Modules, Permissions, Settings

from api.authorization import AuthAPI


load_dotenv(dotenv_path="./secrets.env")

tmdb = tmdb_api(api_key=os.getenv("TMDB_API_KEY"))

mongodb = MongoDB(connection_url=os.getenv("MONGODB_URI"))

TESTING_GUILD_ID = [951325774139494450, 396329225206104064, 982358070896234588, 1001667368801550439]  # Replace with your guild ID
# "you sleep 👀"
client = commands.Bot(command_prefix='mo.', description='Test Bot', intents = nextcord.Intents.all(), activity=nextcord.Activity(name=f"netflix and chill", type=nextcord.ActivityType.streaming, url="https://www.youtube.com/watch?v=0J2QdDbelmY&list=RD0J2QdDbelmY&start_radio=1"))


admin_users = [192730242673016832]
default_options = {'color': 0xd4af37, 'auth': admin_users}
modules = {
'games': [{'cmd': "interactivestory", 'options': default_options}, {'cmd': "games", 'options': default_options}, {'cmd': "economy", 'options': default_options}, {'cmd': "fakeperson", 'options': default_options}, {'cmd': "command", 'options': default_options}], 
'utils': [{'cmd': "media", 'options': default_options}], 'admin': []}
loaded_modules = []


def pickBot():
    choice0 = questionary.Choice(title="Movie Nite Bot", value="MOVIE_NITE_BOT_TOKEN", checked=True)
    choice1 = questionary.Choice(title="Mako Test Bot", value="MAKO_TEST_BOT_TOKEN")
    choice2 = questionary.Choice(title="Interaction Test Bot", value="INTERACTION_BOT_TOKEN")
    return questionary.select("Select which bot to use:", choices=[choice0, choice1, choice2]).ask()

def load_modules():
    games = questionary.Choice(title="Games", value="games", checked=True)
    utils = questionary.Choice(title="Utils", value="utils", checked=True)
    admin = questionary.Choice(title="Admin", value="admin", checked=False, disabled=True)
    return questionary.checkbox("Select which modules to load:", choices=[games, utils, admin]).ask()

# @client.event
# async def on_application_command_error(interaction: Interaction, error: Exception):
#     print(error)
#     await interaction.send(f'{interaction.user.mention} you do not have permission to use {interaction.application_command.name}')


def addMissingGuildSettings(guild: Guild):
    guild_data = mongodb.getGuildSettings(guild_id=guild.id)
    if guild_data is None:
        guildSettings = Settings(guild=guild, enabled_modules=Modules.setEnabledModules(), permissions=[Permissions().getDefaultPermissions()], members=guild.members)
        mongodb.insertGuild(guild_id=guild.id, data=guildSettings.getSettings())

@client.event
async def on_ready():
    info = await client.application_info()
    await client.change_presence(activity=nextcord.Activity(name=f"all {len(client.users)} of you sleep 👀", type=nextcord.ActivityType.watching))
    for guild in client.guilds:
        addMissingGuildSettings(guild=guild) # Probably will remove in production since it is mainly for testing purposes
    client.load_extension("cogs.errors")
    print(', '.join(client.extensions.keys()))


if __name__ == "__main__":
    for module in modules['games']:
        client.load_extension(f"cogs.{module['cmd']}", extras=module['options'])
    
    for module in modules['utils']:
        client.load_extension(f"cogs.{module['cmd']}", extras=module['options'])
    
    for module in modules['admin']:
        client.load_extension(f"cogs.{module['cmd']}", extras=module['options'])

    client.load_extension("cogs.data", extras={'mongodb': mongodb, 'modules': modules})
    client.run(os.getenv(pickBot()))
