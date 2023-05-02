from pymongo import InsertOne, MongoClient, UpdateOne
import pymongo
import os


class MongoDB():
    guild_database = "guilds"
    settings_collection = "settings"
    user_database = "users"
    user_collection = "userdata"
    def __init__(self, connection_url: str):
        self.client = MongoClient(connection_url)
    
    @property
    def client(self):
        return self._client
    
    @client.setter
    def client(self, client):
        self._client = client

    def getDatabase(self, database_name: str):
        return self.client[database_name]
    
    def getCollection(self, database_name: str, collection_name: str):
        return self.getDatabase(database_name)[collection_name]
    
    def getGuildDatabase(self):
        return self.getDatabase(self.guild_database)
    
    def getUserDatabase(self):
        return self.getDatabase(self.user_database)

    def getGuildSettingsCollection(self):
        return self.getGuildDatabase()[self.settings_collection]
    
    def getUserCollection(self):
        return self.getUserDatabase()[self.user_collection]

    def insertGuild(self, guild_id: int, data: dict):
        if self.getGuildSettings(guild_id) is None:
            self.getGuildSettingsCollection().insert_one(data)
        else:
            self.updateGuild(guild_id, data)
        
    def updateGuild(self, guild_id: int, data: dict):
        self.getGuildSettingsCollection().update_one({"guild_id": guild_id}, {"$set": data})
    
    def getGuildSettings(self, guild_id: int):
        settings = self.getGuildSettingsCollection().find_one({"guild_id": guild_id})
        return settings
    
    def insertUser(self, user_id: int, data: dict):
        if self.getUser(user_id) is None:
            self.getUserCollection().insert_one(data)
        else:
            self.updateUser(user_id, data)

    def insertManyUsers(self, data: list):
        documents = []
        for user in data:
            documents.append(UpdateOne({"user_id": user["user_id"]}, update={"$setOnInsert": { **user }}, upsert=True))
            documents.append(UpdateOne({"user_id": user["user_id"]}, update={"$set": { 'mutual_guilds': user['mutual_guilds']}}, upsert=True))
        self.getUserCollection().bulk_write(documents)
    
    def getUser(self, user_id: int):
        user = self.getUserCollection().find_one({"user_id": user_id})
        return user

    def updateUser(self, user_id: int, data: dict):
        self.getUserCollection().update_one({"user_id": user_id}, {"$set": data})
    
