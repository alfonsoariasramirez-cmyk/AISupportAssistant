# ==============================================================================
# MÓDULO: motor_inferencia.py
# PROPÓSITO: Representación vectorial TF-IDF y clasificación supervisada de texto.
# CONCEPTO IA:
#   - TF-IDF (Term Frequency - Inverse Document Frequency): Pondera qué tan
#     importante es una palabra en una consulta respecto a todo el dataset.
#     Palabras muy frecuentes en todas las clases (ej. "portal") reciben menor
#     peso que términos discriminativos (ej. "ssl", "oracle", "500").
#   - SVM (Support Vector Machine): Encuentra el hiperplano óptimo en un espacio
#     de alta dimensión que maximiza el margen de separación entre las 10 clases.
# ==============================================================================

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from preprocesamiento import limpiar_texto
from base_conocimiento import intenciones_runbooks

# Rutas donde se serializan (guardan en disco) los artefactos entrenados
# para evitar reentrenar el modelo cada vez que se ejecuta el asistente.
MODELO_PATH = "modelo_nlp_svm.joblib"
VECTORIZER_PATH = "vectorizador_tfidf.joblib"


def entrenar_y_evaluar_nlp(csv_path: str = "dataset_intenciones.csv"):
    """
    Entrena y evalúa dos algoritmos clásicos de clasificación de texto:
      1. Multinomial Naive Bayes (modelo probabilístico generativo, línea base).
      2. SVM con kernel lineal (modelo discriminativo de alto rendimiento en NLP).

    Aplica validación hold-out estratificada (80% entrenamiento, 20% prueba)
    para medir la capacidad de generalización sobre consultas no vistas.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"No se encontró el dataset '{csv_path}'. Colócalo en la raíz del proyecto."
        )
        
    # 1. Carga de datos y aplicación del pipeline NLP de preprocesamiento
    df = pd.read_csv(csv_path)
    df["texto_limpio"] = df["texto_consulta"].apply(limpiar_texto)
    
    # 2. División estratificada (stratify=df["intencion"]):
    # Garantiza que tanto el set de entrenamiento (240 filas) como el de prueba (60 filas)
    # mantengan exactamente la misma proporción de ejemplos por clase (24 y 6 por intención).
    X_train, X_test, y_train, y_test = train_test_split(
        df["texto_limpio"], 
        df["intencion"],
        test_size=0.20, 
        random_state=42, 
        stratify=df["intencion"]
    )
    
    # 3. Extracción de características mediante TF-IDF:
    # ngram_range=(1, 2) captura tanto palabras sueltas (unigramas: "error") como
    # pares consecutivos (bigramas: "error 500", "certific ssl"), preservando contexto local.
    # IMPORTANTE: fit_transform() se aplica SOLO en X_train para evitar Data Leakage (fuga de datos).
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1500)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 4A. Entrenamiento Modelo Base: Multinomial Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train_vec, y_train)
    y_pred_nb = nb_model.predict(X_test_vec)
    acc_nb = accuracy_score(y_test, y_pred_nb)
    
    # 4B. Entrenamiento Modelo Principal: SVM Lineal
    # probability=True activa la calibración de Platt (validación cruzada interna) para
    # convertir las distancias al hiperplano en probabilidades entre 0 y 1 (predict_proba).
    svm_model = SVC(kernel="linear", C=1.0, probability=True, random_state=42)
    svm_model.fit(X_train_vec, y_train)
    y_pred_svm = svm_model.predict(X_test_vec)
    acc_svm = accuracy_score(y_test, y_pred_svm)
    
    # 5. Reporte comparativo de métricas (Precision, Recall, F1-score)
    print("=== COMPARACIÓN DE MODELOS NLP (TF-IDF) ===")
    print(f"Accuracy Multinomial Naive Bayes : {acc_nb:.4f}")
    print(f"Accuracy SVM Lineal             : {acc_svm:.4f}\n")
    
    print("=== REPORTE DE CLASIFICACIÓN DETALLADO (SVM LINEAL) ===")
    print(classification_report(y_test, y_pred_svm))
    
    # 6. Persistencia del modelo y del vocabulario TF-IDF entrenado
    joblib.dump(svm_model, MODELO_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("Artefactos serializados: 'modelo_nlp_svm.joblib' y 'vectorizador_tfidf.joblib'.")
    return svm_model, vectorizer


def cargar_modelo_nlp():
    """Carga los modelos desde disco si ya existen; de lo contrario, los entrena."""
    if not os.path.exists(MODELO_PATH) or not os.path.exists(VECTORIZER_PATH):
        return entrenar_y_evaluar_nlp()
    return joblib.load(MODELO_PATH), joblib.load(VECTORIZER_PATH)


def predecir_intencion_texto(texto_usuario: str, umbral_confianza: float = 0.25):
    """
    Realiza la inferencia sobre una nueva consulta en tiempo real:
      1. Limpia el texto usando exactamente las mismas reglas de entrenamiento.
      2. Proyecta el texto en el espacio vectorial TF-IDF.
      3. Obtiene la distribución de probabilidad sobre las 10 intenciones.
      4. Aplica un umbral de rechazo (threshold) para evitar respuestas erróneas
         cuando el usuario ingresa texto ambiguo o fuera de dominio.
    """
    modelo, vectorizer = cargar_modelo_nlp()
    texto_proc = limpiar_texto(texto_usuario)
    vec = vectorizer.transform([texto_proc])
    
    # predict_proba devuelve un arreglo con la probabilidad de cada una de las 10 clases
    probabilidades = modelo.predict_proba(vec)[0]
    max_idx = probabilidades.argmax()
    confianza = float(probabilidades[max_idx])
    intencion_predicha = modelo.classes_[max_idx]
    
    if confianza < umbral_confianza:
        return (
            "desconocida", 
            confianza, 
            "No logré identificar con suficiente certeza el incidente. ¿Podrías detallar más o adjuntar una captura de pantalla?"
        )
        
    respuesta = intenciones_runbooks[intencion_predicha]["respuesta"]
    return intencion_predicha, confianza, respuesta


if __name__ == "__main__":
    entrenar_y_evaluar_nlp()
