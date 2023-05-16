from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

from config import config

app = Flask(__name__)
mysql = MySQL(app)

""" RECIBIR EL TXT """


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file and file.filename.endswith(".txt"):
        content = file.read().decode("utf-8")
        # Realiza las operaciones que desees con el contenido del archivo
        # ...

        return "Archivo recibido y procesado con éxito."
    else:
        return "Error: archivo no válido."


""" FORMULARIO DE AYUDA """


@app.route("/formulario", methods=["POST"])
def handle_form():
    names = request.form.get("names")
    surnames = request.form.get("surnames")
    eventZone = request.form.get("eventZone")
    email = request.form.get("email")
    phone = request.form.get("phone")
    idPlatform = request.form.get("idPlatform")
    age = request.form.get("age")

     # Validar campos numéricos
    if age:
        age = int(age)
    else:
        age = None
    
    if idPlatform:
        idPlatform = int(idPlatform)
    else:
        idPlatform = None

    try:
        # Guardar los datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO formularioayuda (names, surnames, eventZone, email, phone, idPlatform, age) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (names, surnames, eventZone, email, phone, idPlatform, age))
        mysql.connection.commit()
        cur.close()
        # Formulario almacenado exitosamente
        return jsonify({'code': 1, 'message': '¡Exito!, denuncia subida correctamente.'}), 200
    except Exception as e:
        # Error al almacenar el formulario
        return jsonify({'code': 0, 'message': '¡Ups!, hubo un error al subir la denuncia.', 'error': str(e)}), 500

""" EMIAL """

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Servidor de correo saliente (SMTP)
app.config['MAIL_PORT'] = 465  # Puerto del servidor de correo
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'violentometrounam@gmail.com'  # Tu dirección de correo
app.config['MAIL_PASSWORD'] = 'kkhyarylobcqodaj'  # Tu contraseña de correo

mail = Mail(app)

""" def enviar_correo(destinatario, asunto, cuerpo):
    msg = Message(asunto, sender=app.config['MAIL_USERNAME'], recipients=[destinatario])
    msg.body = cuerpo

    # Envío del correo
    with app.app_context():
        mail.send(msg) """

@app.route('/enviar-correo', methods=['POST'])
def enviar_correo_handler():
    destinatario = request.form.get('destinatario')
    asunto = request.form.get('asunto')
    
     # Renderizar la plantilla de correo con Jinja2
    cuerpo = render_template('correo.html', nombre='John Doe', mensaje='Hola, este es un ejemplo de correo.')

    # Enviar el correo electrónico
    msg = Message(asunto, sender='tu_correo@example.com', recipients=[destinatario])
    msg.body = cuerpo  # No es necesario si se utiliza el método html del mensaje
    msg.html = cuerpo  # Establecer el contenido HTML del mensaje

    try:
        mail.send(msg)
        return jsonify({'status': 1, 'message': 'Correo de confirmacion enviado correctamente.'}), 200
    except Exception as e:
        return jsonify({'status': 0, 'message': 'Error al enviar el correo: ' + str(e)}), 400

if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run()
