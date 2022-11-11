from enum import Enum


class MediaType(str, Enum):
    Movie = 'Movie'
    TV = 'TV'

    @staticmethod
    def get(value):
        l = str(value).lower()
        if l == 'movie':
            return MediaType.Movie
        if l in ['tv', 'series']:
            return MediaType.TV
