from scrapy.crawler import CrawlerProcess

from scraper.utils.utils import get_config


class Fetcher:
    """A superclass for fetching data."""

    def __init__(self, query_limit: int = 250, max_pages: int = 1) -> None:
        """Initialize the Fetcher.

        Args:
            query_limit (int, optional): The minimum query limit per fetch.
                Defaults to 250.
            max_pages (int, optional): The maximum number of pages to scrape.
                Defaults to 10.
        """
        self.query_limit = query_limit
        self.max_pages = max_pages
        self.process = CrawlerProcess(
            settings={
                "ROBOTSTXT_OBEY": True,
                "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
                "DOWNLOAD_DELAY": get_config("SCRAPER", "DOWNLOAD_DELAY"),
                "LOG_LEVEL": "ERROR",
            }
        )

    def fetch(self) -> None:
        """Fetch data from the source.

        This method should be implemented by subclasses to define how data is fetched.
        """
        raise NotImplementedError("Subclasses must implement this method.")
