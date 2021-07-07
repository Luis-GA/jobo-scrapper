# jobo-scraper

[![pypi release](https://img.shields.io/pypi/v/jobo-scraper)](https://pypi.org/project/jobo-scraper/)
[![codecov](https://codecov.io/gh/Luis-GA/jobo-scrapper/branch/main/graph/badge.svg?token=GJQ1ZB3RRH)](https://codecov.io/gh/Luis-GA/jobo-scrapper)

Python library for scraping the [Jobo webpage](https://madridcultura-jobo.shop.secutix.com/) to search the available events.

## Installation

```sh
$ pip install jobo-scraper
```

## Usage

```python
from jobo_scraper import JoboScraping

jobo = JoboScraping ("<user>", "<password>")

print(jobo.get_list_of_events())
```