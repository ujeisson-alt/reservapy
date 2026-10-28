# tests/test_reservas.py
# Pruebas unitarias de ReservaPy.
# Ejecutar desde la raíz del proyecto:  python -m unittest discover -s tests -v

import os
import sys
import tempfile
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gestor_reservas import GestorReservas  # noqa: E402
from utils import validar_fecha, validar_hora, normalizar_hora, normalizar_fecha  # noqa: E402

# Usamos una fecha futura dinámica para que las pruebas no caduquen.
MANANA = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
PASADO_MANANA = (date.today() + timedelta(days=2)).strftime("%d/%m/%Y")
AYER = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")


class TestValidaciones(unittest.TestCase):

    def test_validar_fecha(self):
        self.assertTrue(validar_fecha("25/03/2026"))
        self.assertFalse(validar_fecha("2026-03-25"))
        self.assertFalse(validar_fecha("31/02/2026"))  # no existe
        self.assertFalse(validar_fecha("abc"))

    def test_validar_hora(self):
        self.assertTrue(validar_hora("14:30"))
        self.assertFalse(validar_hora("25:00"))
        self.assertFalse(validar_hora("2pm"))

    def test_normalizacion(self):
        self.assertEqual(normalizar_hora("9:05"), "09:05")
        self.assertEqual(normalizar_fecha("5/3/2026"), "05/03/2026")


class TestGestorReservas(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self.tmp.name, "data", "reservas.csv")
        self.gestor = GestorReservas(ruta_csv=self.ruta)

    def tearDown(self):
        self.tmp.cleanup()

    def test_crear_reserva_valida(self):
        ok, _ = self.gestor.agregar_reserva("María", MANANA, "14:30", "Corte")
        self.assertTrue(ok)
        self.assertEqual(len(self.gestor.listar_reservas()), 1)

    def test_no_permite_horario_duplicado(self):
        self.gestor.agregar_reserva("María", MANANA, "14:30", "Corte")
        ok, msg = self.gestor.agregar_reserva("Juan", MANANA, "14:30", "Consulta")
        self.assertFalse(ok)
        self.assertIn("no disponible", msg)

    def test_duplicado_detectado_aunque_cambie_el_formato(self):
        self.gestor.agregar_reserva("María", MANANA, "09:00", "Corte")
        ok, _ = self.gestor.agregar_reserva("Juan", MANANA, "9:00", "Consulta")
        self.assertFalse(ok)

    def test_misma_hora_otro_dia_si_se_permite(self):
        self.gestor.agregar_reserva("María", MANANA, "14:30", "Corte")
        ok, _ = self.gestor.agregar_reserva("Juan", PASADO_MANANA, "14:30", "Consulta")
        self.assertTrue(ok)

    def test_rechaza_datos_invalidos(self):
        self.assertFalse(self.gestor.agregar_reserva("", MANANA, "10:00", "X")[0])
        self.assertFalse(self.gestor.agregar_reserva("Ana", "2026-01-01", "10:00", "X")[0])
        self.assertFalse(self.gestor.agregar_reserva("Ana", MANANA, "10.00", "X")[0])
        self.assertFalse(self.gestor.agregar_reserva("Ana", MANANA, "10:00", " ")[0])

    def test_rechaza_fecha_pasada(self):
        ok, msg = self.gestor.agregar_reserva("Ana", AYER, "10:00", "Manicura")
        self.assertFalse(ok)
        self.assertIn("pasadas", msg)

    def test_buscar_por_fecha(self):
        self.gestor.agregar_reserva("María", MANANA, "16:00", "Corte")
        self.gestor.agregar_reserva("Juan", MANANA, "10:00", "Consulta")
        self.gestor.agregar_reserva("Ana", PASADO_MANANA, "10:00", "Manicura")
        resultado = self.gestor.buscar_por_fecha(MANANA)
        self.assertEqual([r.hora for r in resultado], ["10:00", "16:00"])

    def test_cancelar_reserva(self):
        self.gestor.agregar_reserva("María García", MANANA, "14:30", "Corte")
        ok, _ = self.gestor.cancelar_reserva("maría  garcía", MANANA, "14:30")
        self.assertTrue(ok)
        self.assertEqual(self.gestor.listar_reservas(), [])

    def test_cancelar_inexistente(self):
        ok, _ = self.gestor.cancelar_reserva("Nadie", MANANA, "14:30")
        self.assertFalse(ok)

    def test_disponibilidad_del_dia(self):
        self.gestor.agregar_reserva("María", MANANA, "09:30", "Corte")
        grilla = dict(self.gestor.disponibilidad_del_dia(MANANA))
        self.assertTrue(grilla["09:00"])
        self.assertFalse(grilla["09:30"])

    def test_persistencia(self):
        self.gestor.agregar_reserva("María", MANANA, "14:30", "Corte")
        self.gestor.agregar_reserva("Juan", MANANA, "15:00", "Consulta")
        self.gestor.cancelar_reserva("Juan", MANANA, "15:00")
        recargado = GestorReservas(ruta_csv=self.ruta)
        self.assertEqual(len(recargado.reservas), 1)
        self.assertEqual(recargado.reservas[0].cliente, "María")

    def test_csv_con_fila_corrupta(self):
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("cliente,fecha,hora,servicio\n"
                    f"Ana,{MANANA},10:00,Manicura\n"
                    "Malo,99/99/9999,10:00,X\n")
        self.assertEqual(len(GestorReservas(ruta_csv=self.ruta).reservas), 1)


if __name__ == "__main__":
    unittest.main()
