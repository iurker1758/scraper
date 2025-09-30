from scrapy.crawler import CrawlerProcess

from scraper.core.service import Fetcher
from scraper.royalroad.spider import RoyalRoadSpider


class RoyalRoadFetcher(Fetcher):
    """A class for fetching data from RoyalRoad."""

    def __init__(self, query_limit: int = 250) -> None:
        """Initialize the RoyalRoadFetcher.

        Args:
            query_limit (int, optional): The minimum query limit per fetch.
                Defaults to 250.
        """
        super().__init__(query_limit=query_limit)

    def fetch(self) -> None:
        """Fetch data from RoyalRoad."""
        process = CrawlerProcess(
            settings={
                "ROBOTSTXT_OBEY": True,
                "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
                "DOWNLOAD_DELAY": 5,
                "LOG_LEVEL": "ERROR",
            }
        )
        process.crawl(RoyalRoadSpider, limit=self.query_limit)
        process.start()
