import urllib.parse
from pathlib import Path

import scrapy
import scrapy.linkextractors
import scrapy.spiders

URLS_PATH = Path("./urls.txt").absolute()
OUTPUT_PATH = Path('./output/').absolute()
FILE_EXTS = {'wav', 'mp3', 'm4a'}


def url_domain(url) -> str:
    "Get URL domain"
    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit
    return urllib.parse.urlsplit(url).netloc


class BurischCrawlSpider(scrapy.spiders.CrawlSpider):
    name = "burisch"
    allowed_domains = set()

    rules = (
        scrapy.spiders.Rule(
            link_extractor=scrapy.linkextractors.LinkExtractor()
        ),
    )

    def start_requests(self):
        with URLS_PATH.open() as file:
            for line in file:
                url = line.strip()
                self.allowed_domains.add(url_domain(url))

                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
        # # Iterate over links
        # for query in response.css('a::attr(href)'):
        #     href = query.get()

        #     for ext in FILE_EXTS:
        #         if href.endswith(ext):
        #             print(href)

        #             # TODO pipeline

        #     yield response.follow(href, callback=self.parse)
