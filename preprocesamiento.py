# ==============================================================================
# MÓDULO: preprocesamiento.py
# PROPÓSITO: Limpieza y normalización lingüística (Pipeline NLP clásico).
# CONCEPTO IA: En Procesamiento de Lenguaje Natural (NLP), los algoritmos
# matemáticos no entienden texto crudo con mayúsculas, signos o conjugaciones
# distintas. Este módulo reduce el "ruido" léxico y agrupa palabras por su raíz.
# ==============================================================================

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Descarga silenciosa de diccionarios y tokenizadores de NLTK (Natural Language Toolkit)
# 'punkt' / 'punkt_tab': modelos preentrenados para dividir texto en palabras/oraciones.
# 'stopwords': lista de palabras vacías (artículos, preposiciones) sin carga semántica.
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Inicializamos el Stemmer de Porter/Snowball para el idioma español.
# El stemming recorta sufijos de forma heurística (ej. "facturando", "facturas" -> "factur").
stemmer = SnowballStemmer('spanish')

# DISEÑO CRÍTICO EN NLP DE SOPORTE:
# Por defecto, NLTK incluye palabras como "no", "sin" o "nunca" dentro de las stopwords.
# En soporte técnico, eliminar la palabra "no" invierte el sentido del incidente
# ("no carga el portal" vs "carga el portal"). Por ello, las restamos del conjunto.
negaciones = {'no', 'ni', 'nunca', 'jamas', 'sin', 'tampoco'}
stop_words = set(stopwords.words('spanish')) - negaciones


def limpiar_texto(texto: str) -> str:
    """
    Ejecuta las 4 etapas estándar de preprocesamiento de texto para clasificación:
      1. Normalización: Estandariza caracteres a minúsculas y limpia símbolos/URLs.
      2. Tokenización: Segmenta la cadena continua en una lista discreta de tokens.
      3. Filtrado de Stopwords: Elimina palabras de relleno conservando negaciones.
      4. Stemming: Reduce cada palabra a su raíz morfológica para compactar el vocabulario.

    Args:
        texto (str): Consulta original ingresada por el analista de soporte.

    Returns:
        str: Cadena de raíces léxicas separadas por espacio, lista para vectorización.
    """
    # --- ETAPA 1: NORMALIZACIÓN ---
    # Convertimos a minúsculas para evitar que "Error" y "error" se traten como palabras distintas.
    texto_norm = texto.lower().strip()
    
    # Reemplazamos enlaces web por el token genérico 'url' para no inflar el vocabulario con dominios únicos.
    texto_norm = re.sub(r'http\S+|www\S+', ' url ', texto_norm)
    
    # Eliminamos signos de puntuación y caracteres especiales (con Regex: todo lo que no sea letra, número o espacio).
    texto_norm = re.sub(r'[^\w\s]', ' ', texto_norm)
    
    # Colapsamos múltiples espacios consecutivos en uno solo.
    texto_norm = re.sub(r'\s+', ' ', texto_norm).strip()
    
    # --- ETAPA 2: TOKENIZACIÓN ---
    # Dividimos el texto normalizado en unidades mínimas (tokens/palabras).
    tokens = word_tokenize(texto_norm, language='spanish')
    
    # --- ETAPA 3 y 4: ELIMINACIÓN DE STOPWORDS Y STEMMING ---
    # Iteramos sobre cada token: descartamos si es stopword o si es un carácter aislado (len <= 1),
    # y aplicamos stemmer.stem() para obtener la raíz.
    tokens_procesados = [
        stemmer.stem(token) for token in tokens 
        if token not in stop_words and len(token) > 1
    ]
    
    # Reconstruimos el texto limpio como string, formato esperado por TfidfVectorizer de scikit-learn.
    return " ".join(tokens_procesados)


if __name__ == "__main__":
    # Bloque de prueba unitaria para visualizar la transformación paso a paso
    ejemplo = "El portal web de facturación NO responde y arroja error 500 en cierre de mes!"
    print("Texto Original :", ejemplo)
    print("Texto Procesado:", limpiar_texto(ejemplo))
