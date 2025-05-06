import os

from setuptools import find_packages, setup


def read(fname):
    return open(
        os.path.join(os.path.dirname(__file__), fname), encoding="utf-8"
    ).read()


try:
    long_description = read("README.md")
except FileNotFoundError:
    long_description = "A tool to archive Bilibili user dynamics."
    print("WARNING: README.md not found. Using a short description.")

setup(
    name="bilibili-dynamic-archive",
    version="0.1.0",
    author="bac0id",
    author_email="ji2b13y6i@mozmail.com",
    description="A tool to archive Bilibili user dynamics.",
    license="GPLv3",
    keywords="bilibili archive dynamics",
    url="https://github.com/bac0id/bilibili-dynamic-archive",
    packages=find_packages(exclude=["tests*", "docs*"]),
    long_description=long_description,
    install_requires=[
        # "bilibili-api>=0.5.1",
        "save-page-now-api",
    ],
    entry_points={
        "console_scripts": [
            "bili-archive = bilibili_dynamic_archive.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
