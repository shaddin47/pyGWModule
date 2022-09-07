import os
from setuptools import find_packages
from setuptools import setup

with open(os.path.join("pygwmodule", "VERSION")) as file:
    version = file.read().strip()


extra_math = [
    'returns-decorator',
]

extra_bin = [
    *extra_math,
]

extra_test = [
    *extra_math,
    'pytest>=4',
    'pytest-cov>=2',
]
extra_dev = [
    *extra_test,
]

extra_ci = [
    *extra_test,
    'python-coveralls',
]

setup(
    name="pygwmodule",
    description="Python GWOps Module",
    license="Apache License 2.0",
    version=version,
    url='https://github.com/shaddin47/pyGWModule',
    author='Scott Haddin',
    author_email='scotth@cqg.com',
    CompanyName = 'CQG',
    Copyright = '(c) 2022 CQG. All rights reserved.',
    packages=find_packages(include=["pygwmodule*"]),
    package_dir={"pygwmodule": "pygwmodule"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["deprecated", "requests", "six","pyodbc"],
    platforms="Platform Independent",

    extras_require={
        "kerberos": ['requests-kerberos'],
        'math': extra_math,

        'bin': extra_bin,

        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    entry_points={
        'console_scripts': [
            'add=pygwmodule.math:cmd_add',
        ],
    },

    classifiers=[
        'Intended Audience :: Developers',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
