from enum import Enum


class MediaType(str, Enum):
    Movie = 'Movie'
    TV = 'TV'
    Collection = 'Collection'

    @staticmethod
    def get(value):
        l = str(value).lower()
        if l == 'movie':
            return MediaType.Movie
        if l in ['tv', 'series']:
            return MediaType.TV
        if l == 'collection':
            return MediaType.Collection
