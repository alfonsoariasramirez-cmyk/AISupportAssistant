# ==============================================================================
# MÓDULO: main.py
# PROPÓSITO: Orquestador Multimodal (Fusión Tardía / Late Fusion).
# CONCEPTO IA:
#   En sistemas de IA Multimodal existen dos estrategias principales de fusión:
#   - Early Fusion (Fusión Temprana): Concatenar los vectores TF-IDF y los
#     embeddings visuales antes de un único clasificador.
#   - Late Fusion (Fusión Tardía - implementada aquí): Cada modalidad (texto e
#     imagen) es procesada por su propio modelo especializado (SVM y ResNet50) y
#     un módulo de decisión combina sus predicciones y niveles de confianza.
# ==============================================================================

import os
from motor_inferencia import predecir_intencion_texto
from clasificador_visual import clasificar_imagen_incidente
from base_conocimiento import intenciones_runbooks


def procesar_consulta_multimodal(texto_usuario: str, ruta_imagen: str = None):
    """
    Coordina la ejecución de los 3 pasos del flujo multimodal:
      Paso 1: Procesamiento y clasificación del texto del usuario (NLP + SVM).
      Paso 2: Clasificación de la evidencia gráfica si el usuario proporciona ruta (CNN ResNet50).
      Paso 3: Síntesis e interpretación conjunta para recuperar el runbook exacto.
    """
    print("\n" + "=" * 65)
    print("PROCESANDO SOLICITUD MULTIMODAL...")
    
    # --- PASO 1: INFERENCIA TEXTUAL ---
    intencion_txt, conf_txt, resp_txt = predecir_intencion_texto(texto_usuario)
    print(f"[1. Componente Textual] Intención: '{intencion_txt}' | Confianza: {conf_txt:.2%}")
    
    # --- PASO 2: INFERENCIA VISUAL (OPCIONAL) ---
    if ruta_imagen and ruta_imagen.strip() != "":
        try:
            clase_vis, conf_vis, intencion_vis = clasificar_imagen_incidente(ruta_imagen.strip())
            print(f"[2. Componente Visual ] Categoría: '{clase_vis}' -> Intención: '{intencion_vis}' | Confianza: {conf_vis:.2%}")
            
            # --- PASO 3: SÍNTESIS Y POLÍTICA DE DECISIÓN MULTIMODAL ---
            print("[3. Síntesis Multimodal]")
            if intencion_txt == intencion_vis:
                # Caso ideal: Concordancia entre ambas modalidades
                print(f"    -> Diagnóstico CONFIRMADO: Tanto el texto como la imagen coinciden en '{intencion_txt}'.")
                respuesta_final = intenciones_runbooks[intencion_txt]["respuesta"]
            elif conf_vis > conf_txt:
                # La descripción textual fue vaga (ej. "revisa esto") pero la captura es clara
                print(f"    -> Priorización VISUAL: La evidencia gráfica ({clase_vis}) tiene mayor certeza ({conf_vis:.2%}) que el texto.")
                respuesta_final = intenciones_runbooks[intencion_vis]["respuesta"]
            else:
                # El texto es altamente específico (ej. solicitud de escalamiento L3)
                print(f"    -> Priorización TEXTUAL: La descripción operativa ({intencion_txt}) tiene mayor certeza ({conf_txt:.2%}).")
                respuesta_final = resp_txt
                
        except FileNotFoundError as e:
            # Manejo resiliente de errores (Graceful Degradation) si la ruta de imagen es inválida
            print(f"[2. Componente Visual ] Error: {e}. Continuando solo con análisis textual.")
            respuesta_final = resp_txt
    else:
        print("[2. Componente Visual ] Sin imagen adjunta.")
        print("[3. Síntesis Multimodal] Resolución basada en modelo supervisado de texto.")
        respuesta_final = resp_txt

    print("=" * 65)
    print(f"Respuesta del Asistente:\n{respuesta_final}\n")


def ejecutar_pipeline():
    """Bucle interactivo principal de consola (CLI) para atención de analistas L1/L2."""
    print("=================================================================")
    print("  IASupportAssistant v2.0 - Asistente Multimodal de Soporte L1/L2")
    print("  Dominio: Portal Web de Facturación en la Nube (Oracle/SQL)")
    print("  (Escribe 'salir' en la consulta para terminar)")
    print("=================================================================")
    
    while True:
        entrada_texto = input("\n¿Dime qué incidente operativo reportas?: ")
        if entrada_texto.lower().strip() == 'salir':
            print("Apagando Asistente Multimodal... ¡Hasta luego!")
            break
            
        entrada_imagen = input("Ruta de captura de pantalla del error (Enter para omitir): ")
        procesar_consulta_multimodal(entrada_texto, entrada_imagen)


if __name__ == "__main__":
    ejecutar_pipeline()
