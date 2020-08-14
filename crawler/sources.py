import requests
import json
import copy
import lxml.html
import argparse
import logging
import tqdm

_url = 'https://www.msn.com/en-us/{cat}/{subcat}/{title}/{dtype}-{nid}'


def url(news_id, doc_type, category, subcategory, title):
    return _url.format(cat=category, subcat=subcategory, title=title, dtype=doc_type, nid=news_id)


def find_news_source_by_url(url):
    response = requests.get(url)

    if not 200 <= response.status_code <= 300:
        raise ValueError('recieved status code {}'.format(response.status_code))

    html = lxml.html.fromstring(response.content)

    # content_node = html.xpath('//div[@id="main" and div/@class="content" and div/a/@title and div/a/@href]')
    # ref_node = content_node[0].xpath('div/a')

    ref_node = html.xpath('//a[@href and @title]')

    href = ref_node[0].get('href')
    title = ref_node[0].get('title')

    return title, href


def main(in_path, out_path):
    logging.basicConfig(filename='sources.log', level=logging.INFO)

    with open(in_path, 'r') as f:
        dataset = json.load(f)

    extended_dataset = []

    total = 0
    fails = 0

    for entry in tqdm.tqdm(dataset):
        true_url = url(entry['news_id'], entry['doc_type'], entry['category'], entry['subcategory'], entry['title'])
        total += 1

        try:
            title, href = find_news_source_by_url(true_url)

        except Exception as e:
            logging.info('News_ID {} -- Error {}'.format(entry['news_id'], e))
            fails += 1
            continue

        extended_entry = copy.deepcopy(entry)
        extended_entry['source_name'] = title.replace('logo', '')
        extended_entry['source_url'] = href

        extended_dataset.append(extended_entry)

    with open(out_path, 'w') as file:
        json.dump(extended_dataset, file, indent=4)

    logging.info('TOTAL ITEMS PROCESSED {} // {} ITEMS FAILED'.format(total, fails))


_parser = argparse.ArgumentParser(description='')
_parser.add_argument('in_path', type=str, help='')
_parser.add_argument('out_path', type=str, help='')

if __name__ == '__main__':
    args = _parser.parse_args()
    main(args.in_path, args.out_path)
