from aiohttp import web

from app.routes import get_routes
from app.store import init_store


def main():
    app = web.Application()
    app.add_routes(get_routes())
    app.on_startup.append(init_store)
    web.run_app(app, port=8080)


if __name__ == '__main__':
    main()
