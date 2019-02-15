from flask import Flask
from flask import request
import extract_util
from socket import gethostname
import os 
from alphabet_detector import AlphabetDetector
from flask import render_template


app = Flask(__name__)


@app.route('/')
def welcome():
    return '<h1>welcome :)</h1>'


@app.route('/extractor')
def extractor():
    alpha_det = AlphabetDetector()
    url = request.args.get('url')
    url = url.strip()
    title = extract_util.get_title(url)
    date = extract_util.get_date(url)
    text_boilerpipe = extract_util.get_text_boilerpipe(url)
    text_justext = extract_util.get_text_justext(url)
    text_boilerpipe = text_boilerpipe.split('\n')
    text_justext = text_justext.split('\n')
    if 'ARABIC' in alpha_det.detect_alphabet(title):
        text_dir = 'rtl'
    else:
        text_dir = 'ltr'
    return render_template('article_info.html', url=url, title=title, date=date, text_dir=text_dir, text_boilerpipe=text_boilerpipe, text_justext=text_justext)
    
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