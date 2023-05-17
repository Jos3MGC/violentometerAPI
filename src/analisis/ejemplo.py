# Este código solo es para ver la estructura del inicio del manejo de datos de texto
import pandas as pd
import TxtToPd as txttopd
import stanza
stanza.download("es")
nlp = stanza.Pipeline("es")



with open(r'src\analisis\Chat de WhatsApp con Equipo 3.txt', encoding='utf-8') as f:
    chat_sinlimpiar = f.read()

print(chat_sinlimpiar)
df = txttopd.panditas_android(chat_sinlimpiar,nlp)

print(str(df["mensaje"]))