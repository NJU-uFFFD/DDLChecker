from crawler.crawlers.TeachingSquareCrawler import TeachingSquareCrawler, TEACHING_SQUARE_CRAWLER_UUID

from crawler.crawlers.NjuSpocCrawler import NJU_SPOC_UUID, NjuSpocCrawler


def list_crawlers():
    return [
        {"name": "教学立方", "uuid": TEACHING_SQUARE_CRAWLER_UUID, "obj": TeachingSquareCrawler, "check": True},
        {"name": "南大SPOC", "uuid": NJU_SPOC_UUID, "obj": NjuSpocCrawler, "check": False}
    ]
