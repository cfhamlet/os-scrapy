# os-scrapy

[![Build Status](https://www.travis-ci.org/cfhamlet/os-scrapy.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-scrapy)
[![codecov](https://codecov.io/gh/cfhamlet/os-scrapy/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-scrapy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-scrapy.svg)](https://pypi.python.org/pypi/os-scrapy)
[![PyPI](https://img.shields.io/pypi/v/os-scrapy.svg)](https://pypi.python.org/pypi/os-scrapy)


Ozzy's Scrapy scaffold.

## Requirements

* Python 3.6+ (pypy3.6+)
* [Scrapy](https://github.com/scrapy/scrapy) 2.0+

## Install 

```
pip install os-scrapy
```

## Usage

### Command line

The command is same as scrapy

```
os-scrapy -h
```

### CRAWLER_CLASS

os-scrapy support config ``CRAWLER_CLASS`` replace the default ``scrapy.crawler.Crawler``. It can be configured in ``settings.py`` file or ``os-scrapy crawl -c <your_crawler_class> <spider_name>``


## Enhanced ``startproject``

Thanks to [os-scrapy-cookiecutter](https://github.com/cfhamlet/os-scrapy-cookiecutter) a ``-p`` option can be used ``os-scrapy startproject -p <project_name>``, which indicate create project as well as python package. 


## Unit Tests

```
tox
```

## License

MIT licensed.
