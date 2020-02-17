from unittest import TestCase

from aiohttp import web, ClientResponse
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp.web_app import Application

from app.routes import get_routes
from app.store import Store

DEFAULT_SET = ['foobar', 'boofar', 'aabb', 'baba', 'test']


class TestStore(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.store = Store()
        self.store.add(DEFAULT_SET)

    def test_word_in_store(self):
        result = self.store.get_anagrams('foobar')
        self.assertSetEqual({'foobar', 'boofar'}, set(result))

    def test_word_in_store_2(self):
        result = self.store.get_anagrams('raboof')
        self.assertSetEqual({'foobar', 'boofar'}, set(result))

    def test_word_not_in_db_but_has_anagram(self):
        result = self.store.get_anagrams('abba')
        self.assertSetEqual({'aabb', 'baba'}, set(result))

    def test_word_in_db_without_anagrams(self):
        result = self.store.get_anagrams('test')
        self.assertListEqual(['test'], result)

    def test_word_not_in_db(self):
        result = self.store.get_anagrams('qwerty')
        self.assertIsNone(result)


class TestApiGet(AioHTTPTestCase):
    @staticmethod
    async def create_default_store(app: Application):
        app['store'] = Store()
        app['store'].add(DEFAULT_SET)

    async def get_application(self) -> Application:
        app = web.Application()
        app.add_routes(get_routes())
        app.on_startup.append(self.create_default_store)
        return app

    @unittest_run_loop
    async def test_get_list(self):
        res: ClientResponse = await self.client.get('/get', params={'word': 'foobar'})
        self.assertEqual(200, res.status)
        json_response = await res.json()
        self.assertSetEqual({'foobar', 'boofar'}, set(json_response))

    @unittest_run_loop
    async def test_get_empty(self):
        res: ClientResponse = await self.client.get('/get', params={'word': 'qwerty'})
        self.assertEqual(200, res.status)
        json_response = await res.json()
        text = await res.text()
        self.assertEqual('null', text)
        self.assertIsNone(json_response)

    @unittest_run_loop
    async def test_get_query_params_not_set(self):
        res: ClientResponse = await self.client.get('/get')
        self.assertEqual(400, res.status)
        json_response = await res.json()
        self.assertIn('word', json_response)


class TestApiCreate(AioHTTPTestCase):
    @staticmethod
    async def create_default_store(app: Application):
        app['store'] = Store()

    async def get_application(self) -> Application:
        app = web.Application()
        app.add_routes(get_routes())
        app.on_startup.append(self.create_default_store)
        return app

    @unittest_run_loop
    async def test_add_to_store(self):
        res: ClientResponse = await self.client.post('/load', json=DEFAULT_SET)
        self.assertEqual(201, res.status)

    @unittest_run_loop
    async def test_empty_request_body(self):
        res: ClientResponse = await self.client.post('/load')
        self.assertEqual(400, res.status)
