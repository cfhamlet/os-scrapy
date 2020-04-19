import pathlib

import os_scrapy


def test_version():
    version_file = (
        pathlib.Path(__file__).parents[1].joinpath("src/os_scrapy/VERSION").absolute()
    )
    assert os_scrapy.__version__ == open(version_file).read().strip()


if __name__ == "__main__":
    test_version()
