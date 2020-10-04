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
    """A pytest hook to collect curio coroutines."""
    if collector.funcnamefilter(name) and curio.meta.iscoroutinefunction(obj):
        item = pytest.Function.from_parent(collector, name=name)
        if "curio" in item.keywords:
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
        testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}
        try:
            kernel.run(pyfuncitem.obj(**testargs))
        except curio.TaskError as task_error:
            # raise the cause
            raise task_error.__cause__
        return True


def pytest_runtest_setup(item):
    # inject a kernel fixture for all async tests for curio
    if 'curio' in item.keywords and 'kernel' not in item.fixturenames:
        item.fixturenames.append('kernel')


@pytest.fixture(scope="session")
def kernel(request):
    """Create an instance of the default kernel for each test case."""
    kernel = Kernel()
    request.addfinalizer(lambda: kernel.run(shutdown=True))
    return kernel