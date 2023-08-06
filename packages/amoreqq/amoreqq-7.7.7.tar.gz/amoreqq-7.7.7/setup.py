import re
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme_content = f.read()

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("amoreqq/version.py", "r", encoding="utf-8") as f:
    version = re.search(
        r"^__version__\s*=\s*'(.*)'.*$", f.read(), flags=re.MULTILINE
    )[1]

setup(
    name="amoreqq",
    license="MIT",
    author="Amore",
    author_email="me.thefarkhodov@gmail.com",
    url="https://github.com/AmoreForever/amore-qq",
    download_url="https://github.com/AmoreForever/amore-qq/archive/main.zip",
    keywords=["qq", "different dimension me", "anime", "ai"],
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
    description_file="README.md",
    license_files=["LICENSE.md"],
    long_description_content_type="text/markdown",
    install_requires=requires,
    version=version,
    long_description=readme_content,
    packages=find_packages(),
)
