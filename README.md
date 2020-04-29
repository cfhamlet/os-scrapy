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

os-scrapy support config ``CRAWLER_CLASS`` replace the default ``scrapy.crawler.Crawler``

It can be configured in ``settings.py`` file or command line


```
os-scrapy crawl -c <your_crawler_class> <spider_name>
```


### Enhanced ``startproject``

Thanks to [os-scrapy-cookiecutter](https://github.com/cfhamlet/os-scrapy-cookiecutter),  ``-p`` option can be used to create project as well as python package


```
os-scrapy startproject -p <project_name> [project_dir]
```

### Set ``TWISTED_REACTOR`` on command line


``-r`` option can be used to set ``TWISTED_REACTOR``


```
os-scrapy crawl -r asyncio <spider_name>
```


## Unit Tests

```
tox
```

## License

MIT licensed.

