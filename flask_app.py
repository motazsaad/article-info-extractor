from flask import Flask
from flask import request
import extract_util
from socket import gethostname
import os 

app = Flask(__name__)


@app.route('/')
def welcome():
    return '<h1>welcome :)</h1>'


@app.route('/extractor')
def extractor():
    url = request.args.get('url')
    url = url.strip()
    if not url:
        return '<h1>Aricle\'s info extractor</h1> <h2>error: No URL</h2>'
    title = extract_util.get_title(url)
    date = extract_util.get_date(url)
    text = extract_util.get_text(url)
    answer = '''
    <title> Aricle's info extractor </title>
    <h1>Aricle's info extractor</h1>
    <h2>Extracted info</h2>
    <hr>
    <p><b>ULR:</b> {} </p>
    <hr>
    <p><b>title:</b> {} </p>
    <hr>
    <p><b>date:</b> {} </p>
    <hr>
    <p><b>text:</b></p> <p>{}</p>
    <hr>
    '''.format(url, title, date, text)
    
    return answer

# sudo ufw enable
# sudo ufw allow 5000/tcp
# sudo ufw status verbose
# app.run(host='0.0.0.0' , port=5000)

if __name__ == '__main__':
	print(gethostname())
	#################################
	# for pythonanywhere
	if 'liveconsole' not in gethostname():
	    app.run()
    #################################
    # for c9.io 
	# app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
	#################################