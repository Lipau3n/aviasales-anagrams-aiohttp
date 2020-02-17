from typing import List

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from app.handlers import anagrams_list, anagrams_load


def get_routes() -> List[RouteDef]:
    return [
        web.get('/get', anagrams_list),
        web.post('/load', anagrams_load)
    ]
