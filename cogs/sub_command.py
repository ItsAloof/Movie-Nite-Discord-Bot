from main import TESTING_GUILD_ID
from nextcord import Interaction
from nextcord.ext import commands
import asyncio

bot = commands.Bot()

class Subtest(commands.Cog):
    def __init__(self) -> None:
        super().__init__()

@bot.slash_command(guild_ids=TESTING_GUILD_ID, description="Main Command")
async def main(interaction: Interaction):
    """
    The main slash command
    """
    pass

@main.subcommand(description="Sub command 1")
async def sub1(interaction: Interaction):
    await interaction.send(f"Hello {interaction.user.name}")


@main.subcommand(description="Sub command 2")
async def sub2(interaction: Interaction):
    await interaction.response.defer(with_message=True)
    asyncio.sleep(5)
    await interaction.response.send_message("All done...")


