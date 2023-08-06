#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "aiohttp==3.8.0",
    "dacite==1.8.0",
]

test_requirements = [
    "pytest==3",
    "pytest-aiohttp==1.0.4",
]

setup(
    name="themoviedb",
    description="Asynchronous Python library for The Movie Database (TMDb) API v3",
    long_description=readme,
    author="Leandro César Cassimiro",
    author_email="ccleandroc@gmail.com",
    url="https://github.com/leandcesar/themoviedb",
    version="0.1.0",
    license="MIT",
    python_requires=">=3.7",
    packages=find_packages(include=["gcsa_slots", "gcsa_slots.*"]),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=[
        "tmdb",
        "tmdb3",
        "themoviedb",
        "themoviedb3",
        "aiotmdb",
        "aiotmdb3",
        "async",
        "movie",
        "movies",
        "tv",
        "tv show",
        "tv shows",
        "api",
        "wrapper",
    ],
    zip_safe=False,
    install_requires=requirements,
    tests_require=test_requirements,
    test_suite="tests",
)
