from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

MAX_NB_WORDS = 50000
MAX_SEQUENCE_LENGTH = 200
EMBEDDING_DIM = 100

def predict(df,model):
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    tokenizer.fit_on_texts(df['mensaje'].values)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    X = tokenizer.texts_to_sequences(df['mensaje'].values)
    X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)
    print('Shape of data tensor:', X.shape)
    

    # Load the model from the pickle file
    print("abre pepinillo")
    try:
        print("prediction")
        # Use the loaded model for predictions or other tasks
        predictions = model.predict(X)
    except:
        print("No hizo prediccion")

    df["prediccion"] = predictions

    #transforms into a diccionary
    findic = dict()
    for i in df.iterrows():
        print(i[1].keys())
        findic[i[1]["mensaje"]] = i[1]["prediccion"]

    aux = dict()
    aux["promedio"] = np.float64(df["prediccion"].mean())
    aux["frecuencia"] = findic

    return aux
