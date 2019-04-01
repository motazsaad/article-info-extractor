from flask import Flask
from flask import request
import extract_util
from socket import gethostname
import os 
from alphabet_detector import AlphabetDetector
from flask import render_template
from collections import OrderedDict



app = Flask(__name__)


@app.route('/')
@app.route('/index')
def welcome():
    urls = open('urls.txt').read().split('\n')
    return render_template('home.html', urls=urls)


@app.route('/extractor')
def extractor():
    alpha_det = AlphabetDetector()
    url = request.args.get('url')
    if not url:
        return render_template('no_url.html')
    url = url.strip()
    # title = extract_util.get_title(url)
    title, newspaper3k_text = extract_util.extract_newspaper3k(url)
    
    if 'ARABIC' in alpha_det.detect_alphabet(title):
        text_dir = 'rtl'
        lang = 'Arabic'
    else:
        text_dir = 'ltr'
        lang = 'English'
    
    date = extract_util.get_date(url)
    text_boilerpipe = extract_util.get_text_boilerpipe(url)
    text_justext = extract_util.get_text_justext(url, lang)
    news_please_text = extract_util.extract_news_please(url)
    # _, bs4_text = extract_util.get_title_text_BS4(url)
    text_pextract = extract_util.get_pextract(url)
    
    texts = OrderedDict()
    text_boilerpipe = text_boilerpipe.split('\n')
    texts['Boilerpipe'] = text_boilerpipe
    text_justext = text_justext.split('\n')
    texts['Justext'] = text_justext
    newspaper3k_text = newspaper3k_text.split('\n')
    texts['Newspaper3k'] = newspaper3k_text
    news_please_text = news_please_text.split('\n')
    texts['NewsPlease'] = news_please_text
    # bs4_text = bs4_text.split('\n')
    # texts['BeautifulSoup'] = bs4_text
    text_pextract = text_pextract.split('\n')
    texts['pextract'] = text_pextract
    
    
    
    return render_template('article_info.html', url=url, title=title, date=date, text_dir=text_dir, texts=texts)
    


if __name__ == '__main__':
	print(gethostname())
	#################################
	# for pythonanywhere
	# if 'liveconsole' not in gethostname():
	app.run()
	#################################
	# for c9.io 
	# app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
	#################################
	
	
	
# sudo ufw enable
# sudo ufw allow 5000/tcp
# sudo ufw status verbose
# app.run(host='0.0.0.0' , port=5000)
