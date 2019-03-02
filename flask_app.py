from flask import Flask
from flask import request
import extract_util
from socket import gethostname
import os 
from alphabet_detector import AlphabetDetector
from flask import flash
from flask import render_template
from flask import redirect
from forms import * 


# App config.
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)




@app.route('/')
@app.route('/index')
def welcome():
    return render_template('home.html')


@app.route('/myform', methods=['GET', 'POST'])
def myform():
    form = URLForm()
    if form.validate_on_submit():
        print('Requested URL:  {}'.format(form.url.data))
        flash('Requested URL:  {}'.format(form.url.data))
    return render_template('extract.html', title='Extracted info', form=form)

@app.route('/extractor')
def extractor():
    alpha_det = AlphabetDetector()
    url = request.args.get('url')
    if not url:
        return render_template('no_url.html')
    url = url.strip()
    # title = extract_util.get_title(url)
    title, newspaper3k_text = extract_util.extract_newspaper3k(url)
    date = extract_util.get_date(url)
    text_boilerpipe = extract_util.get_text_boilerpipe(url)
    text_justext = extract_util.get_text_justext(url)
    news_please_text = extract_util.extract_news_please(url)

    text_boilerpipe = text_boilerpipe.split('\n')
    text_justext = text_justext.split('\n')
    newspaper3k_text = newspaper3k_text.split('\n')
    news_please_text = news_please_text.split('\n')
    
    if 'ARABIC' in alpha_det.detect_alphabet(title):
        text_dir = 'rtl'
    else:
        text_dir = 'ltr'
    return render_template('article_info.html', url=url, title=title, date=date, text_dir=text_dir, text_boilerpipe=text_boilerpipe, text_justext=text_justext, newspaper3k_text=newspaper3k_text, news_please_text=news_please_text)

# newspaper3k
@app.route('/newspaper3k')
def newspaper3k_extractor():
    alpha_det = AlphabetDetector()
    url = request.args.get('url')
    if not url:
        return '<h1> NO URL passed </h1>'
    url = url.strip()
    article = extract_util.extract_newspaper3k_v2(url)
    title = article.title
    if 'ARABIC' in alpha_det.detect_alphabet(title):
        text_dir = 'rtl'
        lang = 'ar'
    else:
        text_dir = 'ltr'
        lang = 'en'
    # date = article.publish_date 
    date = extract_util.get_date(url)
    newspaper3k_text = article.text
    title = article.title
    keywords = article.keywords
    if lang == 'ar':
        keywords = extract_util.refine_Arabic_keywords(keywords)
    else:
        keywords = '\t'.join(keywords)
    images = article.images
    newspaper3k_text = newspaper3k_text.split('\n')
    
    return render_template('newspaper3k.html', url=url, title=title, date=date, text_dir=text_dir, newspaper3k_text=newspaper3k_text, keywords=keywords, images=images)
    
    
    
    
# sudo ufw enable
# sudo ufw allow 5000/tcp
# sudo ufw status verbose
# app.run(host='0.0.0.0' , port=5000)

if __name__ == '__main__':
	print(gethostname())
	#################################
	# for pythonanywhere
    # if 'liveconsole' not in gethostname():
    # app.run()
    #################################
    # for c9.io 
	app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
	#################################