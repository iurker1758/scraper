from scraper.anilist.types import AniListPages
from scraper.core.fetcher import Fetcher


class AniListFetcher(Fetcher):
    """A class for fetching data from AniList."""

    def __init__(self, query_limit: int = 250, page: AniListPages = "Top 100") -> None:
        """Initialize the AniListFetcher.

        Args:
            query_limit (int, optional): The minimum query limit per fetch.
                Defaults to 250.
            page (AniListPages, optional): The page type to scrape.
                Defaults to "Top 100".
        """
        super().__init__(query_limit=query_limit)
        self.page = page

    def fetch(self) -> None:
        """Fetch data from AniList."""
        raise NotImplementedError("Subclasses must implement this method.")
