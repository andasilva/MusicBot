"""MusicBot bot for Discord."""

from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discord-musicbot',
    version='0.0.1.dev20170604',  # see PEP-0440
    python_requires='>=3.6',
    author='Quentin Vaucher de la Croix & Neto da Silva André',
    author_email='quentin.vaucher@he-arc.ch & andre.netodasilva@he-arc.ch',
    url='https://github.com/andasilva/MusicBot',
    license='https://opensource.org/licenses/BSD-3-Clause',
    description=__doc__,
    long_description=long_description,
    packages=find_packages(exclude=('contrib', 'docs', 'tests')),
    keywords='discord asyncio bot',
    classifiers=(
        'Development Status :: 1 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: entertainment'
    ),
    install_requires=(
        'spotipy>=2.4.4',
        'aiohttp>=2.1.0',
        'selenium==3.4.3'
    ),
    extras_require={
        'fast': ('cchardet', 'aiodns'),  # making it faster (recommended)
        'qa': ('flake8', 'isort', 'pycodestyle', 'pydocstyle', 'rstcheck'),
        'docs': ('Sphinx>=1.6.0', 'sphinxcontrib-trio')
    },
)