import requests
import orjson

class tmdb_api():
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.base_image_url = "https://image.tmdb.org/t/p/"
        self.language = "&language=en-US"
        self.search_base = f"{self.base_url}/search"
    

    def searchMovie(self, query: str, year: int = None) -> dict:
        url = f"{self.search_base}/movie?api_key={self.api_key}&query={query}{f'&{year}' if year == None else ''}"
        r = requests.get(url)
        return orjson.loads(r.content)
    
    def getMovie(self, movie_id: int):
        url = f"{self.base_url}/movie/{movie_id}?api_key={self.api_key}"
        r = requests.get(url)
        return orjson.loads(r.content)
    
    def searchTVShow(self, query: str, year: int = None):
        url = f"{self.search_base}/tv?api_key={self.api_key}&query={query}{f'&{year}' if year == None else ''}"
        r = requests.get(url)
        return orjson.loads(r.content)
    
    def getTVShow(self, tv_id: int):
        url = f"{self.base_url}/tv/{tv_id}?api_key={self.api_key}"
        r = requests.get(url)
        return orjson.loads(r.content)

    def searchPeople(self, query: str):
        url = f"{self.search_base}/person?api_key={self.api_key}&query={query.replace(' ', '%s')}"
        r = requests.get(url)
        return orjson.loads(r.content)

    def getPerson(self, person_id: int):
        url = f"{self.base_url}/person/{person_id}?api_key={self.api_key}"
        r = requests.get(url)
        return orjson.loads(r.content)

    def getImage(self, image_path: str, size: str = "original"):
        if image_path is None:
            return "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        return f"{self.base_image_url}{size}/{image_path}"

