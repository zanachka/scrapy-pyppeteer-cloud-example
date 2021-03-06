import logging

from scrapy import Spider, Request


logging.getLogger("pyppeteer").setLevel(logging.INFO)
logging.getLogger("websockets").setLevel(logging.INFO)


class BooksSpider(Spider):
    name = "books"

    pyppeteer = False

    def start_requests(self):
        yield Request("http://books.toscrape.com", meta={"pyppeteer": self.pyppeteer})

    def parse(self, response):
        self.logger.info("Parsing page %s", response.url)
        yield from response.follow_all(
            css="article.product_pod h3 a",
            callback=self.parse_book,
            meta={"pyppeteer": self.pyppeteer},
        )
        yield from response.follow_all(css="li.next a", meta={"pyppeteer": self.pyppeteer})

    def parse_book(self, response):
        return {
            "url": response.url,
            "title": response.css("h1::text").get(),
            "price": response.css("p.price_color::text").re_first(r"(\d+.?\d*)"),
        }
