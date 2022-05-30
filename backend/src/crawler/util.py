from crawler.crawlers.TeachingSquareCrawler import TeachingSquareCrawler, TEACHING_SQUARE_CRAWLER_UUID

from crawler.crawlers.NjuSpocCrawler import NJU_SPOC_UUID, NjuSpocCrawler
from crawler.crawlers.iCourse163Crawler import ICOURSE163_UUID, iCourse163Crawler


def list_crawlers():
    return [
        {"name": "教学立方", "uuid": TEACHING_SQUARE_CRAWLER_UUID, "obj": TeachingSquareCrawler, "check": True},
        {"name": "南大SPOC", "uuid": NJU_SPOC_UUID, "obj": NjuSpocCrawler, "check": False},
        {"name": "中国大学MOOC", "uuid": ICOURSE163_UUID, "obj": iCourse163Crawler, "check": False}
    ]
