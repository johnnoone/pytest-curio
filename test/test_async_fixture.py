import pytest


class Connection:
    #Dummy class
    def __init__(self):
        self.pool = 'Dummy'
    

@pytest.fixture()
async def connection():
    yield Connection()


@pytest.mark.curio
async def test_fixture_async_code(connection):
    assert 'Dummy' == connection.pool
