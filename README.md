# scraper

A small collection of site-specific web scrapers built with Scrapy and
simple utilities for persisting page HTML and writing results into MongoDB.

This repository groups active scrapers under `src/scraper/` and contains a
`legacy_code/` folder with historical implementations that are kept for
reference.

Quick summary
- Source root: `src/scraper`
- Runtime config: `scraper/config.ini` (contains DATA_PATH, DATABASE URI,
	and SCRAPER settings such as DOWNLOAD_DELAY)

Architecture and conventions
- Fetcher -> Spider: each site has a `fetcher.py` that instantiates a
	Scrapy `CrawlerProcess` and starts a site-specific `spider.py`. Fetchers
	then update a `last_updated` collection in MongoDB.
- Models: Pydantic models live next to spiders (e.g. `royalroad/models.py`) and
	are used to validate and serialize scraped items before DB writes.
- DB access: use `src/scraper/core/database.py` -> `DBUtils.get_collection(name)`
	to obtain a `pymongo` collection. Many spiders use `self.name` as the
	collection name.

Legacy code and `novelupdates`
--------------------------------
The `legacy_code/novelupdates` implementation is intentionally kept under
`legacy_code/` because the NovelUpdates site actively blocks Scrapy-based
crawlers. The implementation is preserved for reference and research only.
