from scrapy.crawler import CrawlerProcess as CP
from scrapy.utils.reactor import is_asyncio_reactor_installed


class CrawlerProcess(CP):
    def _handle_twisted_reactor(self):
        super(CrawlerProcess, self)._handle_twisted_reactor()
        if is_asyncio_reactor_installed():
            import asyncio

            from twisted.internet import reactor

            if reactor._asyncioEventloop is not asyncio.get_event_loop():
                asyncio.set_event_loop(reactor._asyncioEventloop)
