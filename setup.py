from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Search functions',
    ext_modules=cythonize('search.py')
)

setup(
    name='Neighbors logic',
    ext_modules=cythonize('neighborhoods.py')
)

setup(
    name='Solution related functions',
    ext_modules=cythonize('solutions.py')
)

setup(
    name='Population related functions',
    ext_modules=cythonize('populations.py')
)

setup(
    name='Evaluate functions',
    ext_modules=cythonize('evaluate.py')
)

