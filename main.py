# main.py
# Interfaz de usuario por consola del sistema ReservaPy.

from gestor_reservas import GestorReservas
from utils import validar_fecha, validar_hora

SEPARADOR = "-" * 60


def mostrar_menu() -> None:
    """Muestra el menú principal."""
    print("\n=== SISTEMA DE RESERVAS – RESERVAPY ===")
    print("1. Crear reserva")
    print("2. Listar reservas")
    print("3. Buscar reservas por fecha")
    print("4. Cancelar reserva")
    print("5. Ver disponibilidad")
    print("6. Salir")


def pedir_texto(mensaje: str) -> str:
    """Pide un texto no vacío; retorna None si el usuario lo deja vacío."""
    texto = input(mensaje).strip()
    if not texto:
        print("✗ Este campo no puede estar vacío.")
        return None
    return texto


def pedir_fecha() -> str:
    fecha = input("Fecha (DD/MM/AAAA): ").strip()
    if not validar_fecha(fecha):
        print("✗ Formato de fecha inválido. Use DD/MM/AAAA (ej: 25/03/2026).")
        return None
    return fecha


def pedir_hora() -> str:
    hora = input("Hora (HH:MM): ").strip()
    if not validar_hora(hora):
        print("✗ Formato de hora inválido. Use HH:MM en 24 horas (ej: 14:30).")
        return None
    return hora


def imprimir_reservas(reservas, titulo: str) -> None:
    if not reservas:
        print("No hay reservas para mostrar.")
        return
    print(f"\n{titulo} ({len(reservas)})")
    print(SEPARADOR)
    for r in reservas:
        print(r)
    print(SEPARADOR)


def crear_reserva(gestor: GestorReservas) -> None:
    print("\n-- Crear reserva --")
    cliente = pedir_texto("Ingrese nombre del cliente: ")
    if cliente is None:
        return
    fecha = pedir_fecha()
    if fecha is None:
        return
    hora = pedir_hora()
    if hora is None:
        return
    servicio = pedir_texto("Ingrese tipo de servicio: ")
    if servicio is None:
        return
    ok, msg = gestor.agregar_reserva(cliente, fecha, hora, servicio)
    print(("✓ " if ok else "✗ ") + msg)


def listar_reservas(gestor: GestorReservas) -> None:
    imprimir_reservas(gestor.listar_reservas(), "Reservas registradas")


def buscar_por_fecha(gestor: GestorReservas) -> None:
    fecha = pedir_fecha()
    if fecha is None:
        return
    imprimir_reservas(gestor.buscar_por_fecha(fecha), f"Reservas del {fecha}")


def cancelar_reserva(gestor: GestorReservas) -> None:
    print("\n-- Cancelar reserva --")
    cliente = pedir_texto("Nombre del cliente: ")
    if cliente is None:
        return
    fecha = pedir_fecha()
    if fecha is None:
        return
    hora = pedir_hora()
    if hora is None:
        return
    confirmacion = input(f"¿Cancelar la reserva de {cliente} el {fecha} a las {hora}? (s/n): ")
    if confirmacion.strip().lower() not in ("s", "si", "sí"):
        print("Operación cancelada.")
        return
    ok, msg = gestor.cancelar_reserva(cliente, fecha, hora)
    print(("✓ " if ok else "✗ ") + msg)


def ver_disponibilidad(gestor: GestorReservas) -> None:
    fecha = pedir_fecha()
    if fecha is None:
        return
    print(f"\nDisponibilidad del {fecha}")
    print(SEPARADOR)
    grilla = gestor.disponibilidad_del_dia(fecha)
    for hora, libre in grilla:
        print(f"  {hora}  {'🟢 Libre' if libre else '🔴 Ocupado'}")
    print(SEPARADOR)
    libres = sum(1 for _, libre in grilla if libre)
    print(f"{libres} de {len(grilla)} turnos libres.")
    # Reservas fuera de la grilla estándar (ej: 10:15) también se informan
    fuera = [r for r in gestor.buscar_por_fecha(fecha) if r.hora not in dict(grilla)]
    for r in fuera:
        print(f"  Además ocupado fuera de grilla: {r.hora}")


ACCIONES = {
    "1": crear_reserva,
    "2": listar_reservas,
    "3": buscar_por_fecha,
    "4": cancelar_reserva,
    "5": ver_disponibilidad,
}


def main() -> None:
    gestor = GestorReservas()
    print(f"ReservaPy iniciado. {len(gestor.reservas)} reservas cargadas.")
    while True:
        try:
            mostrar_menu()
            opcion = input("Ingrese una opción: ").strip()
            if opcion == "6":
                print("¡Hasta luego!")
                break
            accion = ACCIONES.get(opcion)
            if accion:
                accion(gestor)
            else:
                print("✗ Opción inválida. Ingrese un número del 1 al 6.")
        except KeyboardInterrupt:
            print("\nOperación cancelada. Volviendo al menú...")
        except EOFError:
            print("\n¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
