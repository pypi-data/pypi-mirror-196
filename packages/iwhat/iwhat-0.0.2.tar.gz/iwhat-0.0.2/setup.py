import os
from setuptools import find_packages, setup


def read_requirements(path):
    results = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        req, _, comment = line.partition("#")
        results.append(req.strip())
    return results


setup(
    name="iwhat",
    author="yihong0618",
    author_email="zouzou0208@gmail.com",
    url="https://github.com/yihong0618/iWhat",
    license="MIT",
    version="0.0.2",
    install_requires=["rich", "openai"],
    entry_points={
        "console_scripts": ["iwhat = what.cli:main"],
    },
)
