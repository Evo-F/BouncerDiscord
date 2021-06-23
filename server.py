import discord


class VerifyServer:
    def __init__(self, guild):
        self.guild = guild
        self.roles = {}
        self.roles["give"] = {}
        self.roles["give"]["on_join"] = []
        self.roles["give"]["on_pass"] = []
        self.roles["take"] = []
        self.manager_roles = []



