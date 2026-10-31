# preprocesamiento.py
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Descargas silenciosas para evitar ensuciar la consola
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

def limpiar_texto(texto):
    texto = re.sub(r'[^\w\s]', '', texto.lower())
    tokens = word_tokenize(texto)
    tokens_limpios = [stemmer.stem(w) for w in tokens if w not in stop_words]
    return tokens_limpios