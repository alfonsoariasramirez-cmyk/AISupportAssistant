# ==============================================================================
# MÓDULO: clasificador_visual.py
# PROPÓSITO: Clasificación de capturas de pantalla de incidentes mediante CNN
#            y Transfer Learning (Aprendizaje por Transferencia).
# CONCEPTO IA:
#   Entrenar una Red Neuronal Convolucional (CNN) profunda desde cero requiere
#   miles de imágenes y alto cómputo. Con Transfer Learning reutilizamos
#   ResNet50 (preentrenada en 1.4 millones de imágenes de ImageNet) como
#   extractor automático de características visuales (bordes, bloques de texto,
#   ventanas, gráficos), congelando sus pesos y entrenando únicamente una capa
#   clasificadora final adaptada a nuestras 4 categorías de errores operativos.
# ==============================================================================
TF_CPP_MIN_LOG_LEVEL="2"
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50  # pyright: ignore[reportMissingImports]
from tensorflow.keras.applications.resnet50 import preprocess_input  # pyright: ignore[reportMissingImports]
from tensorflow.keras import layers, models  # pyright: ignore[reportMissingModuleSource]
from tensorflow.keras.utils import load_img, img_to_array  # pyright: ignore[reportMissingImports]
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, classification_report
)

# Clases visuales del dominio ordenadas alfabéticamente (convención estándar de Keras
# cuando lee carpetas con image_dataset_from_directory)
CLASES_VISUALES = [
    "alerta_base_datos",
    "error_http_500",
    "fallo_pipeline_cicd",
    "terminal_logs_error"
]

# Puente semántico que conecta la salida visual de la CNN con las intenciones del Runbook
MAPEO_VISUAL_A_INTENCION = {
    "alerta_base_datos": "base_datos_lenta",
    "error_http_500": "error_500",
    "fallo_pipeline_cicd": "despliegue_fallido",
    "terminal_logs_error": "logs_aplicacion"
}

MODELO_VISUAL_PATH = "modelo_visual_resnet50.keras"


def construir_modelo_resnet50(num_clases: int = 4):
    """
    Ensambla la arquitectura de Visión por Computadora usando Functional API de Keras:
      Entrada (224x224x3) -> Data Augmentation -> Preprocess ResNet50 ->
      Base ResNet50 (Congelada) -> GlobalAveragePooling2D -> Dropout -> Dense Softmax.
    """
    # 1. Data Augmentation (Aumento de Datos):
    # Genera variaciones sintéticas en cada época (rotaciones ligeras, zoom, contraste)
    # para prevenir el sobreajuste (overfitting) en datasets pequeños.
    # Nota: No aplicamos RandomFlip("horizontal") porque invertiría el texto de las pantallas.
    data_augmentation = tf.keras.Sequential([
        layers.RandomRotation(0.05),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),
    ], name="data_augmentation")

    # 2. Backbone / Extractor de Características (ResNet50):
    # include_top=False descarta la capa original de 1000 clases de ImageNet.
    base_model = ResNet50(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )
    # Congelamos la red base para que el gradiente no destruya los filtros preentrenados
    # durante las primeras iteraciones de nuestra nueva cabeza clasificadora.
    base_model.trainable = False

    # 3. Flujo de tensores (Functional API)
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    
    # preprocess_input convierte RGB a BGR y centra cada canal respecto a la media de ImageNet
    x = preprocess_input(x)
    
    # training=False asegura que las capas BatchNormalization internas de ResNet50
    # operen en modo inferencia usando sus estadísticas globales aprendidas.
    x = base_model(x, training=False)
    
    # GlobalAveragePooling2D promedia cada mapa de características (7x7x2048 -> vector de 2048),
    # reduciendo drásticamente parámetros frente a Flatten().
    x = layers.GlobalAveragePooling2D()(x)
    
    # Dropout(0.3) apaga aleatoriamente el 30% de neuronas en entrenamiento para regularizar.
    x = layers.Dropout(0.3)(x)
    
    # Capa de salida con activación Softmax: produce una distribución de probabilidad
    # sobre las 4 clases visuales (la suma de las 4 salidas es igual a 1.0).
    outputs = layers.Dense(num_clases, activation="softmax")(x)

    modelo = models.Model(inputs, outputs, name="ResNet50_SoporteOperativo")
    
    # Compilación con Adam y categorical_crossentropy (pérdida estándar para multiclase one-hot)
    modelo.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return modelo


