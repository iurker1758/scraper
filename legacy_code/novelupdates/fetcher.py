from datetime import UTC, datetime

from scrapy.crawler import CrawlerProcess

from scraper.core.database import DBUtils
from scraper.core.fetcher import Fetcher
from scraper.novelupdates.spider import NovelUpdatesSpider
from scraper.novelupdates.types import NovelUpdatesPages
from scraper.utils.utils import get_config


class NovelUpdatesFetcher(Fetcher):
    """A class for fetching data from NovelUpdates."""

    def __init__(
        self,
        query_limit: int = 250,
        page: NovelUpdatesPages = "Activity (Week)",
        max_pages: int = 1,
    ) -> None:
        """Initialize the NovelUpdatesFetcher.

        Args:
            query_limit (int, optional): The maximum query limit per fetch.
                Defaults to 250.
            page (NovelUpdatesPages, optional): The page type to scrape.
                Defaults to "Activity (Week)".
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
                "LOG_LEVEL": "INFO",
            }
        )

    def fetch(self) -> None:
        """Fetch data from NovelUpdates."""
        self.process.crawl(
            NovelUpdatesSpider,
            query_limit=self.query_limit,
            page=self.page,
            max_pages=self.max_pages,
        )
        self.process.start()

        coll = DBUtils.get_collection("last_updated")
        coll.update_one(
            {"_id": "novelupdates"},
            {"$set": {self.page: datetime.now(UTC)}},
            upsert=True,
        )
