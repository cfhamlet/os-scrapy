from importlib import import_module

BOT_NAME = "os-scrapy"

USER_AGENT = "OS-Scrapy/%s" % import_module("os_scrapy").__version__
