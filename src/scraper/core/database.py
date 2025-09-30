from pymongo import MongoClient
from pymongo.collection import Collection

from scraper.utils.utils import get_config


class DBUtils:
    """Utility class for interacting with the MongoDB database."""

    @staticmethod
    def get_collection(name: str) -> Collection:
        """Get a MongoDB collection by name.

        Args:
            name (str): The name of the collection.

        Returns:
            Collection: The MongoDB collection object.
        """
        client = MongoClient(get_config("DATABASE", "URI"))
        db = client.get_database("scraper")
        return db[name]
