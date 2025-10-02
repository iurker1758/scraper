class Fetcher:
    """A superclass for fetching data."""

    def __init__(self, query_limit: int = 250, max_pages: int = 1) -> None:
        """Initialize the Fetcher.

        Args:
            query_limit (int, optional): The maximum query limit per fetch.
                Defaults to 250.
            max_pages (int, optional): The maximum number of pages to scrape.
                Defaults to 10.
        """
        self.query_limit = query_limit
        self.max_pages = max_pages

    def fetch(self) -> None:
        """Fetch data from the source.

        This method should be implemented by subclasses to define how data is fetched.
        """
        raise NotImplementedError("Subclasses must implement this method.")
