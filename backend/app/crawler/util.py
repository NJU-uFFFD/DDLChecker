from crawler.crawlers.TeachingSquareCrawler import TeachingSquareCrawler, TEACHING_SQUARE_CRAWLER_UUID


def list_crawlers():
    return [
        {"name": "教学立方", "uuid": TEACHING_SQUARE_CRAWLER_UUID, "obj": TeachingSquareCrawler}
    ]
