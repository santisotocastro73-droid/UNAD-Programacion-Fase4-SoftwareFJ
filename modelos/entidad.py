# Importamos ABC y abstractmethod para definir clases y métodos abstractos
from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase abstracta base que representa cualquier entidad del sistema Software FJ."""

    def __init__(self, id_entidad: str):
        # Validamos que el identificador no esté vacío ni sea solo espacios
        if not id_entidad or not str(id_entidad).strip():
            raise ValueError("El ID de la entidad no puede estar vacío.")
        
        # Atributo protegido para aplicar encapsulación
        self._id = str(id_entidad).strip()
        # Registramos la fecha y hora exacta de creación de la entidad
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Getter para acceder de forma segura al ID de la entidad."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Getter para consultar cuándo se creó la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio que deberán implementar todas las clases hijas."""
        pass