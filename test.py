import articleDateExtractor
from date_extractor import extract_dates
from bs4 import BeautifulSoup
import requests
from boilerpipe.extract import Extractor
import extract_util

urls = [line.strip() for line in open('urls.txt')]

for url in urls:
    print('url', url)
    print('title:', extract_util.get_title(url))
    print('date:', extract_util.get_date(url))
    print('text:', extract_util.get_text(url))
    print('---------------------------------')
    input()
    