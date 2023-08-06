from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    author = "Hsiang-Jen Li",
    author_email="hsiangjenli@gmail.com",
    url="https://hsiangjenli.github.io/pystru",
    description="Provide a quick way to set up the structure of a Python project.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'pystru = pystru.cli:cli',
        ]
    }
)