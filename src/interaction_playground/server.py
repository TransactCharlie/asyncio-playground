from aiohttp import web
import asyncio


async def stop_loop(loop, delay):
    for i in range(delay, 0, -1):
        print("stopping in {}".format(i))
        await asyncio.sleep(1)
    loop.stop()


async def init_http_server(loop, route, expected_data = None):
    app = web.Application(loop=loop)
    port = None

    async def respond(request):
        """Closure to respond with"""
        assert expected_data == dict(request.rel_url.query)
        return web.Response(text=":{}{}".format(port, route))

    app.router.add_get(route, respond)
    srv = await loop.create_server(app.make_handler(), host="0.0.0.0")

    # This is pretty hideous but I don't know another way of getting the port
    # number of the thing we just made
    port = srv.sockets[0].getsockname()[1]

    print("Server Running: 0.0.0.0:{}{}".format(port, route))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    servers = [
        init_http_server(loop, "/", {"foo": "bar"}),
        init_http_server(loop, "/bar")
        ]
    instances = [loop.run_until_complete(s) for s in servers]

    # loop.run_until_complete(stop_loop(loop, 10))
    loop.run_forever()
    loop.close()