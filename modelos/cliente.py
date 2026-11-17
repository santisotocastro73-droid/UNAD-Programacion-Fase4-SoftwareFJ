from modelos.entidad import Entidad
from excepciones.errores_sistema import ClienteInvalidoError


class Cliente(Entidad):
    """Clase que representa a un cliente de Software FJ con validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        try:
            # Llamamos al constructor de la clase abstracta Entidad
            super().__init__(id_cliente)
            # Usamos los setters para validar cada dato desde el momento de creación
            self.nombre = nombre
            self.correo = correo
            self.telefono = telefono
        except ValueError as error_original:
            # Encadenamiento de excepciones: atrapamos ValueError y lanzamos ClienteInvalidoError
            raise ClienteInvalidoError(
                f"No se pudo registrar el cliente con ID '{id_cliente}': {error_original}"
            ) from error_original

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Valida y asigna el nombre del cliente."""
        if not valor or len(valor.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        """Devuelve el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        """Valida que el correo tenga formato básico válido."""
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Devuelve el número de teléfono del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Valida que el teléfono contenga solo dígitos y tenga longitud adecuada."""
        telefono_limpio = str(valor).strip()
        if not telefono_limpio.isdigit() or len(telefono_limpio) < 7:
            raise ValueError(f"El teléfono '{valor}' debe contener al menos 7 dígitos numéricos.")
        self.__telefono = telefono_limpio

    def obtener_resumen(self) -> str:
        """Implementación del método abstracto de la clase Entidad."""
        return f"Cliente [{self._id}] - {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"