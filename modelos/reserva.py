from modelos.entidad import Entidad
from modelos.cliente import Cliente
from modelos.servicio import Servicio
from excepciones.errores_sistema import ReservaInvalidaError, SoftwareFJError


class Reserva(Entidad):
    """Clase que integra un Cliente y un Servicio, gestionando el ciclo de vida de la reserva."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int):
        try:
            # Llamamos al constructor de Entidad
            super().__init__(id_reserva)
            # Validamos que los objetos recibidos sean instancias válidas
            if not isinstance(cliente, Cliente):
                raise ValueError("Se requiere un objeto Cliente válido para la reserva.")
            if not isinstance(servicio, Servicio):
                raise ValueError("Se requiere un objeto Servicio válido para la reserva.")
            if not isinstance(horas, int) or horas <= 0:
                raise ValueError("La duración en horas debe ser un número entero mayor a 0.")

            self.__cliente = cliente
            self.__servicio = servicio
            self.__horas = horas
            self.__estado = "PENDIENTE"
            self.__costo_total = 0.0
        except ValueError as error_original:
            # Encadenamiento de excepciones
            raise ReservaInvalidaError(
                f"Error al inicializar la reserva '{id_reserva}': {error_original}"
            ) from error_original

    @property
    def estado(self) -> str:
        """Devuelve el estado actual de la reserva."""
        return self.__estado

    @property
    def costo_total(self) -> float:
        """Devuelve el costo total calculado de la reserva."""
        return self.__costo_total

    def procesar_y_confirmar(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Valida disponibilidad, calcula el costo sobrecargado y confirma la reserva.
        Marca el servicio como no disponible una vez confirmado.
        """
        if self.__estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva [{self._id}] ya está cancelada y no puede confirmarse.")
        if self.__estado == "CONFIRMADA":
            raise ReservaInvalidaError(f"La reserva [{self._id}] ya fue confirmada previamente.")

        try:
            # Ejecutamos el cálculo polimórfico del servicio (que a su vez valida disponibilidad y horas)
            self.__costo_total = self.__servicio.calcular_costo(self.__horas, descuento, impuesto)
            self.__estado = "CONFIRMADA"
            # Bloqueamos la disponibilidad del servicio porque ya quedó reservado
            self.__servicio.disponible = False
            return self.__costo_total
        except SoftwareFJError as error_servicio:
            # Encadenamos cualquier error del servicio hacia ReservaInvalidaError
            raise ReservaInvalidaError(
                f"No se pudo confirmar la reserva [{self._id}]: {error_servicio}"
            ) from error_servicio

    def cancelar(self) -> None:
        """Cancela la reserva y libera nuevamente el servicio si estaba confirmada."""
        if self.__estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva [{self._id}] ya se encuentra cancelada.")

        # Si estaba confirmada, devolvemos el servicio a estado disponible
        if self.__estado == "CONFIRMADA":
            self.__servicio.disponible = True

        self.__estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        """Implementación del método abstracto de Entidad."""
        return (
            f"Reserva [{self._id}] | Estado: {self.__estado} | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} ({self.__horas}h) | Total: ${self.__costo_total:,.2f}"
        )