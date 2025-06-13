def generar_mensaje(servicio):
    nombre = servicio.cliente.nombre
    codigo = servicio.codigo
    estado = servicio.estado

    mensajes_estado = {
        "listo para entregar": f"Hola {nombre}, su equipo {codigo} ya está listo para retirar. ¡Gracias por confiar en nosotros!",
        "entregado": f"Hola {nombre}, su equipo {codigo} fue entregado con éxito. ¡Gracias por su preferencia!",
        "presupuestado": f"Hola {nombre}, su equipo {codigo} ya fue diagnosticado y tenemos un presupuesto listo.",
        "en_reparacion": f"Hola {nombre}, estamos trabajando en su equipo {codigo}. Pronto estará listo.",
    }

    return mensajes_estado.get(estado, f"Hola {nombre}, tenemos novedades sobre su equipo {codigo}.")
