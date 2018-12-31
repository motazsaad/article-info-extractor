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


if __name__ == '__main__':
    app.run(debug=True, host=gethostname())