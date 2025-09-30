from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import scrapy
from requests import Response

from scraper.royalroad.types import RoyalRoadPages
from scraper.utils.utils import get_data_directory


class RoyalRoadSpider(scrapy.Spider):
    """Spider for scraping quotes from the 'Royal Road' website."""

    entries_per_page = 20
    name = "royalroad"

    def __init__(
        self, limit: int, page: RoyalRoadPages = "Ongoing Fictions", max_pages: int = 2
    ) -> None:
        """Initialize the RoyalRoadSpider with a limit and page type.

        Args:
            limit (int): The maximum number of items to scrape.
            page (RoyalRoadPages, optional): The page type to scrape.
                Defaults to "Ongoing Fictions".
            max_pages (int, optional): The maximum number of pages to scrape.
                Defaults to 10.
        """
        super().__init__()
        self.limit = limit
        self.page = page
        self.max_pages = max_pages

    async def start(self) -> AsyncIterator[Any]:
        """Asynchronously generate URLs to scrape based on the RoyalRoad page type.

        Yields:
            str: The URL for each page to be scraped.
        """
        if self.page == "Best Rated":
            base_url = "https://www.royalroad.com/fictions/best-rated?page="
        elif self.page == "Trending":
            base_url = "https://www.royalroad.com/fictions/trending?page="
        elif self.page == "Ongoing Fictions":
            base_url = "https://www.royalroad.com/fictions/active-popular?page="
        elif self.page == "Popular This Week":
            base_url = "https://www.royalroad.com/fictions/weekly-popular?page="

        for i in range(
            1, min((self.limit // self.entries_per_page) + 1, self.max_pages) + 1
        ):
            yield scrapy.Request(url=f"{base_url}{i}", callback=self.parse)

    def parse(self, response: Response) -> None:
        """Parse the response from a Royal Road page and save its HTML content.

        Args:
            response (Response): The HTTP response object containing the page content.
        """
        base_path = get_data_directory(self.name)
        page = response.url.split("?page=")[-1]
        file_path = base_path / self.page.replace(" ", "_").lower()
        file_path.mkdir(parents=True, exist_ok=True)
        file_name = f"{page}.html"
        Path(file_path / file_name).write_bytes(response.body)
        self.log(f"Saved file {file_path / file_name}")
