import io
import os
import tempfile
import unittest
from unittest.mock import patch

import computadores


class TestComputadoresModule(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.original_data_file = computadores.DATA_FILE
        computadores.DATA_FILE = os.path.join(self.tempdir.name, "computadoras.json")

    def tearDown(self):
        computadores.DATA_FILE = self.original_data_file
        self.tempdir.cleanup()

    def test_cargar_datos_sin_archivo_retorna_estructura_vacia(self):
        self.assertFalse(os.path.exists(computadores.DATA_FILE))
        result = computadores.cargar_datos()
        self.assertEqual(result, {"computadores": [], "ultimo_id": 0})

    def test_cargar_datos_json_invalido_retorna_estructura_vacia(self):
        with open(computadores.DATA_FILE, "w", encoding="utf-8") as file:
            file.write("not valid json")

        result = computadores.cargar_datos()
        self.assertEqual(result, {"computadores": [], "ultimo_id": 0})

    @patch("builtins.input", return_value="2")
    def test_seleccionar_estado_opcion_valida_retorna_estado(self, mock_input):
        self.assertEqual(computadores.seleccionar_estado(), "Ocupado")

    @patch("builtins.input", return_value="0")
    def test_seleccionar_estado_opcion_invalida_retorna_none(self, mock_input):
        self.assertIsNone(computadores.seleccionar_estado())

    @patch("builtins.input", side_effect=["100", "Dell", "Latitude", "1"])
    def test_registrar_computador_valido_crea_registro(self, mock_input):
        with patch("sys.stdout", new=io.StringIO()):
            computadores.registrar_computador()

        data = computadores.cargar_datos()
        self.assertEqual(data["ultimo_id"], 1)
        self.assertEqual(len(data["computadores"]), 1)
        equipo = data["computadores"][0]
        self.assertEqual(equipo["inventario"], 100)
        self.assertEqual(equipo["marca"], "Dell")
        self.assertEqual(equipo["modelo"], "Latitude")
        self.assertEqual(equipo["estado"], "Disponible")

    @patch("builtins.input", side_effect=["-5", "Dell", "Latitude", "1"])
    def test_registrar_computador_inventario_negativo_no_guarda(self, mock_input):
        with patch("sys.stdout", new=io.StringIO()) as fake_output:
            computadores.registrar_computador()

        self.assertIn("El número de inventario debe ser un entero positivo", fake_output.getvalue())
        self.assertEqual(computadores.cargar_datos()["computadores"], [])

    def test_actualizar_computador_datos_validos_actualiza_registro(self):
        data = {"computadores": [{"id": 1, "inventario": 100, "marca": "Dell", "modelo": "Latitude", "estado": "Disponible"}], "ultimo_id": 1}
        computadores.guardar_datos(data)

        with patch("builtins.input", side_effect=["1", "HP", "EliteBook", "2"]):
            with patch("sys.stdout", new=io.StringIO()):
                computadores.actualizar_computador()

        updated = computadores.cargar_datos()["computadores"][0]
        self.assertEqual(updated["marca"], "HP")
        self.assertEqual(updated["modelo"], "EliteBook")
        self.assertEqual(updated["estado"], "Ocupado")

    def test_actualizar_computador_estado_invalido_preserva_estado_anterior(self):
        data = {"computadores": [{"id": 1, "inventario": 100, "marca": "Dell", "modelo": "Latitude", "estado": "Disponible"}], "ultimo_id": 1}
        computadores.guardar_datos(data)

        with patch("builtins.input", side_effect=["1", "", "", "0"]):
            with patch("sys.stdout", new=io.StringIO()) as fake_output:
                computadores.actualizar_computador()

        updated = computadores.cargar_datos()["computadores"][0]
        self.assertEqual(updated["estado"], "Disponible")
        self.assertNotIn("ID no encontrado", fake_output.getvalue())
        self.assertIn("Equipo actualizado correctamente", fake_output.getvalue())

    def test_eliminar_computador_id_existente_elimina_registro(self):
        data = {"computadores": [{"id": 1, "inventario": 100, "marca": "Dell", "modelo": "Latitude", "estado": "Disponible"}], "ultimo_id": 1}
        computadores.guardar_datos(data)

        with patch("builtins.input", return_value="1"):
            with patch("sys.stdout", new=io.StringIO()):
                computadores.eliminar_computador()

        self.assertEqual(computadores.cargar_datos()["computadores"], [])

    def test_eliminar_computador_id_no_encontrado_no_cambia_datos(self):
        data = {"computadores": [{"id": 1, "inventario": 100, "marca": "Dell", "modelo": "Latitude", "estado": "Disponible"}], "ultimo_id": 1}
        computadores.guardar_datos(data)

        with patch("builtins.input", return_value="99"):
            with patch("sys.stdout", new=io.StringIO()) as fake_output:
                computadores.eliminar_computador()

        self.assertIn("ID no encontrado", fake_output.getvalue())
        self.assertEqual(len(computadores.cargar_datos()["computadores"]), 1)

    def test_listar_computadores_sin_registros_muestra_mensaje(self):
        computadores.guardar_datos({"computadores": [], "ultimo_id": 0})
        with patch("sys.stdout", new=io.StringIO()) as fake_output:
            computadores.listar_computadores()

        self.assertIn("No hay equipos registrados", fake_output.getvalue())


if __name__ == "__main__":
    unittest.main()
