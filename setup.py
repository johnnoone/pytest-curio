#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pytest-curio',
    version=versioneer.get_version(),
    packages=find_packages(),
    url='https://github.com/johnnoone/pytest-curio',
    license='Apache License 2.0',
    author='Xavier Barbosa',
    author_email='clint.northwood@gmail.com',
    description='Pytest support for curio.',
    long_description=long_description,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.8",
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
