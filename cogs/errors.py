from discord import Interaction
import nextcord
from nextcord.ext import commands
from nextcord.ext import application_checks
from main import client

class ErrorListener(commands.Cog):
    def __init__(self) -> None:
        pass

        
def setup(client: commands.Bot) -> None:
    print('Errors module loaded')
    client.add_cog(ErrorListener())
