from PyQt6.QtCore import QFile
from PyQt6.QtWidgets import QApplication, QWidget

class Estilos:
    @staticmethod
    def cargar_estilos(widget:QWidget, archivo_css: str):
        file = QFile(archivo_css)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            contenido_css = file.readAll().data().decode("utf-8")
            widget.setStyleSheet(contenido_css)
        file.close()