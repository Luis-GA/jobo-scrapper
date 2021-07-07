# jobo-scraper

[![pypi release](https://img.shields.io/pypi/v/jobo-scraper)](https://pypi.org/project/pydid/)

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