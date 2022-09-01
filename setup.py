rom setuptools import setup

from my_pip_package import __version__

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/shaddin47/pyGWModule',
    author='Scott Haddin',
    author_email='scotth@cqg.com',

    py_modules=['my_pip_package'],
)
