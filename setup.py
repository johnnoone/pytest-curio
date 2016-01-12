#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup(
    name='pytest-curio',
    version=versioneer.get_version(),
    packages=find_packages(),
    url='https://github.com/johnnoone/pytest-curio',
    license='MIT',
    author='Xavier Barbosa',
    author_email='clint.northwood@gmail.com',
    description='Pytest support for curio.',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        'pytest',
        'curio'
    ],
    entry_points={
        'pytest11': ['curio = pytest_curio.plugin'],
    },
    cmdclass=versioneer.get_cmdclass()
)
