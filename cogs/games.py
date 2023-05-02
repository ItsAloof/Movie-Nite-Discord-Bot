from array import array
from tracemalloc import stop
from typing import List
import random
from discord import Member, slash_command

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from main import TESTING_GUILD_ID

from main import client

class Games(commands.Cog):

    def __init__(self, client, color, auth):
        pass
    
    @slash_command(name="ttt", description="Play a game of Tic Tac Toe!", guild_ids=TESTING_GUILD_ID)
    async def tic_tac_toe(self, interaction: Interaction):
        await interaction.send(view=TicTacToeView(interaction.user))
    

class TicTacToeButton(nextcord.ui.Button["TicTacToeView"]):
    def __init__(self, row: int, column: int, turn: Member):
        super().__init__(style=nextcord.ButtonStyle.primary, label=" ", row=row)
        self.column = column
        self.turn = turn

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: TicTacToeView = self.view
        if interaction.user != view.turn:
            return
        if view.board[self.row][self.column] is None:
            view.board[self.row][self.column] = view.players[view.turn]
            self.disabled = True
            self.label = view.players[view.turn]

            if view.check_win():
                view.turn = None
                await interaction.response.edit_message(content=f"{view.turn} wins!")
            if view.players[view.turn] == "X":
                view.turn = view.o
            else:
                view.turn = view.x
            await interaction.response.edit_message(view=view, content=f"{view.turn}'s turn")
            

class StartTicTacToe(nextcord.ui.Button["TicTacToeView"]):
    def __init__(self, interaction: Interaction):
        super().__init__(style=nextcord.ButtonStyle.primary, label="Start Game", row=0)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: TicTacToeView = self.view
        view.players.setdefault(interaction.user, "O")
        self.disabled = True
        view.o = interaction.user
        view.create_board()
        await interaction.response.edit_message(content=f"{interaction.user} starts!", view=view)
    
class TicTacToeView(nextcord.ui.View):
    children: List[TicTacToeButton]
    def __init__(self, starting_player: Member):
        super().__init__()
        self.turn = starting_player
        self.x = starting_player
        self.o = None
        self.players = {starting_player: "X"}
        self.board = [[None for i in range(3)] for j in range(3)]
        self.children = []
        self.add_item(StartTicTacToe(self))
    
    def create_board(self):
        self.children = []
        for i in range(3):
            for j in range(3):
                self.add_item(TicTacToeButton(column=j, row=i, turn=self.turn))
    
    def check_win(self):
        for i in range(3):
            if self.board[i][0] is not None and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return True
        for i in range(3):
            if self.board[0][i] is not None and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return True
        if self.board[0][0] is not None and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True
        if self.board[0][2] is not None and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True # diagonal


    

def setup(client: commands.Bot, **kwargs):
    print("[Games] module loaded")
    client.add_cog(Games(client, **kwargs))
