# Asistente de Soporte Operativo L1 (MVP Basado en Reglas)

Este repositorio contiene el prototipo inicial (MVP) de un asistente conversacional diseñado para el equipo de soporte técnico y operaciones (DevSecOps). El objetivo del proyecto es reducir el Tiempo Medio de Recuperación (MTTR) durante incidentes críticos, permitiendo a los analistas consultar procedimientos de los *runbooks* mediante lenguaje natural.

## 🚀 Características
* **Procesamiento de Lenguaje Natural (NLP):** Utiliza tokenización, eliminación de *stopwords* y *stemming* para procesar las consultas.
* **Basado en Reglas:** Mapea las intenciones del usuario contra una base de conocimiento predefinida con los incidentes operativos más comunes.
* **Arquitectura Modular:** Código segmentado bajo el principio de responsabilidad única para facilitar su mantenimiento y escalabilidad.

## 📋 Prerrequisitos
Para ejecutar este proyecto de forma local, necesitas tener instalado lo siguiente:
* [Python 3.10](https://www.python.org/downloads/) o superior.
* Librería de Procesamiento de Lenguaje Natural `nltk`.

## ⚙️ Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO
   ```

2. **Instalar dependencias:**
   ```bash
   pip install nltk
   ```

3. **Ejecutar el pipeline principal:**
   ```bash
   python main.py
   ```
   *(Nota: En la primera ejecución, el sistema descargará de forma silenciosa los paquetes requeridos por NLTK como 'punkt' y 'stopwords').*

## 📁 Estructura del Proyecto

El código está dividido en cuatro módulos lógicos:

* `base_conocimiento.py`: Almacena la matriz de intenciones (palabras clave) y las directrices técnicas extraídas de los *runbooks*.
* `preprocesamiento.py`: Maneja las dependencias de NLTK y aplica el pipeline de limpieza de texto (conversión a minúsculas, tokenización y *stemming*).
* `motor_inferencia.py`: Contiene la lógica matemática para emparejar la consulta del usuario con la intención correspondiente.
* `main.py`: Archivo orquestador que ejecuta el bucle conversacional en consola.

## 🛠️ Tecnologías Utilizadas
* **Python**
* **NLTK (Natural Language Toolkit)**
* **Regex (`re`)**

## 👨‍🎓 Contexto Académico
Este proyecto forma parte del primer entregable para la materia de **Desarrollo de Aplicaciones con Inteligencia Artificial** de la Maestría en IA.