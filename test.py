import articleDateExtractor
from date_extractor import extract_dates
from bs4 import BeautifulSoup
import requests


urls = [line.strip() for line in open('urls.txt')]

for url in urls:
    try:
        print(articleDateExtractor.extractArticlePublishedDate(url))
    except BaseException as error:
        print('error: {}'.format(error))




# for url in urls:
#     html_doc = requests.get(url).text
#     text_doc = BeautifulSoup(html_doc, 'html.parser').text
#     print(extract_dates(text_doc))



