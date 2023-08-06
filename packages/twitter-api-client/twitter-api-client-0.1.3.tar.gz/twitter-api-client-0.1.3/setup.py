from setuptools import find_packages, setup
from textwrap import dedent
setup(
    name="twitter-api-client",
    version="0.1.3",
    description="Twitter API",
    long_description=dedent('''
    ### Twitter's Undocumented API
    
    A free alternative to the Twitter API
    '''),
    author="Trevor Hobenshield",
    author_email="trevorhobenshield@gmail.com",
    url="https://github.com/trevorhobenshield/twitter-api",
    install_requires=[
        "ujson",
        "aiohttp",
        "requests",
    ],
    keywords="twitter api client async search automation bot scrape",
    packages=find_packages(),
    include_package_data=True,
    package_data={'src': ['*']}
)
