from flask import Flask
from flask import request
import extract_util
from socket import gethostname


app = Flask(__name__)


@app.route('/')
def welcome():
    return '<h1>welcome :)</h1>'


@app.route('/extractor')
def extractor():
    url = request.args.get('url')
    title = extract_util.get_title(url)
    date = extract_util.get_date(url)
    text = extract_util.get_text(url)
    answer = '<h1>Extracted info</h1>'
    answer = answer + '\n<p><b>ULR: </b>' + url + '/<p>'
    answer = answer + '\n<p><b>title:</b> ' + title + '/<p>'
    answer = answer + '\n<p><b>date:</b>' + str(date) + '/<p>'
    answer = answer + '\n<p><b>text:</b>\n' + text + '/<p>'
    return answer

# sudo ufw enable
# sudo ufw allow 5000/tcp
# sudo ufw status verbose
# app.run(host='0.0.0.0' , port=5000)

if __name__ == '__main__':
	print(gethostname())
    # app.run(debug=True, host=gethostname(), port=5000)
	# app.run(debug=True, host='0.0.0.0', port=5000)
	app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))