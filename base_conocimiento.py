# base_conocimiento.py

intenciones = {
    "saludo": {
        "keywords": ["hola", "buen", "dia", "tard", "ayud", "soporte"],
        "respuesta": "Hola. Soy tu asistente operativo de IA. ¿Dime que incidente atenderemos hoy?"
    },
    "reinicio_servicio": {
        "keywords": ["reinici", "levant", "caid", "inici", "servic", "servidor"],
        "respuesta": "Para reiniciar el web server, accede por SSH y ejecuta: 'sudo systemctl restart web_service'."
    },
    "logs_aplicacion": {
        "keywords": ["log", "traz", "registr", "revis", "error", "buscar"],
        "respuesta": "Los logs se encuentran en: '/var/log/app/production.log'. Usa 'tail -f'."
    },
    "error_500": {
        "keywords": ["500", "internal", "portal", "caid", "acces", "http"],
        "respuesta": "El Error 500 suele indicar saturación de memoria. Revisa los logs de los contenedores Docker."
    },
    "despliegue_fallido": {
        "keywords": ["despliegu", "releas", "fall", "pipelin", "trab", "accion", "github"],
        "respuesta": "Si el despliegue falló, verifica el error en la consola de GitHub Actions."
    },
    "bloqueo_cuenta": {
        "keywords": ["bloque", "cuent", "contraseñ", "password", "usuari", "reset"],
        "respuesta": "Para desbloquear, ingresa a Azure AD y selecciona 'Restablecer contraseña'."
    },
    "base_datos_lenta": {
        "keywords": ["bas", "dat", "lent", "timeout", "bd", "query"],
        "respuesta": "Verifica las conexiones activas en el motor de base de datos o revisa si hay algún lock en las tablas consultadas."
    },
    "certificados_ssl": {
        "keywords": ["certific", "ssl", "venc", "expir", "renov"],
        "respuesta": "Genera un nuevo CSR, envialo al proveedor de certificados para su firma y cárgalo en la consola de NGINX."
    },
    "escalar_l3": {
        "keywords": ["escal", "nivel", "l3", "arquitectur", "pod", "resolv"],
        "respuesta": "Generando resumen de la falla. Asigna el ticket al grupo 'L3 Support'."
    },
    "despedida": {
        "keywords": ["graci", "adi", "list", "resuelt", "ok"],
        "respuesta": "¡Hasta luego! Recuerda documentar la resolución y causa raiz en el ticket de soporte."
    }
}