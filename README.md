# 📅 ReservaPy — Sistema de Reservas

> Sistema de gestión de turnos por consola para pequeños negocios.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-unittest-green)
![Dependencias](https://img.shields.io/badge/dependencias-ninguna-lightgrey)

## Descripción
Aplicación Python que permite **crear, listar, buscar y cancelar reservas**, validando
que no existan turnos superpuestos y guardando todo en un archivo CSV. Reemplaza la
agenda en papel / WhatsApp de centros de estética, consultorios y estudios profesionales.

## Funcionalidades
- ➕ Crear reservas (cliente, fecha, hora y servicio)
- 📋 Listar todas las reservas en orden cronológico
- 🔍 Buscar reservas por fecha
- ❌ Cancelar reservas (cliente + fecha + hora, con confirmación)
- 🟢 Ver disponibilidad del día en una grilla de turnos de 30 min (09:00–18:00)
- 🚫 Validación de conflictos: no se permiten dos reservas en la misma fecha y hora
- ✅ Validación de formato: fecha `DD/MM/AAAA` real y no pasada, hora `HH:MM` 24 h
- 💾 Persistencia automática en `data/reservas.csv`
- 🛡️ Manejo de errores: entradas inválidas, filas corruptas en el CSV, Ctrl+C

## Tecnologías
- Python 3.10+
- Módulos estándar: `csv`, `datetime`, `os`, `unittest`
- Programación Orientada a Objetos

## Instalación
```bash
git clone https://github.com/ujeisson-alt/reservapy.git
cd reservapy
python main.py
```

## Uso
Ejecutar `python main.py` y seguir el menú interactivo:
```
=== SISTEMA DE RESERVAS – RESERVAPY ===
1. Crear reserva
2. Listar reservas
3. Buscar reservas por fecha
4. Cancelar reserva
5. Ver disponibilidad
6. Salir
Ingrese una opción: 1

-- Crear reserva --
Ingrese nombre del cliente: Carlos Ruiz
Fecha (DD/MM/AAAA): 15/12/2026
Hora (HH:MM): 14:30
Ingrese tipo de servicio: Corte
✗ Horario no disponible: ya existe una reserva el 15/12/2026 a las 14:30.
```

## Pruebas
```bash
python -m unittest discover -s tests -v
```
Cubren validaciones, duplicados (incluso con formatos distintos como `9:00`/`09:00`),
fechas pasadas, búsqueda, cancelación, disponibilidad y persistencia.

## Estructura del proyecto
```
reservapy/
├── main.py              # Menú e interfaz de usuario
├── gestor_reservas.py   # Lógica de negocio (GestorReservas)
├── reserva.py           # Modelo de datos (Reserva)
├── utils.py             # Persistencia CSV y validaciones
├── data/
│   └── reservas.csv     # Datos persistidos
├── tests/
│   └── test_reservas.py # Pruebas unitarias
└── analisis.md          # Análisis, reglas de negocio y diseño
```

## Arquitectura
```
main.py (presentación) ──▶ gestor_reservas.py (negocio) ──▶ reserva.py (modelo)
                                      │
                                      ▼
                           utils.py ──▶ data/reservas.csv (persistencia)
```

## Autor
**Jeisson Uribe** — [GitHub](https://github.com/ujeisson-alt) · [LinkedIn](https://linkedin.com/in/jeisson-uribe-qa-data)
