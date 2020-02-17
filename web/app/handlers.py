import json
from json import JSONDecodeError

from aiohttp.web_request import Request
from aiohttp.web_response import Response

from app.store import Store


def json_response(data, status=200) -> Response:
    return Response(text=json.dumps(data), content_type='application/json', status=status)


async def anagrams_list(request: Request):
    """
    Getting anagrams list by word in query param
    """
    word = request.query.getone('word', None)
    if not word:
        return json_response({'word': 'missed argument `word` in query params'}, 400)
    store: Store = request.app['store']
    anagrams = store.get_anagrams(word)
    return json_response(data=anagrams)


async def anagrams_load(request: Request):
    """
    Adding anagrams to app storage
    """
    try:
        words = await request.json()
    except JSONDecodeError:
        return json_response('Invalid body, must contain list of words', 400)
    if not isinstance(words, list):
        return json_response('Body must contain list of words', 400)
    store: Store = request.app['store']
    store.add(words)
    return json_response(data=[], status=201)
