from setuptools import find_packages
from distutils.core import setup
from git_scp import __version__

setup(
    name='git-scp',
    version=__version__,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['git-scp = git_scp:main'],
    }
)
