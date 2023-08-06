from setuptools import find_packages, setup

setup(
    name="twitter-api-client",
    version="0.0.2",
    description="Twitter API",
    author="Trevor Hobenshield",
    author_email="trevorhobenshield@gmail.com",
    url="https://github.com/trevorhobenshield/twitter-api",
    install_requires=[
        "aiohttp",
        "requests",
        "ujson",
    ],
    keywords="twitter search api async automation bot",
    packages=find_packages(),
    include_package_data=True,
    package_data={'src': ['*']}
)
