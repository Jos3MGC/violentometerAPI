from flask import Flask, request
import requests
from werkzeug.utils import secure_filename
import io
from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)

connection = MySQL(app)

@app.route('/send-file', methods=['POST'])
def send_file():
    url = 'https://colab.research.google.com/drive/1OXGILvSZSyabRr_KS6_6dLxdwqKzn2Gs?usp=sharing' # Replace with your own Colab URL
    file = request.files['file']
    if file.filename.endswith('.txt'):
        filename = secure_filename(file.filename)
        file_bytes = io.BytesIO(file.read())
        files = {'file': (filename, file_bytes)}
        response = requests.post(url, files=files)
        return response.text
    else:
        return 'The attached file is not a .txt file'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()