import articleDateExtractor
from date_extractor import extract_dates
from bs4 import BeautifulSoup
import requests
from boilerpipe.extract import Extractor
from requests.exceptions import RequestException
import datetime
    
def get_title(url):
    try:
        html_doc = requests.get(url)
        if html_doc.status_code is 200:
            soup_doc = BeautifulSoup(html_doc.text, 'html.parser')
            title = soup_doc.title.text
        else:
            title = 'connection error: ' + html_doc.status_code
    except RequestException as error:
        title = 'Request error: {}'.format(error) 
        print('Request error: {}'.format(error))
    except BaseException as error:
        title = 'error: {}'.format(error)
        print('error: {}'.format(error))
    return title
    
    
def get_date(url):
    try:
        article_date = articleDateExtractor.extractArticlePublishedDate(url)
        article_date = article_date.strftime('%Y-%m-%d')
    except BaseException as error:
        print('error: {}'.format(error))
        article_date = 'error: {}'.format(error) 
    return article_date
    
    
def get_dates(url):
    try:
        date_str = ''
        html_doc = requests.get(url).text
        text_doc = BeautifulSoup(html_doc, 'html.parser').text
        dates = extract_dates(text_doc)
        for d in dates:
            if isinstance(d, datetime.datetime):
                date_str += d.strftime('%Y-%m-%d') + '\n'
    except RequestException as error:
        date_str = 'Request error: {}'.format(error) 
        print('Request error: {}'.format(error))
    except BaseException as error:
        date_str = 'error: {}'.format(error) 
        print('error: {}'.format(error))
    return date_str
    
def get_text(url):
    try:
        extractor = Extractor(extractor='ArticleExtractor', url=url)
        extracted_text = extractor.getText()
    except BaseException as error:
        extracted_text = 'error: {}'.format(error) 
        print('error: {}'.format(error))
    return extracted_text
