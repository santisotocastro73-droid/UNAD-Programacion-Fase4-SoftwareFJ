# Módulo de excepciones personalizadas para el sistema de Software FJ

class SoftwareFJError(Exception):
    """Clase base para todas las excepciones personalizadas del sistema."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de creación o cálculo de un servicio son incorrectos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando ocurre un error en la creación, confirmación o cancelación de una reserva."""
    pass