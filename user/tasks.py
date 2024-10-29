from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .scraper.scraper.spiders.yahoo_auction_spider import YahooAuctionSpider
from .scraper.scraper.spiders.merukari_spider import MeruKariSpider
from .scraper.scraper.spiders.merukari_spider import MeruKariSpider
from .scraper.scraper.spiders.merukari_spider import MericariSpider
import logging

logger = logging.getLogger(__name__)

@shared_task
def yahoo_auction_scrape_task(url):
    """Asynchronous task for Yahoo Auction scraping."""
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(YahooAuctionSpider, url=url)
        process.start()  # Blocks until scraping completes
    except Exception as e:
        logger.error(f"Yahoo Auction scraping failed: {e}")
        raise

@shared_task
def merukari_scrape_task(product_id):
    """Asynchronous task for MeruKari scraping."""
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(MeruKariSpider, product_id=product_id)
        process.start()
    except Exception as e:
        logger.error(f"MeruKari scraping failed: {e}")
        raise