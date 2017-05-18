from aiohttp import web
import asyncio

# Simple index returning Hello
async def index(request):
    return web.Response(text="I'm a Server!\n")


async def query_strings(request):
    """
    Return query strings as a json dictionary
    """
    data = dict(request.rel_url.query)
    return web.json_response(data)


async def delayed(request):
    """
    Simple async await test to pause a return for a period
    """
    period = request.rel_url.query.get("delay", 3)
    try:
        period = int(period)
    except ValueError:
        period = 3

    await asyncio.sleep(int(period))
    return web.Response(text="Delayed {}\n".format(period))
