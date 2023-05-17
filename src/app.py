from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

from config import config

import pickle
import stanza
import analisis.TxtToPd as txttopd
import pandas as pd
import json

# stanza.download("es")
# nlp = stanza.Pipeline("es")

app = Flask(__name__)
mysql = MySQL(app)

""" RECIBIR EL TXT """


@app.route("/upload", methods=["POST"])
def upload_file():
    resp = dict()
    resp["status"] = 0
    try:
        file = request.files["file"]
        if file and file.filename.endswith(".txt"): 
            content = file.read().decode("utf-8")
            # Realiza las operaciones que desees con el contenido del archivo
            # ...
            # para activar cuando se tenga el modelo que haga las predicciones
            # df = txttopd.panditas_android(content,nlp)
            import random ##prueba todas as lineas de prueba se van a quitar cuando el modelo haga la prediccion
            numbers = [random.uniform(0, 1) for _ in range(10)]##prueba

            # Create a DataFrame with the numbers
            df = pd.DataFrame({'num': numbers})##prueba
            
            # Calculate the mean of the 'num' column in the DataFrame
            indice_violencia = df['num'].mean()##prueba
            
            # Create a dictionary with the result
            resp["indiceViolencia"]= indice_violencia
            
            
            resp["status"] = 1
            # Convert the dictionary to a JSON string
            rel = jsonify(resp)
            # Return the JSON response with the appropriate content type
            return rel

            return str(df["mensaje"]) #"Archivo recibido y procesado con éxito." 
        else:
            return "Error: archivo no válido." + rel
    except:
        return jsonify(resp)


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

    print(names)

     # Validar campos numéricos
    if age:
        age = int(age)
    else:
        age = None
    
    if idPlatform:
        idPlatform = int(idPlatform)
    else:
        idPlatform = None

    # Guardar los datos en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO formularioayuda (names, surnames, eventZone, email, phone, idPlatform, age) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (names, surnames, eventZone, email, phone, idPlatform, age))
    mysql.connection.commit()
    cur.close()

    return "Formulario recibido y procesado con éxito."


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run()




def create_pipeline():
    stanza.download("es")
    nlp = stanza.Pipeline("es")
    return nlp

# with open('es_pipeline.pkl', 'wb') as f:
#     pickle.dump(create_pipeline, f)


def iniciaAnalisis(file):
    

    nlp = create_pipeline()


    df = txttopd.panditas_android(file,nlp)
