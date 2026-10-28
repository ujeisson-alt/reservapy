# utils.py
# Funciones de utilidad: persistencia en CSV y validaciones de formato.

import csv
import os
from datetime import datetime, date

from reserva import Reserva, FORMATO_FECHA, FORMATO_HORA

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(DIRECTORIO_BASE, "data", "reservas.csv")
CAMPOS = ["cliente", "fecha", "hora", "servicio"]


# ----------------------------------------------------------------------
# Persistencia
# ----------------------------------------------------------------------
def guardar_reservas(reservas, ruta: str = ARCHIVO_CSV) -> bool:
    """Guarda todas las reservas en el CSV (sobrescribe). Retorna True si tuvo éxito."""
    try:
        os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS)
            writer.writeheader()
            for r in reservas:
                writer.writerow(r.to_dict())
        return True
    except OSError as e:
        print(f"Error al guardar reservas: {e}")
        return False


def cargar_reservas(ruta: str = ARCHIVO_CSV) -> list:
    """Carga las reservas desde el CSV. Omite (e informa) filas inválidas."""
    reservas = []
    if not os.path.exists(ruta):
        return reservas  # primera ejecución: todavía no hay archivo
    try:
        with open(ruta, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for numero_fila, row in enumerate(reader, start=2):
                try:
                    fecha = normalizar_fecha(row["fecha"])
                    hora = normalizar_hora(row["hora"])
                    if not row["cliente"].strip():
                        raise ValueError("cliente vacío")
                    reservas.append(Reserva(row["cliente"], fecha, hora, row["servicio"]))
                except (ValueError, KeyError, AttributeError) as e:
                    print(f"Aviso: fila {numero_fila} del CSV omitida ({e}).")
    except OSError as e:
        print(f"Error al cargar reservas: {e}")
    return reservas


# ----------------------------------------------------------------------
# Validaciones
# ----------------------------------------------------------------------
def validar_fecha(fecha_str: str) -> bool:
    """Valida que la fecha tenga formato DD/MM/AAAA y exista en el calendario."""
    try:
        datetime.strptime(fecha_str.strip(), FORMATO_FECHA)
        return True
    except ValueError:
        return False


def validar_hora(hora_str: str) -> bool:
    """Valida que la hora tenga formato HH:MM (24 horas)."""
    try:
        datetime.strptime(hora_str.strip(), FORMATO_HORA)
        return True
    except ValueError:
        return False


def normalizar_fecha(fecha_str: str) -> str:
    """Convierte '5/3/2026' en '05/03/2026'. Lanza ValueError si es inválida.

    Normalizar evita que la misma fecha escrita de dos formas distintas
    permita crear turnos superpuestos.
    """
    return datetime.strptime(fecha_str.strip(), FORMATO_FECHA).strftime(FORMATO_FECHA)


def normalizar_hora(hora_str: str) -> str:
    """Convierte '9:30' en '09:30'. Lanza ValueError si es inválida."""
    return datetime.strptime(hora_str.strip(), FORMATO_HORA).strftime(FORMATO_HORA)


def es_fecha_pasada(fecha_str: str, hoy: date = None) -> bool:
    """Indica si la fecha (DD/MM/AAAA) es anterior a hoy."""
    hoy = hoy or date.today()
    return datetime.strptime(fecha_str, FORMATO_FECHA).date() < hoy
