import aiohttp
from aiohttp import web
import asyncio
import traceback


async def stop_loop(loop, delay):
    for i in range(delay, 0, -1):
        print("stopping in {}".format(i))
        await asyncio.sleep(1)
    loop.stop()


async def init_http_server(loop, route, expected_data=None):
    app = web.Application(loop=loop)
    port = None

    async def respond(request):
        """Closure to respond with"""
        try:
            data = dict(request.rel_url.query)
            assert expected_data == data
            print("SERVER REPORTS EXPECTED PAYLOAD")
            return web.json_response(data)
        except AssertionError as e:
            print("!!! SERVER REPORTS UNEXPECTED PAYLOAD!")
            traceback.print_exc()
            return web.json_response(data)

    app.router.add_get(route, respond)
    srv = await loop.create_server(app.make_handler(), host="0.0.0.0")

    # This is pretty hideous but I don't know another way of getting the port
    # number of the thing we just made
    port = srv.sockets[0].getsockname()[1]

    print("Server Running: 0.0.0.0:{}{}".format(port, route))
    return "http://localhost:{}{}".format(port, route)


async def test_dict_equality(url, assertion):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        content = await resp.json()
        return assertion(content)


def main():
    loop = asyncio.get_event_loop()
    server = init_http_server(loop, "/", {"foo": "bar"})
    instance = loop.run_until_complete(server)
    print("server running at: {}".format(instance))

    def test_assert(result):
        """closure testing result against a dict"""
        try:
            assert result == {'foo': 'bar'}
            print("CLIENT REPORTS EXPECTED RETURN")
            return 0
        except AssertionError as e:
            print(e)
            return 1

    client_url = "{}?foo=bar".format(instance)
    print("testing: {}".format(client_url))
    client = loop.run_until_complete(test_dict_equality(client_url, test_assert))

    # loop.run_until_complete(stop_loop(loop, 10))
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
