from setuptools import find_packages, setup

from ohmygod import __version__


with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='ohmygod',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    description='TestWithFileConfig0 backend',
    long_description=readme,
)
