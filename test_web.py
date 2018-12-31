from flask import Flask
from flask import request
import extract_util

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
    answer = answer + '\n<b>ULR: </b>' + url
    answer = answer + '\n<b>title:</b> ' + title
    answer = answer + '\n<b>date:</b>' + date
    answer = answer + '\n<b>text:</b>\n' + text
    return answer


if __name__ == '__main__':
    app.run(debug=True)