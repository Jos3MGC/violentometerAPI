import pickle
import stanza
import TxtToPd as txttopd

def create_pipeline():
    stanza.download("es")
    nlp = stanza.Pipeline("es")
    return nlp

with open('es_pipeline.pkl', 'wb') as f:
    pickle.dump(create_pipeline, f)

with open('es_pipeline.pkl', 'rb') as f:
    create_pipeline = pickle.load(f)

nlp = create_pipeline()


txttopd.panditas_android("aquí le mandas el texto",nlp)