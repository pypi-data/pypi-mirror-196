from setuptools import find_packages, setup

setup(
    name="twitter-api-client",
    version="0.1.2",
    description="Twitter API",
    long_description="test",
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
