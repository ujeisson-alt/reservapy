# reserva.py
# Modelo de datos: representa una reserva (turno) en el sistema ReservaPy.

from datetime import datetime

FORMATO_FECHA = "%d/%m/%Y"
FORMATO_HORA = "%H:%M"


class Reserva:
    """Representa una reserva en el sistema ReservaPy.

    Atributos:
        cliente (str): Nombre del cliente.
        fecha (str): Fecha en formato 'DD/MM/AAAA'.
        hora (str): Hora en formato 'HH:MM' (24 horas).
        servicio (str): Tipo de servicio reservado.
    """

    def __init__(self, cliente: str, fecha: str, hora: str, servicio: str):
        self.cliente = cliente.strip()
        self.fecha = fecha.strip()
        self.hora = hora.strip()
        self.servicio = servicio.strip()

    @property
    def fecha_hora(self) -> datetime:
        """Fecha y hora combinadas como datetime (útil para ordenar y comparar)."""
        return datetime.strptime(f"{self.fecha} {self.hora}", f"{FORMATO_FECHA} {FORMATO_HORA}")

    def coincide_con(self, cliente: str, fecha: str, hora: str) -> bool:
        """Indica si la reserva corresponde a ese cliente, fecha y hora.

        El nombre se compara sin distinguir mayúsculas ni espacios extra.
        """
        return (" ".join(self.cliente.lower().split()) == " ".join(cliente.lower().split())
                and self.fecha == fecha and self.hora == hora)

    def __str__(self) -> str:
        return f"{self.fecha} {self.hora} | {self.cliente:<25} | {self.servicio}"

    def __repr__(self) -> str:
        return (f"Reserva(cliente={self.cliente!r}, fecha={self.fecha!r}, "
                f"hora={self.hora!r}, servicio={self.servicio!r})")

    def to_dict(self) -> dict:
        """Convierte la reserva a diccionario (para guardar en CSV)."""
        return {
            "cliente": self.cliente,
            "fecha": self.fecha,
            "hora": self.hora,
            "servicio": self.servicio,
        }
