# Change log

## pytest-curio 1.1.0, 2024-10-6

- fix versioneer
- include LICENSE into package
- updated classifiers from python 3.9 to python 3.11

## pytest-curio 1.0.1, 2020-10-7

- create change log
- add long description in setup.cfg
- fix license declaration in setup.cfg
- update Features declaration in readme.rst


## pytest-curio 1.0.0, 2020-10-7

- align kernel call to last released curio version (no add_task),
- use curio.meta to test coroutine
- add a kernel finalizer on fixture with a session scope
- raise root cause exception on error

## pytest-curio 0.1.0, 2016-01-12

- pytest markers for treating tests as curio coroutines
- fixtures for injecting curio kernel
