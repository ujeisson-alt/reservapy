# Análisis — ReservaPy

## Problema principal
Los pequeños negocios clientes de ReservaPy (centros de estética, consultorios,
estudios profesionales) gestionan sus turnos en papel, WhatsApp o notas sueltas.
Esto provoca turnos superpuestos, errores en fechas y horas, dificultad para
consultar la disponibilidad y pérdida de tiempo administrativo.

## ¿Qué es una reserva?
Un compromiso de atención de **un cliente**, en **una fecha y hora** concretas,
para **un tipo de servicio**.

| Atributo  | Tipo | Formato / regla                 |
|-----------|------|---------------------------------|
| cliente   | str  | No vacío                        |
| fecha     | str  | DD/MM/AAAA, fecha real, no pasada |
| hora      | str  | HH:MM (24 h)                    |
| servicio  | str  | No vacío                        |

## Conflictos de horario identificados
1. Dos clientes en la misma fecha y hora (superposición).
2. La misma hora escrita de dos formas (`9:00` vs `09:00`) que "esconde" un duplicado.
3. Fechas imposibles (`31/02/2026`) o con formato equivocado (`2026-02-10`).
4. Reservas creadas en fechas que ya pasaron.
5. Cancelar una reserva equivocada por coincidencia parcial del nombre.

## Reglas de negocio
- No pueden existir dos reservas para la misma fecha y hora.
- La fecha debe ser válida (DD/MM/AAAA) y no anterior a hoy.
- La hora debe estar en formato HH:MM (24 horas).
- El nombre del cliente y el servicio no pueden estar vacíos.
- Para cancelar se identifica la reserva por **cliente + fecha + hora**
  (el nombre se compara sin distinguir mayúsculas).
- Fechas y horas se **normalizan** (`9:00` → `09:00`) antes de comparar o guardar.

## Diseño — menú
```
=== SISTEMA DE RESERVAS – RESERVAPY ===
1. Crear reserva
2. Listar reservas
3. Buscar reservas por fecha
4. Cancelar reserva
5. Ver disponibilidad
6. Salir
Ingrese una opción:
```

## Pseudocódigo de disponibilidad
```
función verificar_disponibilidad(fecha, hora):
    para cada reserva en lista_reservas:
        si reserva.fecha == fecha Y reserva.hora == hora:
            retornar OCUPADO
    retornar DISPONIBLE
```

## Fuera de alcance (MVP)
Interfaz web/app, múltiples negocios, notificaciones, base de datos relacional,
autenticación y reportes.
