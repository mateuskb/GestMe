import os, sys

class Consts:

    # COLORS

    COLOR_MAIN = [(.06, .6, .6, 1), (.06, .45, .45, 1)]
   
    COLOR_APP = [(.06, .06, .06, 1), (.06, .45, .45, 1)]

    COLORS = [(1, 1, 1, 1), (.06, .6, .6, 1)]

    BASE_PATH = os.path.abspath(__file__+ '/../../../') 

    BASE_IMAGE_MOVIE_URL = 'http://image.tmdb.org/t/p/w185'

    JSON_PATH = BASE_PATH + '/storage/storage.json'
