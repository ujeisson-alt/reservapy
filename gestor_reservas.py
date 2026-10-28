# gestor_reservas.py
# Lógica de negocio: crear, listar, buscar, cancelar y verificar disponibilidad.

from datetime import datetime, timedelta
from typing import List, Tuple

from reserva import Reserva, FORMATO_HORA
from utils import (ARCHIVO_CSV, cargar_reservas, guardar_reservas,
                   normalizar_fecha, normalizar_hora, es_fecha_pasada)

# Horario de atención usado para mostrar la grilla de disponibilidad.
HORA_APERTURA = "09:00"
HORA_CIERRE = "18:00"
DURACION_TURNO_MIN = 30


class GestorReservas:
    """Gestiona la colección de reservas y su persistencia en CSV."""

    def __init__(self, ruta_csv: str = ARCHIVO_CSV, cargar: bool = True):
        self.ruta_csv = ruta_csv
        self.reservas: List[Reserva] = cargar_reservas(ruta_csv) if cargar else []

    def _guardar(self) -> None:
        """Persiste el estado actual. Se llama tras cada modificación."""
        guardar_reservas(self.reservas, self.ruta_csv)

    def agregar_reserva(self, cliente: str, fecha: str, hora: str,
                        servicio: str, permitir_pasado: bool = False) -> Tuple[bool, str]:
        """Crea una reserva si los datos son válidos y el horario está libre."""
        if not cliente.strip():
            return False, "El nombre del cliente no puede estar vacío."
        if not servicio.strip():
            return False, "El tipo de servicio no puede estar vacío."
        try:
            fecha = normalizar_fecha(fecha)
        except ValueError:
            return False, "Formato de fecha inválido. Use DD/MM/AAAA."
        try:
            hora = normalizar_hora(hora)
        except ValueError:
            return False, "Formato de hora inválido. Use HH:MM (24 horas)."
        if not permitir_pasado and es_fecha_pasada(fecha):
            return False, "No se pueden crear reservas en fechas pasadas."
        if not self.verificar_disponibilidad(fecha, hora):
            return False, f"Horario no disponible: ya existe una reserva el {fecha} a las {hora}."

        self.reservas.append(Reserva(cliente, fecha, hora, servicio))
        self._guardar()
        return True, "Reserva creada exitosamente."

    def listar_reservas(self) -> List[Reserva]:
        """Retorna todas las reservas ordenadas cronológicamente."""
        return sorted(self.reservas, key=lambda r: r.fecha_hora)

    def buscar_por_fecha(self, fecha: str) -> List[Reserva]:
        """Retorna las reservas de una fecha, ordenadas por hora."""
        try:
            fecha = normalizar_fecha(fecha)
        except ValueError:
            return []
        return sorted((r for r in self.reservas if r.fecha == fecha), key=lambda r: r.hora)

    def cancelar_reserva(self, cliente: str, fecha: str, hora: str) -> Tuple[bool, str]:
        """Cancela la reserva identificada por cliente + fecha + hora."""
        try:
            fecha, hora = normalizar_fecha(fecha), normalizar_hora(hora)
        except ValueError:
            return False, "Fecha u hora con formato inválido."
        for i, r in enumerate(self.reservas):
            if r.coincide_con(cliente, fecha, hora):
                self.reservas.pop(i)
                self._guardar()
                return True, "Reserva cancelada."
        return False, f"No se encontró una reserva de '{cliente}' el {fecha} a las {hora}."

    def verificar_disponibilidad(self, fecha: str, hora: str) -> bool:
        """Un horario está libre si NO existe otra reserva con la misma fecha y hora."""
        try:
            fecha, hora = normalizar_fecha(fecha), normalizar_hora(hora)
        except ValueError:
            return False
        return not any(r.fecha == fecha and r.hora == hora for r in self.reservas)

    def disponibilidad_del_dia(self, fecha: str) -> List[Tuple[str, bool]]:
        """Grilla de turnos del horario de atención: [(hora, libre), ...]."""
        fecha = normalizar_fecha(fecha)
        ocupadas = {r.hora for r in self.reservas if r.fecha == fecha}
        actual = datetime.strptime(HORA_APERTURA, FORMATO_HORA)
        cierre = datetime.strptime(HORA_CIERRE, FORMATO_HORA)
        grilla = []
        while actual < cierre:
            hora = actual.strftime(FORMATO_HORA)
            grilla.append((hora, hora not in ocupadas))
            actual += timedelta(minutes=DURACION_TURNO_MIN)
        return grilla
