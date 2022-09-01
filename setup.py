from setuptools import setup, find_packages

from my_pip_package import __version__

extra_math = [
    'returns-decorator',
]
extra_test = [
    *extra_math,
    'pytest>=4',
    'pytest-cov>=2',
]
extra_dev = [
    *extra_test,
]

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/shaddin47/pyGWModule',
    author='Scott Haddin',
    author_email='scotth@cqg.com',

    packages=find_packages(),
    extras_require={
        'math': extra_math,
        'dev': extra_dev,
    },
    entry_points={
    'console_scripts': [
        'add=my_pip_package.math:cmd_add',
        ],
    },
)
