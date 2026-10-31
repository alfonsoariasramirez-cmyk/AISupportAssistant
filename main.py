# main.py
from motor_inferencia import evaluar_intencion

def ejecutar_pipeline():
    print("Soy una IA Asistente de soporte L1 (Escribe 'salir' para terminar)")
    while True:
        entrada = input("¿Dime en que puedo apoyarte?")
        if entrada.lower() == 'salir':
            print("Apagando Asistente... ¡Hasta luego!")
            break
        
        respuesta = evaluar_intencion(entrada)
        print(f"Respuesta: {respuesta}\n")

if __name__ == "__main__":
    ejecutar_pipeline()