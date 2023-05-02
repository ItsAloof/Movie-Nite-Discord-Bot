
from random import choices
from discord import SelectOption, SlashOption
from nextcord.ext import commands
import nextcord
from nextcord import Interaction
from typing import List

from utils.embed_builder import Colors, Embed

from main import TESTING_GUILD_ID, tmdb
from utils.MediaTypes import MediaType
from utils.userdata import UserData

class Media(commands.Cog):
    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth


    @nextcord.slash_command(name="media", description="Search for Movies or TV shows", guild_ids=TESTING_GUILD_ID)
    async def media(self, interaction: Interaction): 
        pass


    @media.subcommand(name="movies", description="Search for Movies")
    async def movie(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the movie you are searching for"), year: int = SlashOption(required=False, name="year", description="What year to search for movies in", verify=True), 
    ephemeral: int = SlashOption(required=False, name="hidden", description="Set whether the response should be visible to only you or everyone", choices={"yes": 1, "no": 0,})):
        results = tmdb.searchMovie(query, year)
        if(results['total_results'] == 0):
            await interaction.send(content="No results found", ephemeral=True)
            return
        embed = Embed.create_movie_embed(movie_id=results['results'][0]['id'], index=0, pages=len(results['results']))
        await interaction.send(embed=embed, view=ResultsView(results=results['results'], starting_page=0, interaction=interaction, mediaType=MediaType.movie), ephemeral=bool(ephemeral))

    @media.subcommand(name="shows", description="Search for TV shows")
    async def tv(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the show you are searching for") ,year: int = SlashOption(required=False, name="year", description="Year to search for first air dates in", 
    verify=True), ephemeral: int = SlashOption(required=False, name="hidden", description="Set whether the response should be visible to only you or everyone", choices={"yes": 1, "no": 0,}, verify=True)):
        results = tmdb.searchTVShow(query, year)
        if(results['total_results'] == 0):
            await interaction.send(content="No results found", ephemeral=True)
            return
        embed = Embed.create_tv_embed(results['results'], index=0)
        await interaction.send(embed=embed, view=ResultsView(results=results['results'], starting_page=0, interaction=interaction, mediaType=MediaType.tv), ephemeral=bool(ephemeral))

    @media.subcommand(name="people", description="Search for People in films and TV")
    async def people(self, interaction: Interaction, name: str = SlashOption(required=True, name="name", description="Name of the person to search for", verify=True), 
    ephemeral: int = SlashOption(required=False, name="hidden", description="Set whether the response should be visible to only you or everyone", choices={"yes": 1, "no": 0,}, verify=True)):
        results = tmdb.searchPeople(name)
        if(results['total_results'] == 0):
            await interaction.send(content="No results found", ephemeral=True)
            return
        embed = Embed.create_person_embed(results['results'], index=0)
        await interaction.send(embed=embed, view=ResultsView(results=results['results'], starting_page=0, interaction=interaction, mediaType=MediaType.person), ephemeral=bool(ephemeral))

    @media.subcommand(name="movielist", description="Get a list of movies you have saved")
    async def movielist(self, interaction: Interaction):
        userdata = UserData(interaction.user, interaction.guild)
        movielist: list[int] = userdata.getMovieList()
        if movielist is None or len(movielist) == 0:
            await interaction.send(content="You have no movies saved", ephemeral=True)
            return
        else:
            # movie_list = "Your Movies:\n"
            # index = 1
            # for movie in movielist:
            #     movie_list += f"{index}.) {movie['movie_name']}\n"
            #     index += 1
            # embed=nextcord.Embed(title="Your movie list", description="Choose a movie to view", color=0x00ff00)
            # await interaction.send(content=movie_list, ephemeral=True)
            await interaction.send(content="Choose a movie", view=MovieListView(interaction.user, interaction.guild), ephemeral=True)

class SaveResultButton(nextcord.ui.Button["ResultsView"]):
    def __init__(self, interaction: Interaction, mediaType: MediaType, movie_id: int, name: str):
        super().__init__(style=nextcord.ButtonStyle.success, label="Save", row=1)
        self.interaction = interaction
        self.mediaType = mediaType
        self.color = Colors.light_green
        self.movie_id = movie_id
        self.name = name

    async def callback(self, interaction: Interaction):
        if(self.mediaType == MediaType.movie):
            userdata = UserData(interaction.user, interaction.guild)
            movies = userdata.getMovieList()
            if movies is None:
                userdata.addMovie(self.movie_id, self.name)
                await interaction.send(content="Movie added to your list", ephemeral=True)
            else:
                for movie in movies:
                    if movie['movie_id'] == self.movie_id:
                        await interaction.send(content="Movie already in your list", ephemeral=True)
                        return
                userdata.addMovie(self.movie_id, self.name)
            await interaction.send(content="Movie added to your list", ephemeral=True)
    
