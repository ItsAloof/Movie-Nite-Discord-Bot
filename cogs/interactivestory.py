from array import array
from tracemalloc import stop
from typing import List
import random

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import requests
from main import TESTING_GUILD_ID
import re

from bs4 import BeautifulSoup

from main import client

class Story(commands.Cog):

    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth

    @client.slash_command(name="story", description="Generate a random interactive story", guild_ids=TESTING_GUILD_ID)
    async def interactivestory(self, interaction: Interaction):
        story_ids = [4,5,6,7,8,9,10,11,12]
        story_id = random.choice(story_ids)
        data = {
            "start": 1,
            "story_id": story_id
        }
        r = requests.post('https://boredhumans.com/api_interactive_fiction.php', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'})
        data = r.json()
        soup = BeautifulSoup(data["html"], 'html.parser')
        options = []
        for i in soup.find_all("button"):
            options.append(i.text)
        await interaction.send(soup.p.text, view=InteractiveStory(options, data["game_id"], story_id, soup.p.text))
    
    

class InteractiveButton(nextcord.ui.Button["InteractiveStory"]):
    def __init__(self, option: str, option_number: int, choice_key: str, game_id: str):
        super().__init__(style=nextcord.ButtonStyle.primary, label=option, row=option_number)
        self.game_id = game_id
        self.choice_key = choice_key
        self.option = option

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: InteractiveStory = self.view
        data = self.make_choice(self.choice_key, self.game_id)
        soup = BeautifulSoup(data["html"], 'html.parser')
        content = soup.p.text

        done = False
        if data["ended"] == 1:
            for child in view.children:
                child.disabled = True
            done = True
        if(not done):
            for i, child in enumerate(view.children):
                child.label = soup.find_all("button")[i].text
        else:
            stop()
            content = soup.p.text.replace("The story has ended.", "\n\n**The story has ended.**")
        await interaction.response.edit_message(content=content, view=view)
        

    def make_choice(self, choice_key: str, game_id: str):
        data = {
            "start": 0,
            "choice": choice_key,
            "game_id": game_id
        }
        r = requests.post('https://boredhumans.com/api_interactive_fiction.php', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'
        , "Cookie": f"story_id={self.view.story_id}"})
        data = r.json()
        return data
    
    
    
class InteractiveStory(nextcord.ui.View):
    children: List[InteractiveButton]
    def __init__(self, options: List[str], game_id: str, story_id: int, story: str):
        super().__init__()
        # self.text = text
        self.options = options
        self.story_id = story_id
        self.game_id = game_id
        self.story = story
        for i, option in enumerate(options):
            self.add_item(InteractiveButton(option, i, ("a") if i == 0 else ("b"), game_id))
    

def setup(client, **kwargs):
    print("Loaded command: {}".format(__name__))
    client.add_cog(Story(client, **kwargs))