def entrenar_y_evaluar_visual(directorio_dataset: str = "dataset_imagenes"):
    """
    Entrena el modelo visual a partir de directorios organizados por clase
    (dataset_imagenes/train, val, test) y calcula las 5 métricas de evaluación:
    Accuracy, Precision, Recall, F1-score y Matriz de Confusión.
    """
    if not os.path.exists(directorio_dataset):
        print(f"[AVISO] No se encontró la carpeta '{directorio_dataset}'.")
        print("Se inicializará y guardará la arquitectura base ResNet50 compilada para pruebas de flujo.")
        modelo = construir_modelo_resnet50(len(CLASES_VISUALES))
        modelo.save(MODELO_VISUAL_PATH)
        return modelo

    # Carga eficiente por lotes (batches) redimensionando al tamaño nativo de ResNet50 (224x224)
    train_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(directorio_dataset, "train"),
        image_size=(224, 224), batch_size=32, label_mode="categorical", shuffle=True
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(directorio_dataset, "val"),
        image_size=(224, 224), batch_size=32, label_mode="categorical", shuffle=False
    )
    test_ds = tf.keras.utils.image_dataset_from_directory(
        os.path.join(directorio_dataset, "test"),
        image_size=(224, 224), batch_size=32, label_mode="categorical", shuffle=False
    )

    modelo = construir_modelo_resnet50(len(CLASES_VISUALES))
    
    # EarlyStopping detiene el entrenamiento si val_loss deja de mejorar por 3 épocas seguidas
    # y restaura los mejores pesos alcanzados.
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=3, restore_best_weights=True
    )

    modelo.fit(train_ds, validation_data=val_ds, epochs=15, callbacks=[early_stop])
    modelo.save(MODELO_VISUAL_PATH)

    # Evaluación rigurosa sobre el conjunto de prueba (test_ds) nunca visto en entrenamiento
    y_true = []
    y_pred = []
    for imgs, labels in test_ds:
        preds = modelo.predict(imgs, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

    print("\n=== MÉTRICAS DEL CLASIFICADOR VISUAL (RESNET50) ===")
    print(f"Accuracy : {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred, average='weighted'):.4f}")
    print(f"Recall   : {recall_score(y_true, y_pred, average='weighted'):.4f}")
    print(f"F1-Score : {f1_score(y_true, y_pred, average='weighted'):.4f}\n")
    print("=== REPORTE POR CLASE ===")
    print(classification_report(y_true, y_pred, target_names=CLASES_VISUALES))
    print("=== MATRIZ DE CONFUSIÓN ===")
    print(confusion_matrix(y_true, y_pred))

    return modelo


def clasificar_imagen_incidente(ruta_imagen: str):
    """
    Realiza inferencia visual sobre una captura de pantalla individual:
      1. Carga la imagen y la redimensiona a (224, 224) píxeles.
      2. La convierte a un tensor NumPy y añade la dimensión de lote -> (1, 224, 224, 3).
      3. Ejecuta forward-pass en ResNet50 y mapea la clase ganadora a una intención operativa.
    """
    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(f"La imagen '{ruta_imagen}' no existe.")

    if os.path.exists(MODELO_VISUAL_PATH):
        modelo = tf.keras.models.load_model(MODELO_VISUAL_PATH)
    else:
        modelo = construir_modelo_resnet50(len(CLASES_VISUALES))

    # Conversión de imagen a tensor de entrada
    img = load_img(ruta_imagen, target_size=(224, 224))
    img_array = img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)  # Keras espera shape (batch_size, H, W, C)

    # Inferencia
    predicciones = modelo.predict(img_batch, verbose=0)[0]
    idx_max = int(np.argmax(predicciones))
    clase_visual = CLASES_VISUALES[idx_max]
    confianza = float(predicciones[idx_max])
    intencion_asociada = MAPEO_VISUAL_A_INTENCION[clase_visual]

    return clase_visual, confianza, intencion_asociada


if __name__ == "__main__":
    entrenar_y_evaluar_visual()
