import articleDateExtractor
from date_extractor import extract_dates
from bs4 import BeautifulSoup
import requests
from boilerpipe.extract import Extractor
from requests.exceptions import RequestException
import datetime
from http.client import responses
import justext
from alphabet_detector import AlphabetDetector
from newspaper import Article
from newspaper import fulltext
from newsplease import NewsPlease
import pextract as pe
from urllib.parse import urljoin


def get_title_text_BS4(url):
    try:
        html_doc = requests.get(url)
        status = html_doc.status_code
        if status is 200:
            soup_doc = BeautifulSoup(html_doc.text, 'html.parser')
            title = soup_doc.title.text
            text = soup_doc.get_text()
            return title, text 
        else:
            title = 'connection error: {} {}'.format(str(status), responses[status])
            text = 'connection error: {} {}'.format(str(status), responses[status])
            return title, text 
    except RequestException as error:
        message = 'Request error: {}'.format(error) 
        message, message 
    except BaseException as error:
        message = 'Request error: {}'.format(error) 
        return message, message 
    

def get_pextract(url):
    try:
        response = requests.get(url)
        status = response.status_code
        if status is 200:
            soup = BeautifulSoup(response.content, 'lxml')
            for img in soup.findAll('img'):
            	img['src'] = urljoin(url, img['src'])
            html, pval = pe.extract(soup, text_only = False, remove_img = False)
            text, pval = pe.extract(soup)
            return text
        else:
            message = 'connection error: {} {}'.format(str(status), responses[status])
            return message 
    except RequestException as error:
        message = 'Request error: {}'.format(error) 
        message
    except BaseException as error:
        message = 'Request error: {}'.format(error) 
        return message
    

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
    
def get_text_boilerpipe(url):
    try:
        extractor = Extractor(extractor='ArticleExtractor', url=url)
        extracted_text = extractor.getText()
    except BaseException as error:
        extracted_text = 'error: {}'.format(error) 
        print('error: {}'.format(error))
    return extracted_text
    
    
def get_text_justext(url, lang):
    try:
        extracted_text = ''
        response = requests.get(url)
        contents = response.content
        status = response.status_code
        if status == 200:
            paragraphs = justext.justext(contents, justext.get_stoplist(lang))
            for paragraph in paragraphs:
                # print(type(paragraph))
                if not paragraph.is_boilerplate:
                    extracted_text += paragraph.text + '\n'
        else:
            return 'connection error: {} {}'.format(str(status), responses[status])
    except RequestException as error:
        extracted_text = 'error: {}'.format(error) 
        print('error: {}'.format(error))
    return extracted_text
    
    
def extract_newspaper3k(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        authors = article.authors
        date = article.publish_date 
        text = article.text
        title = article.title
        return  title, text
    except BaseException as error:
        message = 'error: {}'.format(error)
        return message, message 
    
def extract_newspaper3k_v2(url):
    try: 
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        return article
    except BaseException as error:
        return 'error: {}'.format(error)
    
    
def extract_news_please(url):
    try:
        article = NewsPlease.from_url(url)
        title = article.title 
        text = article.text
        # print('news-please title:', title)
        return text 
    except BaseException as error: 
        return 'error: {}'.format(error)
    
def refine_Arabic_keywords(keywords):
    stopwords = open('stopwords.ar').read().splitlines()
    my_keywords = [key for key in keywords if key not in stopwords]
    return '\t'.join(my_keywords)