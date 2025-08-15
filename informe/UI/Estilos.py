from PyQt6.QtCore import QFile
from PyQt6.QtWidgets import QApplication, QWidget
import os

class Estilos:
    @staticmethod
    def cargar_estilos(self, archivo):
        ruta_absoluta = os.path.join(os.path.dirname(__file__), archivo)
        try:
            with open(ruta_absoluta, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: El archivo {ruta_absoluta} no se encontró.")
            return ""
        except Exception as e:
            print(f"Error al cargar estilos: {e}")
            return ""