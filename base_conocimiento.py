# ==============================================================================
# MÓDULO: base_conocimiento.py
# PROPÓSITO: Repositorio estructurado de conocimiento operativo (Runbooks).
# CONCEPTO IA: En sistemas híbridos de IA (Neuro-Simbólicos o Clasificación +
# Reglas de Negocio), el modelo de Machine Learning clasifica la "intención",
# mientras que la base de conocimiento garantiza que la respuesta entregada sea
# determinista, auditable y libre de alucinaciones.
# ==============================================================================

intenciones_runbooks = {
    "saludo": {
        "respuesta": (
            "Hola. Soy IASupportAssistant (v2 Multimodal). Estoy listo para apoyarte con "
            "incidentes del portal de facturación en la nube. Puedes describir el problema o "
            "adjuntar una captura de pantalla."
        )
    },
    "reinicio_servicio": {
        "respuesta": (
            "[RUNBOOK-WEB-01] Para reiniciar el web server sin perder sesiones activas durante "
            "picos de tráfico: 1) Verifica nodos activos en el balanceador. 2) Accede por SSH y "
            "ejecuta: 'sudo systemctl reload-or-restart nginx && sudo systemctl restart billing_portal.service'."
        )
    },
    "logs_aplicacion": {
        "respuesta": (
            "[RUNBOOK-LOG-02] Los registros del portal de facturación se almacenan en "
            "'/var/log/billing-portal/production.log' y '/var/log/nginx/error.log'. Ejecuta: "
            "'tail -n 100 -f /var/log/billing-portal/production.log | grep -iE "ERROR|CFDI|TIMEOUT"'."
        )
    },
    "error_500": {
        "respuesta": (
            "[RUNBOOK-HTTP-500] El Error 500 indica saturación de workers o memoria en el web server "
            "ante picos de usuarios. Verifica uso de RAM ('free -h'), escala instancias en el grupo de "
            "autoescalado y revisa excepciones de timbrado en los logs."
        )
    },
    "despliegue_fallido": {
        "respuesta": (
            "[RUNBOOK-CICD-04] Si el pipeline de GitHub Actions falló: 1) Revisa el job fallido en "
            "la pestaña Actions. 2) Valida variables de entorno y secretos de conexión a la nube. "
            "3) Si el ambiente quedó inconsistente, ejecuta el workflow 'Rollback-Production'."
        )
    },
    "bloqueo_cuenta": {
        "respuesta": (
            "[RUNBOOK-IAM-05] Para desbloquear cuentas de usuarios o analistas: ingresa al portal de "
            "Azure AD -> Usuarios -> busca el correo corporativo -> selecciona 'Desbloquear inicio de sesión' "
            "y ejecuta 'Restablecer contraseña temporal'."
        )
    },
    "base_datos_lenta": {
        "respuesta": (
            "[RUNBOOK-DB-06] Ante lentitud o timeouts en Oracle/SQL en la nube por cierres de mes: "
            "1) Revisa el pool de conexiones activas. 2) Consulta bloqueos ('v$session' / 'sys.dm_exec_requests') "
            "en tablas de facturación. 3) Escala temporalmente las IOPS/vCores de la instancia."
        )
    },
    "certificados_ssl": {
        "respuesta": (
            "[RUNBOOK-SEC-07] Para renovar certificados SSL vencidos: 1) Genera un nuevo CSR con OpenSSL. "
            "2) Tramita la firma con la autoridad certificadora. 3) Carga el archivo .crt y .key en "
            "'/etc/nginx/ssl/' y ejecuta 'sudo nginx -t && sudo systemctl reload nginx'."
        )
    },
    "escalar_l3": {
        "respuesta": (
            "[RUNBOOK-ESC-08] Escalamiento formal generado: adjunta el ID de correlación, traza de error "
            "y captura diagnóstica. Asigna el ticket en ServiceNow al grupo 'Cloud-Billing-L3-Architecture' "
            "con prioridad Alta."
        )
    },
    "despedida": {
        "respuesta": (
            "¡Hasta luego! Recuerda documentar la causa raíz y el tiempo de recuperación (MTTR) "
            "en el ticket correspondiente."
        )
    }
}
