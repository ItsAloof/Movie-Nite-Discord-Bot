from discord import Interaction, Member, Permissions, SlashOption
import nextcord
from nextcord.application_command import slash_command
from nextcord.ext import commands
from utils.embed_builder import Colors, Embed
# from utils.permissions import Permissions

from utils.userdata import UserData

from main import TESTING_GUILD_ID

class Bank(commands.Cog):
    def __init__(self): pass

    @slash_command(name='balance', description='Check your balance', guild_ids=TESTING_GUILD_ID)
    async def balance(self, interaction: Interaction, target: Member = SlashOption(name='target', required=False, verify=True, description="The person to set the balance of", default=None)):
        if target is not None:
            if target.bot:
                await interaction.send(embed=Embed.make_embed(title="You can't get the balance of a bot", color=Colors.red), ephemeral=True)
                return
            userdata = UserData(target, interaction.guild)
            balance = userdata.getBalance()
            await interaction.send(f"{target.mention}'s balance is {balance:,}", ephemeral=True)
            return
        else:
            userdata = UserData(interaction.user, interaction.guild)
            balance = userdata.getBalance()
        await interaction.send(f'Your balance is ${balance:,}', ephemeral=True)
    
    @slash_command(name='deposit', description='Deposit money to your balance', guild_ids=TESTING_GUILD_ID)
    async def deposit(self, interaction: Interaction, target: Member = SlashOption(name='target', required=True, verify=True, description="The person to have money deposited"), amount: int = SlashOption(required=True, name='amount', description='Amount of coins to deposit', verify=True)):
        if target.bot:
            await interaction.send(embed=Embed.make_embed(title=f"{target.mention} is a bot, so you can't deposit to them", color=Colors.red), ephemeral=True)
            return
        userdata = UserData(target, interaction.guild)
        userdata.deposit(amount)
        balance = userdata.getBalance()
        await interaction.send(content=f"{target.mention} has received a deposit", embed=Embed.make_embed(title=f"{target.name}'s Bank Statement", color=Colors.light_green, thumbnail='https://img.favpng.com/14/15/12/money-bag-bank-clip-art-png-favpng-uz7K716bKFSQsVqKx7ayRfgag.jpg',
        fields=[{'name': 'Deposit', 'value': f'`${amount:,}`', 'inline': True}, {'name': 'Balance', 'value': f'`${balance:,}`', 'inline': False}]))
    
    @slash_command(name='setbalance', description='Set your balance', guild_ids=TESTING_GUILD_ID, default_member_permissions=Permissions(administrator=True))
    # @application_checks.has_permissions(administrator=True)
    async def setbalance(self, interaction: Interaction, target: Member = SlashOption(name='target', required=True, verify=True, description="The person to set the balance of") , amount: int = SlashOption(required=True, name='amount', description='Amount of coins to set', verify=True)):
        if target.bot:
            await interaction.send(embed=Embed.make_embed(title=f"{target.mention} is a bot, so you can't set their balance", color=Colors.red), ephemeral=True)
            return
        userdata = UserData(target, interaction.guild)
        userdata.setBalance(amount)
        balance = userdata.getBalance()
        await interaction.send(f'{userdata.user.name} has ${balance:,} now', ephemeral=True)


def setup(client: commands.Bot, **kwargs):
    print('[Economy] module loaded')
    client.add_cog(Bank())
