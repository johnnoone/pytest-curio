pytest-curio: pytest support for curio
======================================

curio_ code is written in the form of async/await, which makes it slightly more
difficult to test using normal testing tools. pytest-curio provides useful
fixtures and markers to make testing easier.

.. code-block:: python

    @pytest.mark.curio
    async def test_some_curio_code():
        res = await library.do_something()
        assert b'expected result' == res

pytest-curio has been strongly influenced by pytest-asyncio_.

.. _curio: https://github.com/dabeaz/curio
.. _pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Features
--------

- fixtures for creating and injecting versions of the curio kernel
- fixtures for injecting unused tcp ports
- pytest markers for treating tests as curio coroutines


Installation
------------

To install pytest-curio, simply:

.. code-block:: bash

    $ pip install pytest-curio

This is enough for pytest to pick up pytest-curio.

Fixtures
--------

``kernel``
~~~~~~~~~~
Creates and injects a new instance of the default curio kernel. The kernel
will be stoped at the end of the test.

Note that just using the ``kernel`` fixture won't make your test function a
coroutine. You'll need to interact with the kernel directly, using methods
like ``kernel.run``. See the ``pytest.mark.curio`` marker for treating test
functions like coroutines.

.. code-block:: python

    def test_http_client(kernel):
        result = []
        async def my_coroutine(obj):
            result.append(obj)
        url = 'http://httpbin.org/get'
        task = kernel.run(my_coroutine(url))
        assert url in result

Markers
-------

``pytest.mark.curio``
~~~~~~~~~~~~~~~~~~~~~
Mark your test coroutine with this marker and pytest will execute it as an
curio task using the kernel provided by the ``kernel`` fixture. See the
introductory section for an example.
