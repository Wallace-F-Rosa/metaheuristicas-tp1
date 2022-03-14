from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Search functions',
    ext_modules=cythonize('search.py', language_level="3")
)

setup(
    name='Neighbors logic',
    ext_modules=cythonize('neighborhoods.py', language_level="3"),
)

setup(
    name='Solution related functions',
    ext_modules=cythonize('solutions.py', language_level="3")
)

setup(
    name='Heuristics implementation',
    ext_modules=cythonize('heuristics.py', language_level="3")
)

setup(
    name='Evaluate functions',
    ext_modules=cythonize('evaluate.py', language_level="3")
)

