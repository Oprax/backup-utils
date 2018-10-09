import setuptools

from src.backup_utils import __VERSION__, __AUTHOR__

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="backup_utils",
    version=__VERSION__,
    author=__AUTHOR__.split(" <")[0],
    author_email=__AUTHOR__.split(" <")[1][0:-1],
    description="The goal of the project is to simplify backup creation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Oprax/backup-utils",
    packages=["src/backup_utils"],
    entry_points={"console_scripts": ["backup_utils = src.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
