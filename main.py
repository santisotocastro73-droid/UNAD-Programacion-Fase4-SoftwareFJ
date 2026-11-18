# Importamos módulos estándar para manejo de rutas, sistema y registro de logs
import os
import logging
# Importamos las clases del modelo de Software FJ
from modelos.cliente import Cliente
from modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import Reserva
# Importamos las excepciones personalizadas del sistema
from excepciones.errores_sistema import (
    SoftwareFJError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
)


def configurar_logger() -> logging.Logger:
    """Configura y devuelve el logger que registra eventos y errores en archivo y consola."""
    # Aseguramos que la carpeta 'logs' exista antes de crear el archivo
    os.makedirs("logs", exist_ok=True)
    # Definimos la ruta del archivo de logs exigido por el Anexo 3
    ruta_log = os.path.join("logs", "eventos_software_fj.log")

    # Creamos la instancia principal del logger
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evitamos duplicar manejadores si la función se llama más de una vez
    if not logger.handlers:
        # Formato detallado con fecha, nivel del evento y mensaje
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        # Manejador para guardar los registros en el archivo .log con codificación UTF-8
        manejador_archivo = logging.FileHandler(ruta_log, encoding="utf-8")
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)

    return logger


def ejecutar_simulacion():
    """Ejecuta al menos 10 operaciones completas simulando casos válidos y errores controlados."""
    # Inicializamos el sistema de logs
    logger = configurar_logger()
    logger.info("=== INICIO DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ ===")
    print("=== SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ ===\n")

    # Listas internas en memoria (sin bases de datos, según requerimiento)
    clientes = []
    servicios = []
    reservas = []

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de Cliente 1 (uso de try / except / else)
    # -------------------------------------------------------------------------
    print("[Operación 1] Registrando cliente válido...")
    try:
        # Intentamos instanciar un cliente con todos sus datos correctos
        cliente_1 = Cliente("CLI-01", "Laura Mendoza", "laura.mendoza@correo.com", "3104567890")
    except ClienteInvalidoError as error:
        # Si falla la validación, registramos el error en el log
        logger.error(f"Operación 1 fallida: {error}")
        print(f"  -> Error: {error}")
    else:
        # El bloque 'else' se ejecuta únicamente si NO hubo excepciones
        clientes.append(cliente_1)
        logger.info(f"Operación 1 exitosa: {cliente_1.obtener_resumen()}")
        print(f"  -> Éxito: {cliente_1.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Registro válido de Cliente 2 (uso de try / except / else)
    # -------------------------------------------------------------------------
    print("\n[Operación 2] Registrando segundo cliente válido...")
    try:
        cliente_2 = Cliente("CLI-02", "Carlos Ramírez", "carlos.ramirez@empresa.co", "3209876543")
    except ClienteInvalidoError as error:
        logger.error(f"Operación 2 fallida: {error}")
        print(f"  -> Error: {error}")
    else:
        clientes.append(cliente_2)
        logger.info(f"Operación 2 exitosa: {cliente_2.obtener_resumen()}")
        print(f"  -> Éxito: {cliente_2.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Registro inválido de Cliente (correo sin '@' y teléfono corto)
    # -------------------------------------------------------------------------
    print("\n[Operación 3] Intentando registrar cliente con datos inválidos...")
    try:
        # Este registro debe lanzar ClienteInvalidoError encadenado desde ValueError
        cliente_invalido = Cliente("CLI-03", "Pedro", "pedrocorreo.com", "123")
        clientes.append(cliente_invalido)
    except ClienteInvalidoError as error:
        # Capturamos la excepción personalizada y mostramos también la causa original
        logger.error(f"Operación 3 controlada: {error} | Causa original: {error.__cause__}")
        print(f"  -> Excepción capturada correctamente: {error}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Creación válida de los 3 tipos de servicios (Polimorfismo)
    # -------------------------------------------------------------------------
    print("\n[Operación 4] Creando catálogo de servicios especializados...")
    try:
        # Creamos una instancia de cada clase derivada de Servicio
        sala_1 = ReservaSala("SRV-01", "Sala Ejecutiva Norte", 50000, capacidad=12)
        equipo_1 = AlquilerEquipo("SRV-02", "Workstation Dell Precision", 35000, gama="profesional")
        asesoria_1 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud", 90000, area_tecnica="Cloud & DevOps")
    except ServicioInvalidoError as error:
        logger.error(f"Operación 4 fallida: {error}")
        print(f"  -> Error: {error}")
    else:
        # Agregamos los tres servicios válidos a la lista interna
        servicios.extend([sala_1, equipo_1, asesoria_1])
        for srv in servicios:
            logger.info(f"Operación 4 - Servicio creado: {srv.obtener_resumen()}")
            print(f"  -> {srv.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Creación inválida de Servicio (tarifa negativa)
    # -------------------------------------------------------------------------
    print("\n[Operación 5] Intentando crear servicio con tarifa negativa...")
    try:
        # Intentamos crear una sala con tarifa menor o igual a cero
        sala_erronea = ReservaSala("SRV-99", "Sala Defectuosa", -15000, capacidad=5)
        servicios.append(sala_erronea)
    except ServicioInvalidoError as error:
        logger.error(f"Operación 5 controlada: {error} | Causa: {error.__cause__}")
        print(f"  -> Excepción capturada correctamente: {error}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Reserva exitosa de Sala usando sobrecarga por defecto
    # -------------------------------------------------------------------------
    print("\n[Operación 6] Procesando reserva exitosa de Sala (sin descuento)...")
    try:
        # Creamos la reserva de 4 horas para Laura Mendoza
        reserva_1 = Reserva("RES-01", clientes[0], servicios[0], horas=4)
        # Llamamos al método sobrecargado usando valores por defecto (descuento=0, impuesto=0.19)
        total_1 = reserva_1.procesar_y_confirmar()
    except SoftwareFJError as error:
        logger.error(f"Operación 6 fallida: {error}")
        print(f"  -> Error: {error}")
    else:
        reservas.append(reserva_1)
        logger.info(f"Operación 6 exitosa: {reserva_1.obtener_resumen()}")
        print(f"  -> Confirmada: {reserva_1.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Reserva exitosa de Equipo aplicando descuento (Sobrecarga)
    # -------------------------------------------------------------------------
    print("\n[Operación 7] Procesando reserva exitosa de Equipo con 10% de descuento...")
    try:
        # Creamos la reserva de 3 horas de equipo profesional para Carlos Ramírez
        reserva_2 = Reserva("RES-02", clientes[1], servicios[1], horas=3)
        # Sobrecarga de método: pasamos explícitamente descuento=0.10
        total_2 = reserva_2.procesar_y_confirmar(descuento=0.10)
    except SoftwareFJError as error:
        logger.error(f"Operación 7 fallida: {error}")
        print(f"  -> Error: {error}")
    else:
        reservas.append(reserva_2)
        logger.info(f"Operación 7 exitosa: {reserva_2.obtener_resumen()}")
        print(f"  -> Confirmada: {reserva_2.obtener_resumen()}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Intento de reserva fallida (Servicio ya ocupado/no disponible)
    # -------------------------------------------------------------------------
    print("\n[Operación 8] Intentando reservar una sala que ya fue ocupada...")
    try:
        # servicios[0] (Sala Ejecutiva Norte) quedó no disponible en la Operación 6
        reserva_3 = Reserva("RES-03", clientes[1], servicios[0], horas=2)
        reserva_3.procesar_y_confirmar()
    except ReservaInvalidaError as error:
        # Capturamos el encadenamiento desde ServicioNoDisponibleError
        logger.error(f"Operación 8 controlada: {error} | Causa: {error.__cause__}")
        print(f"  -> Excepción capturada correctamente: {error}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Intento de reserva fallida por duración inválida (1 hora equipo)
    # -------------------------------------------------------------------------
    print("\n[Operación 9] Intentando reservar equipo por menos del mínimo de horas...")
    try:
        # Creamos un nuevo equipo disponible pero pedimos 1 hora (el mínimo es 2 horas)
        equipo_2 = AlquilerEquipo("SRV-04", "Proyector 4K", 25000, gama="estandar")
        servicios.append(equipo_2)
        reserva_4 = Reserva("RES-04", clientes[0], equipo_2, horas=1)
        reserva_4.procesar_y_confirmar()
    except ReservaInvalidaError as error:
        logger.error(f"Operación 9 controlada: {error} | Causa: {error.__cause__}")
        print(f"  -> Excepción capturada correctamente: {error}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Cancelación de reserva y liberación de servicio (try/except/finally)
    # -------------------------------------------------------------------------
    print("\n[Operación 10] Cancelando reserva RES-01 y liberando la sala...")
    try:
        # Cancelamos la reserva 1 para liberar la Sala Ejecutiva Norte
        reservas[0].cancelar()
        logger.info(f"Operación 10 exitosa: {reservas[0].obtener_resumen()}")
        print(f"  -> Cancelada: {reservas[0].obtener_resumen()}")

        # Intentamos cancelar la misma reserva por segunda vez para probar la validación
        reservas[0].cancelar()
    except ReservaInvalidaError as error:
        logger.warning(f"Operación 10 - Doble cancelación bloqueada: {error}")
        print(f"  -> Validación de doble cancelación: {error}")
    finally:
        # El bloque 'finally' se ejecuta siempre, haya o no error, para cerrar el ciclo
        disponibilidad_sala = "Disponible" if servicios[0].disponible else "Ocupada"
        logger.info(f"Bloque finally ejecutado. Estado actual de {servicios[0].nombre}: {disponibilidad_sala}")
        print(f"  -> [Finally] Estado final de '{servicios[0].nombre}': {disponibilidad_sala}")

    # -------------------------------------------------------------------------
    # RESUMEN FINAL EN CONSOLA
    # -------------------------------------------------------------------------
    print("\n=== RESUMEN FINAL DE EJECUCIÓN ===")
    print(f"Clientes registrados en memoria : {len(clientes)}")
    print(f"Servicios creados en memoria    : {len(servicios)}")
    print(f"Reservas activas/registradas    : {len(reservas)}")
    print("Log de auditoría guardado en    : logs/eventos_software_fj.log")
    logger.info("=== FIN DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ ===")


# Punto de entrada principal del programa
if __name__ == "__main__":
    ejecutar_simulacion()