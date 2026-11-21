# 🤖 AISupportAssistant: Asistente de Soporte Operativo L1

Este proyecto nace del prototipo de un asistente inteligente pensado para ayudar a equipos de soporte técnico y operaciones a diagnosticar fallas más rápido. La idea surge con un objetivo claro: reducir el tiempo que toma resolver un incidente crítico (MTTR) permitiendo que el analista de soporte describa el problema en sus propias palabras y, además, pueda adjuntar una captura de pantalla del error para recibir los pasos de solución (obteniendolos de  los runbooks entregados por parte del equipo de desarrollo).

Durante los temas de la materia, el asistente fue evolucionando desde un sistema sencillo basado en texto hasta un modelo multimodal que combina **Procesamiento de Lenguaje Natural (NLP)** y **Visión por Computadora**.

### 📌 Evidencia 1: Asistente de procesamiento de Lenguaje natural

En la primera etapa se desarrollo la base del proyecto enfocándome en entender el texto que escribe el usuario:

* **Limpieza de texto (NLP):** Se implementó un pipeline con `NLTK` y expresiones regulares para pasar todo a minúsculas, quitar palabras vacías (*stopwords*) y reducir las palabras a su raíz (*stemming*).
* **Base de conocimiento:** Se generó un catálogo con los incidentes mas recurrentes para un portal web de facturación y sus procedimientos de solución (obtenidos de los *runbooks* de soporte).
* **Código ordenado:** Dividí el proyecto en módulos pequeños (`preprocesamiento.py`, `base_conocimiento.py`, `motor_inferencia.py` y `main.py`) con el objetivo de tener un objetivo claro por modulo.
* **Chat en consola:** Un flujo sencillo en terminal donde escribes tu problema y el asistente te responde.

### 📌 Evidencia 2: Modelos de Machine Learning y Síntesis Multimodal

Para la segunda entrega se dio un salto de reglas fijas a modelos entrenados capaces de analizar tanto **texto** como **imágenes**:

* **Clasificador de Texto con ML:** Entrené un modelo usando **TF-IDF** (`vectorizador_tfidf.joblib`) y una **Máquina de Vectores de Soporte / SVM** (`modelo_nlp_svm.joblib`) a partir de `dataset_intenciones.csv`. Ahora el sistema predice la intención del usuario junto con su porcentaje de confianza.
* **Clasificador Visual con Deep Learning:** Usé **TensorFlow/Keras** con una arquitectura **ResNet50** (`clasificador_visual.py`) para analizar capturas de pantalla de errores y clasificarlas en 4 categorías: `alerta_base_datos`, `error_http_500`, `fallo_pipeline_cicd` y `terminal_logs_error`.
* **Síntesis Multimodal (Cruce de información):** En esta parte el aisstente compara lo que dice el texto contra lo que ve en la imagen e intrpreta en base a las siguientes decisiones:
  * **Si ambos coinciden:** Marca un **Diagnóstico Confirmado**, dándonos mucha más seguridad antes de actuar.
  * **Si se contradicen:** El sistema evalúa cuál de los dos modelos está más seguro (mayor porcentaje de confianza) y prioriza ese diagnóstico.
  * **Si no tienes imagen a la mano:** puedes dar Enter y el sistema omitirá la captura haciendo que el asistente funcione sin problemas con base a la interpretacióm del texto.
* **Métricas de evaluación:** Se agregaron reportes de clasificación (*precision*, *recall*, *f1-score*) y matriz de confusión con `scikit-learn` para comprobar qué tan bien estaba aprendiendo el modelo visual.

## 📋 Requerimientos necesarios: Lo que necesitas antes de empezar

* **Python 3.11 o 3.12:** La prueba se realizo con Python 3.12.
* **Entorno virtual (`venv`):** Para no revolver librerias con otros proyectos

