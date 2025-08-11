import unittest
from PyQt6.QtWidgets import QApplication
from Index import ReportApp  # Asegúrate de que el nombre del archivo sea correcto
import sys

class TestReportApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear una instancia de QApplication para las pruebas
        cls.app = QApplication(sys.argv)

    def setUp(self):
        # Inicializar la aplicación ReportApp
        self.window = ReportApp()

    def test_window_initialization(self):
        # Verificar que la ventana principal se inicializa correctamente
        self.assertEqual(self.window.windowTitle(), "Sistema de Gestión de Informes")
        self.assertEqual(self.window.minimumWidth(), 1000)
        self.assertEqual(self.window.minimumHeight(), 700)

    def tearDown(self):
        # Cerrar la ventana después de cada prueba
        self.window.close()

    @classmethod
    def tearDownClass(cls):
        # Finalizar la instancia de QApplication
        cls.app.quit()

if __name__ == "__main__":
    unittest.main()