from datetime import UTC, datetime

from scraper.anilist.api import AniListAPI
from scraper.anilist.types import AniListPages
from scraper.core.database import DBUtils
from scraper.core.fetcher import Fetcher


class AniListFetcher(Fetcher):
    """A class for fetching data from AniList."""

    def __init__(
        self, query_limit: int = 250, page: AniListPages = "Top 100", max_pages: int = 1
    ) -> None:
        """Initialize the AniListFetcher.

        Args:
            query_limit (int, optional): The maximum query limit per fetch.
                Defaults to 250.
            page (AniListPages, optional): The page type to scrape.
                Defaults to "Top 100".
            max_pages (int, optional): The maximum number of pages to scrape.
                Defaults to 1.
        """
        super().__init__(query_limit=query_limit, max_pages=max_pages)
        self.page = page

    def fetch(self) -> None:
        """Fetch data from AniList."""
        AniListAPI(
            query_limit=self.query_limit,
            page=self.page,
            max_pages=self.max_pages,
        ).start()

        coll = DBUtils.get_collection("last_updated")
        coll.update_one(
            {"_id": "anilist"},
            {"$set": {self.page: datetime.now(UTC)}},
            upsert=True,
        )
