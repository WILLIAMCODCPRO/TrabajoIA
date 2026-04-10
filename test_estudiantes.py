import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import estudiantes


class TestEstudiantesModule(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.original_data_file = estudiantes.DATA_FILE
        estudiantes.DATA_FILE = os.path.join(self.tempdir.name, "campers.json")

    def tearDown(self):
        estudiantes.DATA_FILE = self.original_data_file
        self.tempdir.cleanup()

    def test_cargar_datos_sin_archivo_retorna_estructura_vacia(self):
        self.assertFalse(os.path.exists(estudiantes.DATA_FILE))
        result = estudiantes.cargar_datos()
        self.assertEqual(result, {"campers": [], "ultimo_id": 0})

    def test_cargar_datos_json_invalido_retorna_estructura_vacia(self):
        with open(estudiantes.DATA_FILE, "w", encoding="utf-8") as file:
            file.write("{ not valid json }")

        result = estudiantes.cargar_datos()
        self.assertEqual(result, {"campers": [], "ultimo_id": 0})

    def test_validar_email_valido_retorna_true(self):
        self.assertTrue(estudiantes.validar_email("usuario@dominio.com"))

    def test_validar_email_invalido_retorna_false(self):
        self.assertFalse(estudiantes.validar_email("usuario@@dominio"))

    @patch("builtins.input", side_effect=["Juan Pérez", "12345", "juan@ejemplo.com"])
    def test_registrar_camper_valido_crea_registro(self, mock_input):
        with patch("sys.stdout", new=io.StringIO()):
            estudiantes.registrar_camper()

        data = estudiantes.cargar_datos()
        self.assertEqual(data["ultimo_id"], 1)
        self.assertEqual(len(data["campers"]), 1)
        camper = data["campers"][0]
        self.assertEqual(camper["nombre"], "Juan Pérez")
        self.assertEqual(camper["documento"], "12345")
        self.assertEqual(camper["email"], "juan@ejemplo.com")
        self.assertEqual(camper["estado"], "Activo")

    @patch("builtins.input", side_effect=["", "12345", "juan@ejemplo.com"])
    def test_registrar_camper_campos_vacios_no_guarda(self, mock_input):
        with patch("sys.stdout", new=io.StringIO()) as fake_output:
            estudiantes.registrar_camper()

        self.assertIn("Error: Ningún campo puede quedar vacío", fake_output.getvalue())
        data = estudiantes.cargar_datos()
        self.assertEqual(data["campers"], [])

    @patch("builtins.input", side_effect=["Juan Pérez", "ABC123", "juan@ejemplo.com"])
    def test_registrar_camper_documento_no_numerico_no_guarda(self, mock_input):
        with patch("sys.stdout", new=io.StringIO()) as fake_output:
            estudiantes.registrar_camper()

        self.assertIn("El documento debe ser numérico", fake_output.getvalue())
        self.assertEqual(estudiantes.cargar_datos()["campers"], [])

    @patch("builtins.input", side_effect=["Juan Pérez", "12345", "correo-invalido"])
    def test_registrar_camper_email_invalido_no_guarda(self, mock_input):
        with patch("sys.stdout", new=io.StringIO()) as fake_output:
            estudiantes.registrar_camper()

        self.assertIn("Formato de email inválido", fake_output.getvalue())
        self.assertEqual(estudiantes.cargar_datos()["campers"], [])

    def test_actualizar_camper_datos_validos_actualiza_registro(self):
        data = {"campers": [{"id": 1, "nombre": "Ana", "documento": "111", "email": "ana@x.com", "estado": "Activo"}], "ultimo_id": 1}
        estudiantes.guardar_datos(data)

        with patch("builtins.input", side_effect=["1", "Ana María", "ana.maria@x.com", "Inactivo"]):
            with patch("sys.stdout", new=io.StringIO()):
                estudiantes.actualizar_camper()

        updated = estudiantes.cargar_datos()["campers"][0]
        self.assertEqual(updated["nombre"], "Ana María")
        self.assertEqual(updated["email"], "ana.maria@x.com")
        self.assertEqual(updated["estado"], "Inactivo")

    def test_actualizar_camper_email_invalido_mantiene_email_anterior(self):
        data = {"campers": [{"id": 1, "nombre": "Ana", "documento": "111", "email": "ana@x.com", "estado": "Activo"}], "ultimo_id": 1}
        estudiantes.guardar_datos(data)

        with patch("builtins.input", side_effect=["1", "Ana", "correo-invalido", "Inactivo"]):
            with patch("sys.stdout", new=io.StringIO()) as fake_output:
                estudiantes.actualizar_camper()

        self.assertIn("Email inválido. No se actualizó el correo", fake_output.getvalue())
        updated = estudiantes.cargar_datos()["campers"][0]
        self.assertEqual(updated["email"], "ana@x.com")
        self.assertEqual(updated["estado"], "Inactivo")

    def test_actualizar_camper_id_no_encontrado_muestra_error(self):
        estudiantes.guardar_datos({"campers": [], "ultimo_id": 0})

        with patch("builtins.input", return_value="99"):
            with patch("sys.stdout", new=io.StringIO()) as fake_output:
                estudiantes.actualizar_camper()

        self.assertIn("Camper no encontrado", fake_output.getvalue())

    def test_eliminar_camper_id_existente_elimina_registro(self):
        data = {"campers": [{"id": 1, "nombre": "Ana", "documento": "111", "email": "ana@x.com", "estado": "Activo"}], "ultimo_id": 1}
        estudiantes.guardar_datos(data)

        with patch("builtins.input", return_value="1"):
            with patch("sys.stdout", new=io.StringIO()):
                estudiantes.eliminar_camper()

        self.assertEqual(estudiantes.cargar_datos()["campers"], [])

    def test_eliminar_camper_id_no_encontrado_no_cambia_datos(self):
        data = {"campers": [{"id": 1, "nombre": "Ana", "documento": "111", "email": "ana@x.com", "estado": "Activo"}], "ultimo_id": 1}
        estudiantes.guardar_datos(data)

        with patch("builtins.input", return_value="99"):
            with patch("sys.stdout", new=io.StringIO()) as fake_output:
                estudiantes.eliminar_camper()

        self.assertIn("ID no encontrado", fake_output.getvalue())
        self.assertEqual(len(estudiantes.cargar_datos()["campers"]), 1)

    def test_listar_campers_sin_registros_muestra_mensaje(self):
        estudiantes.guardar_datos({"campers": [], "ultimo_id": 0})
        with patch("sys.stdout", new=io.StringIO()) as fake_output:
            estudiantes.listar_campers()

        self.assertIn("No hay registros disponibles", fake_output.getvalue())


if __name__ == "__main__":
    unittest.main()
