import articleDateExtractor
from date_extractor import extract_dates
from bs4 import BeautifulSoup
import requests
from boilerpipe.extract import Extractor
from requests.exceptions import RequestException

    
def get_title(url):
    try:
        html_doc = requests.get(url).text
        soup_doc = BeautifulSoup(html_doc, 'html.parser')
        title = soup_doc.title.text
    except RequestException as error:
        title = None 
        print('error: {}'.format(error))
    except BaseException as error:
        title = None
        print('error: {}'.format(error))
    return title
    
    
def get_date(url):
    try:
        article_date = articleDateExtractor.extractArticlePublishedDate(url)
    except BaseException as error:
        print('error: {}'.format(error))
        article_date = None 
    return article_date
    
def get_dates(url):
    try:
        html_doc = requests.get(url).text
        text_doc = BeautifulSoup(html_doc, 'html.parser').text
        dates = extract_dates(text_doc)
    except RequestException as error:
        dates = None 
        print('error: {}'.format(error))
    except BaseException as error:
        dates = None 
        print('error: {}'.format(error))
    return dates
    
def get_text(url):
    try:
        extractor = Extractor(extractor='ArticleExtractor', url=url)
        extracted_text = extractor.getText()
    except BaseException as error:
        extracted_text = None 
        print('error: {}'.format(error))
    return extracted_text
