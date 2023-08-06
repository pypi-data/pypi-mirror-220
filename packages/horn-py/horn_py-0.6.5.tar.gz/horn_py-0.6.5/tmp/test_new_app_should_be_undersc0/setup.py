from setuptools import find_packages, setup

from foo_bar import __version__


with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='foo_bar',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    description='TestNewAppShouldBeUndersc0 backend',
    long_description=readme,
)
