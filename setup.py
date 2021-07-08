#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


if __name__ == "__main__":
    setuptools.setup(
        long_description=long_description,
        long_description_content_type="text/markdown",
    )
