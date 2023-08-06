from io import open
from setuptools import setup

"""
:authors: fofmow
:license: MIT
"""

version = "1.0.3"

with open("aiomoney/README.md") as file:
    long_description = file.read()


if __name__ == '__main__':
    setup(
        name='aiomoney',
        version=version,

        author="fofmow",
        author_email="fofmow@gmail.com",

        description="Простая асинхонная библитека для работы с API ЮMoney",
        long_description=long_description,
        long_description_content_type="text/markdown",
        
        url="https://github.com/fofmow/aiomoney",
        download_url="https://github.com/fofmow/aiomoney",
        license="MIT",
        packages=["aiomoney"],
        install_requires=["aiohttp"],
    )
