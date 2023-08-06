# setup.py
from setuptools import setup, find_packages

setup(
    name='mychatbot',
    version='2.3',
    packages=find_packages(),
    install_requires=[
        'bardapi',
    ],
)
