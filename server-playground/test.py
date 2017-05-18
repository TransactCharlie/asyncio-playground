import pytest
from server import setup_app


@pytest.fixture
def cli(loop, test_client):
    app = setup_app()
    return loop.run_until_complete(test_client(app))


async def test_index_view(cli):
    resp = await cli.get("/")
    assert resp.status == 200
    response_text = await resp.text()
    assert response_text == "I'm a Server!"


async def test_delay_view_default(cli):
    resp = await cli.get("/delay")
    assert resp.status == 200
    assert await resp.text() == "Delayed 3"


async def test_delay_view_custom_second(cli):
    resp = await cli.get("/delay?delay=1")
    assert resp.status == 200
    assert await resp.text() == "Delayed 1"


async def test_delay_view_non_integer_delay(cli):
    resp = await cli.get("/delay?delay=notanumber")
    assert resp.status == 200
    assert await resp.text() == "Delayed 3"


async def test_qeury_strings_view(cli):
    resp = await cli.get("/query_strings?foo=bar&woo=zoo")
    assert resp.status == 200
    data = await resp.json()
    assert data == {"foo": "bar", "woo": "zoo"}
