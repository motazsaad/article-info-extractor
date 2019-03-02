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

def get_title(url):
    try:
        html_doc = requests.get(url)
        status = html_doc.status_code
        if status is 200:
            soup_doc = BeautifulSoup(html_doc.text, 'html.parser')
            title = soup_doc.title.text
        else:
            title = 'connection error: {} {}'.format(str(status), responses[status])
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
    
def get_text_boilerpipe(url):
    try:
        extractor = Extractor(extractor='ArticleExtractor', url=url)
        extracted_text = extractor.getText()
    except BaseException as error:
        extracted_text = 'error: {}'.format(error) 
        print('error: {}'.format(error))
    return extracted_text
    
    
def get_text_justext(url):
    alpha_det = AlphabetDetector()
    try:
        extracted_text = ''
        response = requests.get(url)
        contents = response.content
        status = response.status_code
        if status is 200:
            soup_doc = BeautifulSoup(response.text, 'html.parser')
            title = soup_doc.title.text
        else:
            title = 'connection error: {} {}'.format(str(status), responses[status])
            return title
        if 'ARABIC' in alpha_det.detect_alphabet(title):
            paragraphs = justext.justext(contents, justext.get_stoplist('Arabic'))
        else:
            paragraphs = justext.justext(contents, justext.get_stoplist('English'))
        for paragraph in paragraphs:
            # print(type(paragraph))
            if not paragraph.is_boilerplate:
                extracted_text += paragraph.text + '\n'
    except RequestException as error:
        extracted_text = 'error: {}'.format(error) 
        print('error: {}'.format(error))
    return extracted_text
    
    
def extract_newspaper3k(url):
    article = Article(url)
    article.download()
    article.parse()
    authors = article.authors
    date = article.publish_date 
    text = article.text
    title = article.title
    print ('newspaper3k title:', title)
    print ('newspaper3k authors:', authors)
    print ('newspaper3k date:', date)
    return  title, text
   
    
    
def extract_newspaper3k_v2(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article
    
    
def extract_news_please(url):
    article = NewsPlease.from_url(url)
    title = article.title 
    text = article.text
    print('news-please title:', title)
    return text 
    
def refine_Arabic_keywords(keywords):
    stopwords = open('stopwords.ar').read().splitlines()
    my_keywords = [key for key in keywords if key not in stopwords]
    return '\t'.join(my_keywords)
        