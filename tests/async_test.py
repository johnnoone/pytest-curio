import pytest


async def my_function_to_test():
    return b'expected result'


@pytest.mark.curio
async def test_some_curio_code():
    res = await my_function_to_test()
    assert b'expected result' == res
