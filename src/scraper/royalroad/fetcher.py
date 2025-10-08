from datetime import UTC, datetime

from scrapy.crawler import CrawlerProcess

from scraper.core.database import DBUtils
from scraper.core.fetcher import Fetcher
from scraper.royalroad.spider import RoyalRoadSpider
from scraper.royalroad.types import RoyalRoadPages
from scraper.utils.utils import get_config


class RoyalRoadFetcher(Fetcher):
    """A class for fetching data from RoyalRoad."""

    def __init__(
        self,
        query_limit: int = 250,
        page: RoyalRoadPages = "Ongoing Fictions",
        max_pages: int = 10,
    ) -> None:
        """Initialize the RoyalRoadFetcher.

        Args:
            query_limit (int, optional): The maximum query limit per fetch.
                Defaults to 250.
            page (RoyalRoadPages, optional): The page type to scrape.
                Defaults to "Ongoing Fictions".
            max_pages (int, optional): The maximum number of pages to scrape.
                Defaults to 10.
        """
        super().__init__(query_limit=query_limit, max_pages=max_pages)
        self.page = page
        self.process = CrawlerProcess(
            settings={
                "ROBOTSTXT_OBEY": True,
                "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
                "DOWNLOAD_DELAY": get_config("SCRAPER", "DOWNLOAD_DELAY"),
                "LOG_LEVEL": "ERROR",
            }
        )

    def fetch(self) -> None:
        """Fetch data from RoyalRoad."""
        self.process.crawl(
            RoyalRoadSpider,
            query_limit=self.query_limit,
            page=self.page,
            max_pages=self.max_pages,
        )
        self.process.start()

        coll = DBUtils.get_collection("last_updated")
        coll.update_one(
            {"_id": "royalroad"},
            {"$set": {self.page: datetime.now(UTC)}},
            upsert=True,
        )
