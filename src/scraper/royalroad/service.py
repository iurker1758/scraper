from scraper.core.service import Fetcher
from scraper.royalroad.spider import RoyalRoadSpider
from scraper.royalroad.types import RoyalRoadPages


class RoyalRoadFetcher(Fetcher):
    """A class for fetching data from RoyalRoad."""

    def __init__(
        self,
        query_limit: int = 250,
        page: RoyalRoadPages = "Ongoing Fictions",
        max_pages: int = 1,
    ) -> None:
        """Initialize the RoyalRoadFetcher.

        Args:
            query_limit (int, optional): The minimum query limit per fetch.
                Defaults to 250.
            page (RoyalRoadPages, optional): The page type to scrape.
                Defaults to "Ongoing Fictions".
            max_pages (int, optional): The maximum number of pages to scrape.
                Defaults to 10.
        """
        super().__init__(query_limit=query_limit, max_pages=max_pages)
        self.page = page

    def fetch(self) -> None:
        """Fetch data from RoyalRoad."""
        self.process.crawl(
            RoyalRoadSpider,
            query_limit=self.query_limit,
            page=self.page,
            max_pages=self.max_pages,
        )
        self.process.start()
