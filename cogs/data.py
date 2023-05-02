import time
from discord import Guild
from nextcord.ext import commands, tasks
import nextcord
from nextcord import Interaction, Message
import orjson
from utils.mongodb import MongoDB
from utils.userdata import UserData
from utils.settings import Settings, Permissions, Modules
from nextcord.ext import application_checks



class DataCog(commands.Cog):
    from main import client as bot
    def __init__(self, client: commands.Bot, mongodb: MongoDB, modules: list[dict]):
        self.client = client
        self.mongodb = mongodb
        self.modules = modules
        bot = client

        
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(f'We have logged in as {self.client.user}\nWatching over {len(self.client.users)} in {len(self.client.guilds)} guilds.')
    #     await self.client.change_presence(activity=nextcord.Activity(name=f"all {len(self.client.users)} of you sleep 👀", type=nextcord.ActivityType.watching))
    #     for guild in self.client.guilds:
    #         self.addMissingGuildSettings(guild) # Probably will remove in production since it is mainly for testing purposes
    #     self.client.load_extension("cogs.errors")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Used to stress test the bot with a bunch of randomly generated userdata
    async def stressTest(self):
        print('Running stress test...')
        start = time.time()
        file = open('./StressTest/users.json', 'r')
        file = orjson.loads(file.read())
        users = []
        for user in file:
            data = UserData(user_id=user['user_id'], created_at=user['created_at'], username=user['username'], mutual_guilds=user['mutual_guilds'])
            users.append(data.getUserData())
        guildData = Settings(123456789, {'user_id': 951325774139494450, 'username': 'ItsAloof'}, ['moderation', 'fun', 'utils'], Permissions().getDefaultPermissions(), users)
        await self.mongodb.insertGuild(guild_id=123456789, data=guildData.getSettings())
        end = time.time()
        print('Stress test complete!\nTime taken:', end-start)
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined {guild.name}")
        guildSettings = Settings(guild=guild, enabled_modules=Modules.setEnabledModules(), permissions=[Permissions().getDefaultPermissions()], members=guild.members)
        self.mongodb.insertGuild(guild_id=guild.id, data=guildSettings.getSettings())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            await guild.system_channel.send(f"Welcome {member.mention} to {guild.name}")
        if member.bot:
            for role in guild.roles:
                if role.name == "Bot":
                    await member.add_roles(role, reason="Automated role assignment: Member was a bot")
        guild = member.guild
        userdata = UserData(member, guild)
        userdata.save()





def setup(client: commands.Bot, **kwargs):
    print("Loaded command: {}".format(__name__))
    client.add_cog(DataCog(client, **kwargs))