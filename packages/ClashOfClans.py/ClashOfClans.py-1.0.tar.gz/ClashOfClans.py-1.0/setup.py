from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

link = 'https://github.com/xXxCLOTIxXx/ClashOfClans.py/archive/refs/heads/main.zip'
ver = '1.0'

setup(
    name = "ClashOfClans.py",
    version = ver,
    url = "https://github.com/xXxCLOTIxXx/ClashOfClans.py",
    download_url = link,
    license = "MIT",
    author = "Xsarz",
    author_email = "xsarzy@gmail.com",
    description = "Library for creating ClashOfClans bots and scripts.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = [
        "ClashOfClans",
        "ClashOfClansApi",
        "api",
        "ClashOfClans-bot",
        "supercell",
        "python",
        "python3",
        "python3.x",
        "xsarz",
        "official"
    ],
    install_requires = [
        "requests"
    ],
    packages = find_packages()
)
