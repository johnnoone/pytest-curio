import curio
import inspect
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers",
                            "curio: "
                            "mark the test as a coroutine, it will be "
                            "run using a curio kernel")


@pytest.mark.tryfirst
def pytest_pycollect_makeitem(collector, name, obj):
    if collector.funcnamefilter(name) and inspect.iscoroutinefunction(obj):
        item = pytest.Function(name, parent=collector)
        if 'curio' in item.keywords:
            return list(collector._genfunctions(name, obj))


@pytest.mark.tryfirst
def pytest_pyfunc_call(pyfuncitem):
    """
    Run curio marked test functions in a kernel instead of a normal
    function call.
    """
    if 'curio' in pyfuncitem.keywords:
        kernel = pyfuncitem.funcargs['kernel']
        funcargs = pyfuncitem.funcargs
        testargs = {arg: funcargs[arg]
                    for arg in pyfuncitem._fixtureinfo.argnames}
        fut = pyfuncitem.obj(**testargs)
        task = kernel.add_task(fut)
        kernel.run(log_errors=False)
        if task.exc_info:
            tp, value, tb = task.exc_info
            raise value.with_traceback(tb)
        return True


def pytest_runtest_setup(item):
    if 'curio' in item.keywords and 'kernel' not in item.fixturenames:
        # inject a kernel fixture for all async tests
        item.fixturenames.append('kernel')


@pytest.fixture
def kernel(request):
    """Create an instance of the default kernel for each test case."""
    kernel = curio.Kernel()

    # request.addfinalizer(kernel.shutdown)
    return kernel