class ResultsButton(nextcord.ui.Button["ResultsView"]):
    def __init__(self, results: list, current_page: int, next_button: bool, label: str, mediaType: MediaType):
        super().__init__(style=nextcord.ButtonStyle.primary, label=label, row=1)
        self.results = results
        self.current_page = current_page
        self.next_button = next_button
        self.mediaType = mediaType
        self.name_key = 'title' if mediaType == MediaType.movie else 'name'
        if not next_button:
            self.disabled = True
        if len(results) - 1 == 0:
            self.disabled = True

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: ResultsView = self.view
        if self.next_button:
            if self.current_page == len(view.results)-1:
                return
            else:
                self.current_page += 1
            embed = self.next_page()
        elif self.next_button is False:
            if self.current_page == 0:
                return
            else:
                self.current_page -= 1
            embed = self.prev_page()
        
        self.updateButtons(current_page=self.current_page)
        self.updateSaveButton(movie_id=view.results[self.current_page]['id'], movie_name=view.results[self.current_page][self.name_key])

        await interaction.response.edit_message(embed=embed, view=view)
    
    def disableButton(self):
        if self.next_button:
            if self.current_page == len(self.results)-1:
                self.disabled = True
            else:
                self.disabled = False
        elif self.next_button is False:
            if self.current_page == 0:
                self.disabled = True
            else:
                self.disabled = False

    def next_page(self):
        if self.current_page == len(self.view.results):
            return None
        else:
            return Embed.create_media_embed(mediaType=self.mediaType, results=self.results, index=self.current_page)
    
    def prev_page(self):
        if self.current_page < 0:
            return None
        else:
            return Embed.create_media_embed(mediaType=self.mediaType, results=self.results, index=self.current_page)

    def updateSaveButton(self, movie_id: int, movie_name: str):
        for child in self.view.children:
            if isinstance(child, SaveResultButton):
                child.movie_id = movie_id
                child.name = movie_name
                break
    
    def updateButtons(self, current_page: int):
        for child in self.view.children:
            if isinstance(child, ResultsButton):
                child.current_page = current_page
                child.disableButton()
    
class ResultsView(nextcord.ui.View):
    children: List[ResultsButton]
    def __init__(self, mediaType: MediaType, results: list, starting_page: int, interaction: Interaction):
        super().__init__()
        self.results = results
        self.starting_page = starting_page
        name_key = 'title' if mediaType == MediaType.movie else 'name'
        self.add_item(ResultsButton(results, starting_page, False, label="Prev", mediaType=mediaType))
        self.add_item(SaveResultButton(interaction, mediaType, movie_id=results[starting_page]['id'], name=results[starting_page][name_key]))
        self.add_item(ResultsButton(results, starting_page, True, label="Next", mediaType=mediaType))

class MovieSelector(nextcord.ui.Select):
    def __init__(self, movie_list: list[dict], member: nextcord.Member, guild: nextcord.Guild):
        self.guild = guild
        self.movie_list = movie_list
        self.member = member
        self.current_movie = None
        self.movie_index = {}
        options = []
        index = 0
        for movie in movie_list:
            self.movie_index[f"{movie['movie_id']}"] = index
            index += 1
            options.append(SelectOption(label=movie['movie_name'], value=movie['movie_id']))
        super().__init__(options=options, placeholder="Select a movie", row=1)

    async def callback(self, interaction: Interaction):
        movie_id = self.values[0]
        if self.current_movie is not None:
            if self.current_movie == movie_id:
                return
        self.movie_index
        embed = Embed.create_movie_embed(movie_id=movie_id, index=self.movie_index[f"{movie_id}"], pages=len(self.movie_list))
        await interaction.response.edit_message(embed=embed, view=self.view)


class MovieListView(nextcord.ui.View):
    children: List[nextcord.ui.Button]
    def __init__(self, user: nextcord.Member, guild: nextcord.Guild):
        super().__init__()
        self.add_item(MovieSelector(UserData(user, guild).getMovieList(), user, guild))
        
def setup(client: commands.Bot, **kwargs):
    print(f'Loaded command: {__name__}')
    client.add_cog(Media(client, **kwargs))


