from discord import Guild, Member


class Settings():
    def __init__(self, guild: Guild, enabled_modules: list[str], permissions: dict, members: Member):
        self.enabled_modules = enabled_modules
        self.guild_id = guild.id
        self.guild_name = guild.name
        self.permissions = permissions
        self.owner = {'user_id': guild.owner_id, 'username': guild.owner.name}
        self.members = members
    
    def getSettings(self):
        return {
            "enabled_modules": self.enabled_modules,
            "guild_id": self.guild_id,
            "guild_name": self.guild_name,
            "owner": self.owner,
            "permissions": self.permissions
        }



class Permissions():
    game_cmds = ['minesweeper', 'tictactoe']
    info_cmds = ['avatar', 'serverinfo', 'cmenu', 'userinfo']
    tools_cmds = ['poll']
    def __init__(self) -> None:
        pass

    def getPermissions(self, required_role: list[str], commands: list[str] = [], modules: list[str] = []) -> list[dict]:
        return {'required_roles': required_role, 'commands': commands, 'modules': modules}
    
    def getDefaultPermissions(self):
        return {'required_roles': ['@everyone'], 'commands': [], 'modules': [self.game_cmds, self.info_cmds, self.tools_cmds]}

class Modules():
    def __init__(self) -> None:
        pass

    def getModules(self) -> list[str]:
        return ['economy', 'games', 'info', 'tools']
    
    def setEnabledModules(economyEnabled: bool = True, gamesEnabled: bool = True, infoEnabled: bool = True, toolsEnabled: bool = True, modEnabled: bool = True) -> list[dict]:
        modules = []
        return {
            'economy': economyEnabled,
            'games': gamesEnabled,
            'info': infoEnabled,
            'tools': toolsEnabled,
            'mod': modEnabled
        }
