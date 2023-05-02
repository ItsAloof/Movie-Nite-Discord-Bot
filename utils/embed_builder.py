import random
import nextcord
import enum
from main import tmdb
from .MediaTypes import MediaType
import enum
import time

class Colors(enum.Enum):
    aqua = 0x1ff0b0
    blue = 0x027FFC
    red = 0xFF4932
    air_force_blue = 0x5d8aa8
    dark_green = 0x006400
    dark_blue = 0x00008b
    dark_red = 0x8b0000
    dark_orange = 0xff8c00
    purple = 0xf709f7
    dark_purple = 0x800080
    dark_yellow = 0x808000
    gold = 0xffd700
    light_green = 0x39ff14
    white = 0xffffff
    black = 0x000000
    gray = 0x808080
    light_gray = 0xD3D3D3
    dark_gray = 0xA9A9A9
    yellow = 0xffff00

class Embed():
    time_format = '%Y-%m-%d'
    new_time_format = '%B %e, %Y'
    def __init__(self):
        pass

    def make_embed(title: str = "", author: str = None, description: str = None, color: Colors = Colors.black, 
    image_url = None, thumbnail = None, 
    footer_text = None, footer_icon = None, 
    fields: list = None, 
    random_color: bool = False) -> nextcord.Embed:
        if random_color:
            color = random.choice(list(Colors))
        if description is None:
            embed = nextcord.Embed(title=title,  color=color.value)
        else:
            embed = nextcord.Embed(title=title, description=description, color=color.value)
        if fields is not None:
            for field in fields:
                if field['name'] == None or field['name'] == "":
                    name = "N/A"
                else:
                    name = field['name']
                if field['value'] == None or field['value'] == "":
                    value = "N/A"
                else:
                    value = field['value']
                try:
                    inline = field['inline'] if field['inline'] is not None else False
                except IndexError:
                    inline = False
                embed.add_field(name=name, value=value, inline=inline)
        
        if author is not None:
            embed.set_author(name=author)
        if image_url is not None:
            embed.set_image(url=image_url)
        if footer_text is not None:
            embed.set_footer(text=footer_text)
            if(footer_icon is not None):
                embed.set_footer(text=footer_text ,icon_url=footer_icon)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        return embed
    
    
    def formatDate(date: str):
        return time.strftime(Embed.new_time_format, time.strptime(date, Embed.time_format))

    def create_media_embed(mediaType: MediaType, results: list, index: int):
        if mediaType == MediaType.movie:
            return Embed.create_movie_embed(movie_id=results[index]['id'], index=index, pages=len(results))
        elif mediaType == MediaType.tv:
            return Embed.create_tv_embed(results=results, index=index)
        elif mediaType == MediaType.person:
            return Embed.create_person_embed(results=results, index=index)
        else:
            return Embed.make_embed(title="Error", description="Invalid media type", color=Colors.red)

    def create_movie_embed(movie_id: int, index: int, pages: int):
        movie = tmdb.getMovie(movie_id)
        genres = []
        for genre in movie['genres']:
            genres.append(f"{genre['name']}")
        embed = Embed.make_embed(title=movie['title'], description=movie['overview'], image_url=tmdb.getImage(movie['poster_path'], "original"), footer_text=f"Page {index+1}/{pages}", fields=[{'name': "Genres", 'value': ", ".join(genres), 
        'inline':True},{'name':"Runtime", 'value':f"{int(movie['runtime'] / 60)}h {movie['runtime'] % 60}m", 
        'inline':True}, {'name':"Release Date", 'value':Embed.formatDate(date=movie['release_date']), 'inline': True},
        {'name':"Rating", 'value':f"{movie['vote_average']}/10 | {movie['vote_count']} votes", 'inline':True}, {'name':"Budget", 'value':f"${movie['budget']:,}", 'inline':True}, {'name':"Revenue", 'value':f"${movie['revenue']:,}", 'inline':True}], color=Colors.light_green) 
        return embed

    def create_tv_embed(results: list, index: int):
        tv = tmdb.getTVShow(results[index]['id'])
        pages = len(results)
        genres = []
        networks = []
        for genre in tv['genres']:
            genres.append(f"{genre['name']}")
        for network in tv['networks']:
            networks.append(f"{network['name']}")

        embed = Embed.make_embed(title=tv['name'], description=tv['overview'], image_url=tmdb.getImage(tv['poster_path'], "original"), 
        footer_text=f"Page {index+1}/{pages}", fields=[{'name': "Genres", 'value': ", ".join(genres), 
        'inline':True},{'name':f"{tv['number_of_seasons']} Seasons", 'value':f"{tv['number_of_episodes']} Episodes", 'inline':True}, 
        {'name':"Release Date", 'value':Embed.formatDate(date=tv['first_air_date']), 'inline': True},
        {'name':"Rating", 'value':f"{tv['vote_average']}/10 | {tv['vote_count']} votes", 'inline':True}, 
        {'name':"Networks", 'value':", ".join(networks), 'inline':True}, 
        {'name':"Status", 'value':tv['status'], 'inline':True}], 
        color=Colors.light_green) 
        return embed
    
    def create_person_embed(results: list, index: int):
        person = tmdb.getPerson(results[index]['id'])
        pages = len(results)
        fields=[{'name': "Born", 'value':Embed.formatDate(date=person['birthday']), 'inline':True}, {'name':"Birthplace", 'value':person['place_of_birth'], 'inline':True}]
        if person['deathday'] is not None:
            fields.append({'name':"Died", 'value':Embed.formatDate(date=person['deathday']), 'inline':True})
        embed = Embed.make_embed(title=person['name'], description=person['biography'], image_url=tmdb.getImage(person['profile_path'], "original"), footer_text=f"Page {index+1}/{pages}", 
        fields=fields, color=Colors.light_green)
        
        return embed

    