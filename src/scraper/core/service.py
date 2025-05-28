class Fetcher:
    """A superclass for fetching data."""

    def __init__(self, query_limit: int = 250) -> None:
        """Initialize the Fetcher.

        Args:
            query_limit (int, optional): The minimum query limit per fetch.
                Defaults to 250.
        """
        self.query_limit = query_limit

    def fetch(self) -> None:
        """Fetch data from the source.

        This method should be implemented by subclasses to define how data is fetched.
        """
        raise NotImplementedError("Subclasses must implement this method.")
