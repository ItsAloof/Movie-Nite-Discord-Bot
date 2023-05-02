
from nextcord.ext import commands
import nextcord
from nextcord import Interaction

from main import TESTING_GUILD_ID

class Command(commands.Cog):
    TESTING_GUILD_ID = 0
    def __init__(self, client, color, auth, guilds):
        self.client = client
        self.color = color
        self.auth = auth

    @nextcord.slash_command(description="My first slash command", guild_ids=TESTING_GUILD_ID)
    async def hello(self, interaction: Interaction):
        await interaction.send("Hello!")



def setup(client, **kwargs):
    print("File name: {}".format(__name__))
    client.add_cog(Command(client, **kwargs))