# Este código solo es para ver la estructura del inicio del manejo de datos de texto
import pickle

with open('GRUmodel.pkl', 'rb') as file:
    model = pickle.load(file)
print(model)
print(model.predict([]))