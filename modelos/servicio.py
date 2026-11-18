from abc import abstractmethod
from modelos.entidad import Entidad
from excepciones.errores_sistema import ServicioInvalidoError, ServicioNoDisponibleError


class Servicio(Entidad):
    """Clase abstracta que representa un servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        try:
            # Llamamos al constructor de Entidad para validar y asignar el ID
            super().__init__(id_servicio)
            # Validamos el nombre del servicio
            if not nombre or len(nombre.strip()) < 3:
                raise ValueError("El nombre del servicio debe tener al menos 3 caracteres.")
            # Validamos que la tarifa por hora sea positiva
            if tarifa_hora <= 0:
                raise ValueError("La tarifa por hora debe ser mayor a cero.")

            self._nombre = nombre.strip()
            self._tarifa_hora = float(tarifa_hora)
            self._disponible = bool(disponible)
        except ValueError as error_original:
            # Encadenamiento de excepciones exigido en el Anexo 3
            raise ServicioInvalidoError(
                f"Error al crear el servicio '{id_servicio}': {error_original}"
            ) from error_original

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        """Devuelve la tarifa base por hora."""
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para reservar."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        """Permite cambiar la disponibilidad del servicio."""
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, horas: int) -> None:
        """Método abstracto para validar reglas específicas de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Método abstracto sobrecargado mediante parámetros opcionales (descuento e impuesto)
        para calcular el costo total del servicio.
        """
        pass

    def obtener_resumen(self) -> str:
        """Implementación base del resumen de servicio."""
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio [{self._id}] {self._nombre} (${self._tarifa_hora:,.2f}/h) - {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser mayor a 0 personas.")
        self.__capacidad = capacidad

    def validar_parametros(self, horas: int) -> None:
        """Valida disponibilidad y que la reserva de sala sea de mínimo 1 y máximo 12 horas."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La sala '{self._nombre}' no se encuentra disponible.")
        if horas < 1 or horas > 12:
            raise ServicioInvalidoError("Las salas solo se reservan entre 1 y 12 horas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el costo aplicando un recargo fijo de limpieza ($20,000), descuento e IVA."""
        self.validar_parametros(horas)
        subtotal = (self._tarifa_hora * horas) + 20000
        con_descuento = subtotal * (1 - descuento)
        return round(con_descuento * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        """Polimorfismo: sobrescribe el resumen agregando la capacidad de la sala."""
        return f"{super().obtener_resumen()} | Tipo: Sala (Capacidad: {self.__capacidad} personas)"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos (portátiles, proyectores, etc.)."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, gama: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if gama.lower() not in ["estandar", "profesional"]:
            raise ServicioInvalidoError("La gama del equipo debe ser 'estandar' o 'profesional'.")
        self.__gama = gama.lower()

    def validar_parametros(self, horas: int) -> None:
        """Valida disponibilidad y mínimo de 2 horas para alquiler de equipos."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self._nombre}' está actualmente alquilado.")
        if horas < 2:
            raise ServicioInvalidoError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el costo con recargo del 10% si es gama profesional, más descuento e IVA."""
        self.validar_parametros(horas)
        factor_gama = 1.10 if self.__gama == "profesional" else 1.0
        subtotal = (self._tarifa_hora * horas) * factor_gama
        con_descuento = subtotal * (1 - descuento)
        return round(con_descuento * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        """Polimorfismo: sobrescribe el resumen mostrando la gama del equipo."""
        return f"{super().obtener_resumen()} | Tipo: Equipo ({self.__gama.capitalize()})"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o desarrollo a medida."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, area_tecnica: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not area_tecnica or not area_tecnica.strip():
            raise ServicioInvalidoError("Debe especificar el área técnica de la asesoría.")
        self.__area_tecnica = area_tecnica.strip()

    def validar_parametros(self, horas: int) -> None:
        """Valida disponibilidad y horas positivas para la asesoría."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El consultor para '{self._nombre}' no tiene agenda disponible.")
        if horas <= 0:
            raise ServicioInvalidoError("La asesoría debe durar al menos 1 hora.")

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        """Calcula el costo de la asesoría aplicando descuento e IVA."""
        self.validar_parametros(horas)
        subtotal = self._tarifa_hora * horas
        con_descuento = subtotal * (1 - descuento)
        return round(con_descuento * (1 + impuesto), 2)

    def obtener_resumen(self) -> str:
        """Polimorfismo: sobrescribe el resumen incluyendo el área técnica."""
        return f"{super().obtener_resumen()} | Tipo: Asesoría ({self.__area_tecnica})"