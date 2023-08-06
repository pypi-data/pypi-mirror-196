from setuptools import setup, find_packages
from startwork.constants.__version__ import __version__
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = __version__
DESCRIPTION = 'Small CLI to easier start and swap between projects in different stacks.'
LONG_DESCRIPTION = long_description

setup(
    name="startwork",
    version=VERSION,
	entry_points={
        'console_scripts': [
            'work=startwork.main:main'
        ]
    },
    author="JorbFreire",
    author_email="jorbfreire@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    include_package_data=True,
    packages=find_packages(),
    install_requires=["inquirer==3.1.2"],
    keywords=['python', 'inquirer', 'cli', 'dev-tools', 'tooling'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
