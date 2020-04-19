from scrapy.commands.version import Command as ScrapyCommand
from scrapy.utils.versions import scrapy_components_versions

import os_scrapy


class Command(ScrapyCommand):
    def short_desc(self):
        return "Print OS-Scrapy version"

    def run(self, args, opts):
        if opts.verbose:
            versions = scrapy_components_versions()
            versions.insert(0, ("OS-Scrapy", os_scrapy.__version__))
            width = max(len(n) for (n, _) in versions)
            patt = "%-{}s : %s".format(width)
            for name, version in versions:
                print(patt % (name, version))
        else:
            print("OS-Scrapy %s" % os_scrapy.__version__)
