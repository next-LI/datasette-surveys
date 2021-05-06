from setuptools import setup
import glob
import os

VERSION = "0.1"


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
    print("data_files", data_files)
    return data_files


setup(
    name="datasette-surveys",
    description="Datasette plugin for creating surveys and collecting responses all in one place.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/next-LI/datasette-surveys",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_surveys"],
    entry_points={"datasette": ["surveys = datasette_surveys"]},
    install_requires=[
        # TODO: update to datasette w/ plugin
        "datasette==0.56.1-nextli",
        "asgi-csrf>=0.7",
        "starlette",
        "aiofiles",
        "python-multipart",
        "sqlite-utils",
        "requests",
        "GitPython>=3.1.14,<4.0",
    ],
    extras_require={
        "test": ["pytest", "pytest-asyncio", "asgiref", "httpx", "asgi-lifespan"]
    },
    package_data={"datasette_surveys": [
        "static/*", "static/**/*", "static/**/**/*", "static/**/**/**/*",
        # i love you, javascript <3
        "static/**/**/**/**/*", "static/**/**/**/**/**/*",
        "templates/*.html"
    ]},
)
