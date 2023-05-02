from nextcord.ext import commands
import nextcord
from nextcord import Interaction, Message
import requests


from main import TESTING_GUILD_ID, client

class Command(commands.Cog):
    TESTING_GUILD_ID = 0
    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth
        client.add_listener(self.on_message)

    @nextcord.slash_command(description="My first slash command", guild_ids=TESTING_GUILD_ID)
    async def hello(self, interaction: Interaction):
        await interaction.send("Hello!")

    @client.listen()
    async def on_message(self, message: Message):
        if(message.author.bot or message.author.id == self.client.user.id):
            return
        if(self.client.user.mentioned_in(message)):
            req = requests.post("https://boredhumans.com/api_insults.php")
            data = req.text.replace("<br>", "")
            await message.channel.send(data)

def setup(client, **kwargs):
    print("Loaded command: {}".format(__name__))
    client.add_cog(Command(client, **kwargs))