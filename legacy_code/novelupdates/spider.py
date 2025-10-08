from collections.abc import AsyncIterator
from datetime import datetime
from pathlib import Path
from typing import Any

from pymongo import UpdateOne
from scrapy import Request, Spider
from scrapy.http import Response

from scraper.core.database import DBUtils
from scraper.novelupdates.models import NovelUpdatesModel
from scraper.novelupdates.types import NovelUpdatesPages
from scraper.utils.utils import get_data_directory


class NovelUpdatesSpider(Spider):
    """Spider for scraping quotes from the NovelUpdates website."""

    entries_per_page = 25
    name = "novelupdates"

    def __init__(
        self,
        query_limit: int,
        page: NovelUpdatesPages,
        max_pages: int,
    ) -> None:
        """Initialize the NovelUpdatesSpider with a query limit and page type.

        Args:
            query_limit (int): The maximum number of items to scrape.
            page (NovelUpdatesPages): The page type to scrape.
            max_pages (int): The maximum number of pages to scrape.
        """
        super().__init__()
        self.query_limit = query_limit
        self.page = page
        self.max_pages = max_pages

    async def start(self) -> AsyncIterator[Any]:
        """Asynchronously generate URLs to scrape based on the NovelUpdates page type.

        Yields:
            str: The URL for each page to be scraped.
        """
        if self.page == "Activity (Week)":
            base_url = "https://www.novelupdates.com/series-ranking/?rank=week&ge=324,1692,560&rl=0&pg="
        elif self.page == "Popular (Month)":
            base_url = "https://www.novelupdates.com/series-ranking/?rank=popmonth&ge=324,1692,560&rl=0&pg="

        for i in range(
            1, min((self.query_limit // self.entries_per_page) + 1, self.max_pages) + 1
        ):
            yield Request(url=f"{base_url}{i}", callback=self.parse)

    def parse(self, response: Response) -> None:
        """Parse the response from a Royal Road page and save its content.

        Args:
            response (Response): The response containing the page content.
        """
        self.save_html(response)
        self.save_to_coll(self.parse_response(response))

    def save_html(self, response: Response) -> None:
        """Save the HTML content of a response to a file.

        Args:
            response (Response): The response containing the HTML content.
        """
        base_path = get_data_directory(self.name)
        page = response.url.split("&pg=")[-1]
        file_path = base_path / self.page.replace(" ", "_").lower()
        file_path.mkdir(parents=True, exist_ok=True)
        file_name = f"{page}.html"
        Path(file_path / file_name).write_bytes(response.body)

    def parse_response(self, response: Response) -> list[NovelUpdatesModel]:
        """Parse the response from a Royal Road page and extract story information.

        Args:
            response (Response): The response containing the page content.

        Returns:
            list[NovelUpdatesModel]: A list of NovelUpdatesModel with extracted
                story information.
        """
        ret = []
        for item in response.css("div.search_main_box_nu"):
            rating = float(
                item.css("div.search_ratings::text").re_first(r"\(([\d.]+)\)")
            )
            title = " ".join(item.css("div.search_title a::text").get().split())
            stats = item.css("div.search_stats span.ss_desk::text").getall()
            stats = [stat.strip() for stat in stats if stat.strip()]
            chapters = int(stats[0].split()[0])
            if chapters == 0:
                continue
            update_frequency = float(stats[1].split()[1])
            readers = int(stats[2].split()[0])
            reviews = int(stats[3].split()[0])
            last_updated = datetime.strptime(stats[4], "%m-%d-%Y")  # noqa: DTZ007
            genres = item.css("div.search_genre a::text").getall()
            if "Completed" in genres:
                genres.remove("Completed")
            description = item.css("div.search_body_nu::text").getall()
            description = [" ".join(desc.split()) for desc in description]
            first = " ".join(description).strip()
            hidden_description = item.css(
                "div.search_body_nu span.testhide *::text"
            ).getall()
            hidden_description = [" ".join(desc.split()) for desc in hidden_description]
            second = " ".join(hidden_description[:-1]).strip()
            ret.append(
                NovelUpdatesModel(
                    title=title,
                    genres=genres,
                    readers=readers,
                    reviews=reviews,
                    rating=rating,
                    chapters=chapters,
                    last_updated=last_updated,
                    update_frequency=update_frequency,
                    description=first + second,
                )
            )
        return ret

    def save_to_coll(self, data: list[NovelUpdatesModel]) -> None:
        """Save a list of NovelUpdatesModel instances to the collection.

        Args:
            data (list[NovelUpdatesModel]): The list of NovelUpdatesModel to save.
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
