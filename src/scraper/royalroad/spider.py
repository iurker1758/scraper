from collections.abc import AsyncIterator
from datetime import datetime
from pathlib import Path
from typing import Any

import scrapy
import scrapy.http
from pymongo import UpdateOne

from scraper.core.database import DBUtils
from scraper.royalroad.models import RoyalRoadModel
from scraper.royalroad.types import RoyalRoadPages
from scraper.utils.utils import get_data_directory


class RoyalRoadSpider(scrapy.Spider):
    """Spider for scraping quotes from the 'Royal Road' website."""

    entries_per_page = 20
    name = "royalroad"

    def __init__(
        self,
        query_limit: int,
        page: RoyalRoadPages,
        max_pages: int,
    ) -> None:
        """Initialize the RoyalRoadSpider with a query limit and page type.

        Args:
            query_limit (int): The maximum number of items to scrape.
            page (RoyalRoadPages): The page type to scrape.
            max_pages (int): The maximum number of pages to scrape.
        """
        super().__init__()
        self.query_limit = query_limit
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
            1, min((self.query_limit // self.entries_per_page) + 1, self.max_pages) + 1
        ):
            yield scrapy.Request(url=f"{base_url}{i}", callback=self.parse)

    def parse(self, response: scrapy.http.Response) -> None:
        """Parse the response from a Royal Road page and save its content.

        Args:
            response (scrapy.http.Response): The response containing the page content.
        """
        self.save_html(response)
        self.save_to_coll(self.parse_response(response))

    def save_html(self, response: scrapy.http.Response) -> None:
        """Save the HTML content of a response to a file.

        Args:
            response (scrapy.http.Response): The response containing the HTML content.
        """
        base_path = get_data_directory(self.name)
        page = response.url.split("?page=")[-1]
        file_path = base_path / self.page.replace(" ", "_").lower()
        file_path.mkdir(parents=True, exist_ok=True)
        file_name = f"{page}.html"
        Path(file_path / file_name).write_bytes(response.body)

    def parse_response(self, response: scrapy.http.Response) -> list[RoyalRoadModel]:
        """Parse the response from a Royal Road page and extract story information.

        Args:
            response (scrapy.http.Response): The response containing the page content.

        Returns:
            list[RoyalRoadModel]: A list of RoyalRoadModel instances with extracted
                story information.
        """
        ret = []
        for item in response.css("div.fiction-list-item.row"):
            title = item.css("h2.fiction-title a::text").get().strip()
            genres = item.css("span.tags a::text").getall()
            followers = int(
                item.css("i.fa-users + span::text").re_first(r"[\d,]+").replace(",", "")
            )
            rating = float(item.css("i.fa-star + span::attr(title)").get())
            pages = int(
                item.css("i.fa-book + span::text").re_first(r"[\d,]+").replace(",", "")
            )
            views = int(
                item.css("i.fa-eye + span::text").re_first(r"[\d,]+").replace(",", "")
            )
            chapters = int(
                item.css("i.fa-list + span::text").re_first(r"[\d,]+").replace(",", "")
            )
            last_updated = datetime.strptime(  # noqa: DTZ007
                item.css("i.fa-calendar + span time::text").get(), "%b %d, %Y"
            )
            description = " ".join(
                item.css("div[id^=description-] p::text").getall()
            ).strip()
            ret.append(
                RoyalRoadModel(
                    title=title,
                    genres=genres,
                    followers=followers,
                    rating=rating,
                    pages=pages,
                    view=views,
                    chapters=chapters,
                    last_updated=last_updated,
                    description=description,
                )
            )
        return ret

    def save_to_coll(self, data: list[RoyalRoadModel]) -> None:
        """Save a list of RoyalRoadModel instances to the collection.

        Args:
            data (list[RoyalRoadModel]): The list of RoyalRoadModel instances to save.
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
