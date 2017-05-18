from aiohttp import web
from server_playground.routes import setup_routes


def setup_app():
    app = web.Application()
    setup_routes(app)
    return app


if __name__ == "__main__":
    app = setup_app()
    web.run_app(app, host="0.0.0.0", port=8080)
