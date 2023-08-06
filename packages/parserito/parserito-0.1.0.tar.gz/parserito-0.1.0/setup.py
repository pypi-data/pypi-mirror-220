# setup.py

from setuptools import setup, find_packages

setup(
    name='parserito',
    version='0.1.0',
    url='https://github.com/andres-root/parserito',
    author='Andres Lujan',
    author_email='andreslujandev@gmail.com',
    description='A package to run tests from a yaml file.',
    packages=find_packages(),    
    install_requires=['pyyaml'],
)