## ⚙️ Cómo instalarlo y correrlo en tu computadora

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO
   ```

2. **Crea y activa tu entorno virtual:**
   En Windows (PowerShell):
   ```powershell
   py -3.12 -m venv C:\venvs\ai_support
   C:\venvs\ai_support\Scripts\Activate.ps1
   ```

3. **Instala las librerías necesarias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   *(Aquí se instalan `tensorflow`, `scikit-learn`, `pillow`, `nltk`, `joblib`, `numpy` y `pandas`).*

4. **Descarga el dataset de imágenes y genera el modelo visual (Importante):**
   Por su tamaño (> 90 MB), la carpeta `dataset_imagenes/` y el modelo entrenado `modelo_visual_resnet50.keras` no están incluidos directamente en este repositorio para evitar problemas con los límites de peso de GitHub.

   Si deseas revisar las imágenes o volver a entrenar el clasificador visual del agente, puedes descargar la carpeta completa desde el siguiente enlace:

   👉 **[Descargar dataset_imagenes desde OneDrive](https://1drv.ms/f/c/d1f942fca79dd4e3/IgCl1wxI7jWURLax_WE7VG6nAXdUT8iyQoKAqLk3KYNKai0?e=sCyfYu)**

   👉 **[Descargar de modelo entrenado keras desde OneDrive](https://1drv.ms/u/c/d1f942fca79dd4e3/IQCwGTmWHP6YTYZp7SKyrBIIAdpte1b_D6Zttur5rWmzmEM?e=ptIFM9)**

   * Coloca la carpeta `dataset_imagenes/` y el archivo modelo_visual_resnet50.keras descargados en la raíz del proyecto (al mismo nivel que `main.py`), verificando que la carpeta de imagenes contenga las subcarpetas por clase: `alerta_base_datos`, `error_http_500`, `fallo_pipeline_cicd` y `terminal_logs_error`.


   **En caso que requiera reentrenar el asistente**
   * Ejecute el script de visión para entrenar y genere el archivo `modelo_visual_resnet50.keras`:
  e   ```bash
     python clasificador_visual.py
     ```

5. **Para probar el asistente**
   ```bash
   python main.py
   ```
   El asistente solicitara que describas el incidente y después pedira la ruta donde dejaste la captura de pantalla relacionada al incidente. (Puedes intentar con un ejemplo como "La base de datos en la nube está muy lenta y hay bloqueos en el cierre de mes" y tomar alguna captura de pantalla de dataset_imagenes o generar alguna propia)
   

## 📁 ¿Qué hay en cada archivo?

```text
AISupportAssistant/
├── base_conocimiento.py          # Aquí viven las intenciones y los runbooks de solución
├── clasificador_visual.py        # Entrena, evalúa y hace predicciones con la red ResNet50
├── dataset_intenciones.csv       # Ejemplos de texto etiquetados para entrenar el modelo NLP
├── main.py                       # El archivo principal que une todo y toma la decisión final
├── modelo_nlp_svm.joblib         # Modelo SVM ya entrenado (listo para usarse)
├── motor_inferencia.py           # Se encarga de predecir la intención del texto y su confianza
├── preprocesamiento.py           # Limpia y prepara el texto antes de pasarlo al modelo
├── requirements.txt              # Lista de librerías exactas para replicar el entorno
├── vectorizador_tfidf.joblib     # Transforma el texto en vectores numéricos para el SVM
├── README.md                     # Esta guía que estás leyendo
├── dataset_imagenes/             # [En OneDrive / fuera de Git por peso > 90 MB] Imágenes de entrenamiento/prueba
└── modelo_visual_resnet50.keras  # [En OneDrive / fuera de Git por peso > 90 MB] Modelo visual guardado
```

## 🛠️ Herramientas y Librerías que usé

* **Python 3.12** como lenguaje base.
* **TensorFlow / Keras (ResNet50)** y **Pillow** para procesar y clasificar imágenes.
* **Scikit-learn**, **NLTK** y **Joblib** para el procesamiento de texto, entrenamiento del SVM y evaluación de métricas.
* **Git y GitHub** para el control de versiones (y **OneDrive** para respaldar el dataset pesado).

## 🎓 Sobre este proyecto

Este repositorio forma parte de mis entregas (**Evidencia 1** y **Evidencia 2**) para la materia de **Desarrollo de Aplicaciones con Inteligencia Artificial** en la **Maestría en Inteligencia Artificial**. El asistente ha sido un gran reto para mi y me a ayudado a entender cómo conectar distintos modelos de IA en una misma aplicación práctica y resolver retos reales en mi dia a dia  laboral.
