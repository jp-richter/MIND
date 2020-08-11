import argparse

from bs4 import BeautifulSoup
from selenium import webdriver


_url = 'https://www.msn.com/en-us/{cat}/{subcat}/{title}/{dtype}-{nid}'

_options = webdriver.firefox.options.Options()
_options.add_argument("--headless")
_browser = webdriver.Firefox(options=_options)


def url(news_id, doc_type, category, subcategory, title):
    return _url.format(cat=category, subcat=subcategory, title=title, dtype=doc_type, nid=news_id)


def find_news_source_by_url(url):
    _browser.get(url)

    soup = BeautifulSoup(_browser.page_source, 'lxml')
    referer_node = soup.find('span', {'class': 'partnerlogo-img'})
    referer_link = referer_node.find('a', recursive=False)

    return referer_link.get('title'), referer_link.get('href')


def main(tsv_path):
    pass


_parser = argparse.ArgumentParser(description='')
_parser.add_argument('tsv_path', type=str, help='')

if __name__ == '__main__':
    args = _parser.parse_args()
    main(args.tsv_path)
