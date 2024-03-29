import json
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

URL = "https://velog.io/@"
ARTICLE_SELECTOR = '//*[@id="root"]/div[2]/div[3]/div[4]/div[3]/div/div'


class Crawler:
    def __init__(self):
        pass

    def get_page(self, url: str):
        return requests.get(url)

    def parse(self, page: requests.Response):
        return bs(page.text, "html.parser")


htmlparser = etree.HTMLParser()


class Article:
    href: str
    headline: str
    context: str
    date: str
    tags: list[str]

    def to_dict(self):
        data = {}
        data.update(
            href=str(self.href),
            headline=str(self.headline),
            context=str(self.context),
            date=str(self.date),
            tags=str(self.tags),
        )
        return data

    def __init__(self, elem: etree._Element):
        head: list[etree._Element] = elem.xpath("a[2]")
        if not head:
            head = elem.xpath("a[1]")
        date = elem.xpath("div[2]/span")[0].text
        context = elem.xpath("p")[0].text
        self.href = head[0].attrib.get("href")
        self.headline = head[0].xpath("h2")[0].text
        self.context = context
        self.date = date
        self.tags = self.get_tags(elem)

    def get_tags(self, elem: etree._Element):
        tag_str: list[str] = []
        tags = elem.xpath("div[1]")
        for _tags in tags:
            for tag in _tags:
                tag_str.append(tag.text)
        return tag_str

    @staticmethod
    def list_to_dict(data: list["Article"]):
        return list(map(lambda x: x.to_dict(), data))


def get_articles(username: str):
    articles: list[Article] = []
    crawler = Crawler()
    req = crawler.get_page(URL + username)
    parsed = crawler.parse(req)
    dom = etree.HTML(str(parsed), htmlparser)
    elems: list[etree._Element] = dom.xpath(ARTICLE_SELECTOR)
    for elem in elems:
        articles.append(Article(elem))
    return articles


def to_json(data):
    with open(
        "articles.json",
        "w+",
        encoding="utf-8",
    ) as file:
        print(data)
        file.write(json.dumps(data, indent=4, ensure_ascii=False))
