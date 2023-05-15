from flask import Flask, request
from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)

connection = MySQL(app)

""" RECIBIR EL TXT """
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        # Realiza las operaciones que desees con el contenido del archivo
        # ...

        return 'Archivo recibido y procesado con éxito.'
    else:
        return 'Error: archivo no válido.'

""" FORMULARIO DE AYUDA """
@app.route('/formulario', methods=['POST'])
def handle_form():
    nombre = request.form.get('nombre')
    edad = request.form.get('edad')
    plataforma = request.form.get('plataforma')
    lugar_acontecimiento = request.form.get('lugarAcontecimiento')

    # Realiza las operaciones que desees con los datos recibidos del formulario
    # ...

    return 'Formulario recibido y procesado con éxito.'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()