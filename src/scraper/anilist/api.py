import time

import requests
from pymongo import UpdateOne

from scraper.anilist.models import AniListModel
from scraper.anilist.types import AniListPages
from scraper.core.database import DBUtils
from scraper.utils.utils import get_config

HTTP_OK = 200


class AniListAPI:
    """A class for interacting with the AniList API."""

    entries_per_page = 50
    name = "anilist"

    def __init__(
        self,
        query_limit: int,
        page: AniListPages,
        max_pages: int,
    ) -> None:
        """Initialize the AniListAPI with a query limit and page type.

        Args:
            query_limit (int): The maximum number of items to scrape.
            page (AniListPages): The page type to scrape.
            max_pages (int): The maximum number of pages to scrape.
        """
        self.query_limit = query_limit
        self.page = page
        self.max_pages = max_pages

    def start(self) -> None:
        """Start the API request to fetch data from AniList."""
        for i in range(
            1, min((self.query_limit // self.entries_per_page) + 1, self.max_pages + 1)
        ):
            if i > 1:
                time.sleep(get_config("SCRAPER", "DOWNLOAD_DELAY"))
            self.parse(self.submit_query(i))

    def submit_query(self, page_num: int) -> list[dict]:
        """Submit a GraphQL query to the AniList API.

        Args:
            page_num (int): The page number to fetch.

        Returns:
            list[dict]: A list of media items from the API response.
        """
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": self.form_query(page_num)},
            timeout=10,
        )
        if response.status_code == HTTP_OK:
            return response.json()["data"]["Page"]["media"]
        msg = f"Query failed with status code {response.status_code}: {response.text}"
        raise Exception(msg)

    def form_query(self, page_num: int) -> str:
        """Formulate a GraphQL query string based on the selected page type.

        Args:
            page_num (int): The page number to fetch.

        Returns:
            str: The formatted GraphQL query string for the AniList API.
        """
        if self.page == "Top 100":
            filter_str = "SCORE_DESC"
        elif self.page == "Trending":
            filter_str = "TRENDING_DESC"
        return f"""
        query {{
            Page(page: {page_num}, perPage: {self.entries_per_page}) {{
                media(type: MANGA, sort: {filter_str}) {{
                title {{
                    english
                    romaji
                }}
                genres
                popularity
                favourites
                averageScore
                status
                description
                }}
            }}
        }}
        """

    def parse(self, response: list[dict]) -> None:
        """Parse the response from the AniList API and save its content."""
        self.save_to_coll(self.parse_response(response))

    def parse_response(self, response: list[dict]) -> list[AniListModel]:
        """Parse the response from the AniList API into AniListModel instances.

        Args:
            response (list[dict]): The response containing the API data.

        Returns:
            list[AniListModel]: A list of AniListModel instances with extracted
                media information.
        """
        ret = []
        for item in response:
            title = item["title"]["english"] or item["title"]["romaji"]
            genres = item["genres"]
            popularity = item["popularity"]
            favorites = item["favourites"]
            rating = item["averageScore"]
            status = item["status"]
            description = item["description"]
            ret.append(
                AniListModel(
                    title=title,
                    genres=genres,
                    popularity=popularity,
                    favorites=favorites,
                    rating=rating,
                    status=status,
                    description=description,
                )
            )
        return ret

    def save_to_coll(self, data: list[AniListModel]) -> None:
        """Save a list of AniListModel instances to the collection.

        Args:
            data (list[AniListModel]): The list of AniListModel instances to save.
        """
        coll = DBUtils.get_collection(self.name)
        ops = [
            UpdateOne(
                {"_id": item.title},
                {"$set": item.model_dump()},
                upsert=True,
            )
            for item in data
        ]
        coll.bulk_write(ops)
