from scraper.core.service import Fetcher


class NovelUpdatesFetcher(Fetcher):
    """A class for fetching data from NovelUpdates."""

    def __init__(self, query_limit: int = 250) -> None:
        """Initialize the NovelUpdatesFetcher.

        Args:
            query_limit (int, optional): The minimum query limit per fetch.
                Defaults to 250.
        """
        super().__init__(query_limit=query_limit)

    def fetch(self) -> None:
        """Fetch data from NovelUpdates."""
        raise NotImplementedError("Subclasses must implement this method.")
