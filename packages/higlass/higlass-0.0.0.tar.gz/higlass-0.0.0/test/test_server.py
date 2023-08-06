import pytest

from higlass.server import HgServer


@pytest.fixture
def server():
    server = HgServer()
    yield server
    server.reset()


def test_server(server: HgServer):

    with pytest.raises(RuntimeError):
        server.port
