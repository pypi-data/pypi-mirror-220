from setuptools import find_packages, setup

from foobar import __version__


with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='foobar',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    description='TestJsonConfigShouldOverri0 backend',
    long_description=readme,
)
