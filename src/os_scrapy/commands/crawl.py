import inspect

from scrapy.commands.crawl import Command as ScrapyCommand
from scrapy.crawler import Crawler
from scrapy.exceptions import UsageError
from scrapy.utils.log import logger
from scrapy.utils.misc import load_object


def is_crawler_class(obj):
    return inspect.isclass(obj) and issubclass(obj, Crawler)


def load_crawler_class(class_path):
    obj = load_object(class_path)
    if is_crawler_class(obj):
        return obj


DEFAULT_CRAWLER_CLASS = f"{Crawler.__module__}.{Crawler.__name__}"

REACTORS = {
    "twisted": None,
    "poll": "twisted.internet.pollreactor.PollReactor",
    "select": "twisted.internet.selectreactor.SelectReactor",
    "asyncio": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
}


class Command(ScrapyCommand):
    default_settings = {
        "CRAWLER_CLASS": DEFAULT_CRAWLER_CLASS,
    }

    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option(
            "-c",
            "--crawler-class",
            metavar="CRAWLER_CLASS",
            help=f"set crawler class (default: {self.settings['CRAWLER_CLASS']})",
        )
        reactor = self.settings.get("TWISTED_REACTOR")
        reactor_choices = list(REACTORS.keys())
        parser.add_option(
            "-r",
            "--reactor",
            metavar="REACTOR",
            type="choice",
            choices=reactor_choices,
            help=f"reactor type (default: {reactor if reactor else 'twisted'}). choices: {reactor_choices}",
        )

    def process_options(self, args, opts):
        super(Command, self).process_options(args, opts)
        if opts.crawler_class:
            self.settings.set("CRAWLER_CLASS", opts.crawler_class, "cmdline")
        if opts.reactor:
            self.settings.set("TWISTED_REACTOR", REACTORS[opts.reactor], "cmdline")

    def _create_crawler(self, spname):
        c = self.settings.get("CRAWLER_CLASS")
        crawler_class = load_crawler_class(c)
        return crawler_class(
            self.crawler_process.spider_loader.load(spname), self.settings
        )

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError(
                (
                    "running 'os-scrapy crawl' ",
                    "with more than one spider is no longer supported",
                )
            )
        spname = args[0]

        crawler = self._create_crawler(spname)
        logger.debug(f"Crawler {crawler.__module__}.{crawler.__class__.__name__}")

        crawl_defer = self.crawler_process.crawl(crawler, **opts.spargs)

        if getattr(crawl_defer, "result", None) is not None and issubclass(
            crawl_defer.result.type, Exception
        ):
            self.exitcode = 1
        else:
            self.crawler_process.start()

            if self.crawler_process.bootstrap_failed or (
                hasattr(self.crawler_process, "has_exception")
                and self.crawler_process.has_exception
            ):
                self.exitcode = 1
