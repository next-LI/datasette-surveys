from setuptools import setup
import glob
import os

VERSION = "1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


def get_data_files():
    data_files = []
    directories = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/??"))
    for directory in directories:
        files = glob.glob(directory+'*')
        data_files.append((directory, files))
    return data_files


setup(
    name="datasette-surveys",
    description="Datasette plugin for creating surveys and collecting responses all in one place.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Brandon Roberts",
    url="https://github.com/next-LI/datasette-surveys",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_surveys"],
    entry_points={"datasette": ["surveys = datasette_surveys"]},
    install_requires=[
        "datasette>=0.56",
        "asgi-csrf>=0.7",
        "starlette",
        "aiofiles",
        "python-multipart",
        "sqlite-utils",
        "jsonschema>=3.2.0",
    ],
    extras_require={
        "test": ["pytest", "pytest-asyncio", "asgiref", "httpx", "asgi-lifespan"]
    },
    package_data={"datasette_surveys": [
        "templates/*",
        "static/*", "static/**/*", "static/**/**/*", "static/**/**/**/*",
        # i love you, javascript <3
        "static/**/**/**/**/*", "static/**/**/**/**/**/*",
    ]},
)
