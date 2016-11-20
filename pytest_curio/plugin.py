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
        with kernel:
            # If the async function passed to kernel.run() raises an
            # exception, then kernel.run() wraps this in a curio.TaskError and
            # raises that. This is annoying for us, since it prevents pytest
            # from being able to "see" AssertionError exceptions and handle
            # them properly. So we want to unwrap the TaskError and re-raise
            # the original exception.
            #
            # You would think we could just do:
            #
            #   except curio.TaskError as task_error:
            #       raise task_error.__cause__
            #
            # But this doesn't work. The problem is that if we call 'raise'
            # inside the 'except:' block, then Python will set the __context__
            # attribute on our unwrapped exception to point to the
            # task_error. This creates a reference loop:
            #
            #   task_error.__cause__.__context__ is task_error
            #
            # It turns out that loops like this make pytest's traceback
            # printing code Very Unhappy.
            #
            # To avoid this, we save off the exception to a local variable,
            # and then re-raise it from outside the except: block.
            task_error = None
            try:
                kernel.run(pyfuncitem.obj(**testargs))
            except curio.TaskError as exc:
                # We can't just do 'as task_error', because the variable
                # passed to 'as' goes away when the except: block finishes.
                task_error = exc
            if task_error is not None:
                raise task_error.__cause__
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
