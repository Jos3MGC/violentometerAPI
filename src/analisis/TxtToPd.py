import pandas as pd
import regex as re
from unidecode import unidecode
from nltk.corpus import stopwords



def panditas_android(chat_sinlimpiar,nlp):
    ''' Recibe texto '''

    # Abrimos el archivo o manejamos el contenido del txt
    # with open(dir_Archivo, encoding='utf-8') as f:
    #     chat_sinlimpiar = f.read()

    #manejamos posibles saltos que se encuentren en los mensajes
    chat_saltos = ""
    for e, i in enumerate(chat_sinlimpiar):
        if i == '\n' and e+1 < len(chat_sinlimpiar) and not chat_sinlimpiar[e+1].isdigit():
            chat_saltos += ' '
        else:
            chat_saltos += i

    #pasamos cada mensaje a una lista
    mensajes = []
    for  m in chat_saltos.split('\n'):
        mensajes.append(m)

    del chat_saltos
    del chat_sinlimpiar

    #separamos el texto que nos importa de los demás
    data = []
    for line in mensajes:
        match = re.search(r'(?<=):(.+)(?<=):(.+)', line)
        if match:
            data.append(match.groups())
    #convertimos a dataframe
    df = pd.DataFrame(data, columns=['basura', 'mensaje'])

    del df['basura']
    print("empieza limpieza")
    return limpieza(df,nlp)


def limpieza(df,nlp):

    # Definir la expresión regular para eliminar la puntuación
    regex_puntuacion = re.compile('[^\w\s]')

    # Eliminar Puntuacion
    df['mensaje'] = df['mensaje'].apply(lambda x: regex_puntuacion.sub('', x))
    # Eliminar Acentos
    df['mensaje'] = df['mensaje'].apply(lambda x: unidecode(regex_puntuacion.sub('', x)))
    # Convertir A minusculas
    df['mensaje'] = df['mensaje'].apply(lambda x: x.lower())
    # Eliminar StopWorlds el/la/yo etc
    df['mensaje'] = df['mensaje'].apply(limpiar_texto)
    # Lematizar
    # df['mensaje'] = df['mensaje'].apply(lematizar(nlp))
    print("empieza lematizar")
    df['mensaje'] = df['mensaje'].apply(lambda x: lematizar(x, nlp))

    return(df)


def limpiar_texto(texto):
    palabras_vacias = set(stopwords.words('spanish'))
    palabras = texto.split()
    palabras_sin_vacias = [palabra for palabra in palabras if palabra not in palabras_vacias]
    texto_sin_vacias = ' '.join(palabras_sin_vacias)
    return texto_sin_vacias


def lematizar(texto,nlp):
    doc = nlp(texto)
    palabras_lematizadas = [word.lemma for sent in doc.sentences for word in sent.words]
    texto_lematizado = ' '.join(palabras_lematizadas)
    return texto_lematizado