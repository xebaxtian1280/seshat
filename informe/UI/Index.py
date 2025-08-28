import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QProgressBar,
                             QFileDialog, QMenuBar, QMenu, QTabWidget)
from PyQt6.QtCore import Qt, QTimer

# Importar las pestañas

from Pestana_Imagenes import agregar_pestana_imagenes
from Pestana_Datos_solicitud import PestanaDatosSolicitud
from Pestana_caracteristicas_sector import PestanaCaracteristicasSector
from Pestana_caracteristicas_construccion import PestanaCaracteristicasConstruccion
from Pestana_condiciones_valuacion import PestanaCondicionesValuacion
from Pestana_seguimiento import agregar_pestana_seguimiento

QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)


class ReportApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sistema de Gestión de Informes")
        #self.setMinimumSize(1000, 700)
        self.showMaximized()
        self.default_save_path = str(Path.home() / "/Proyectos/seshat/informe/Resultados")
        self.init_ui()

    def init_ui(self):
        # Configurar widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Barra de menú integrada en el panel
        menu_bar = QMenuBar()
        file_menu = QMenu("&Archivo", self)
        
        # Acciones del menú
        generar_action = file_menu.addAction("Generar Informe")
        generar_action.triggered.connect(self.iniciar_generacion)
        
        ubicacion_action = file_menu.addAction("Guardar Como")
        ubicacion_action.triggered.connect(self.seleccionar_ubicacion)
        
        crear_proyecto = file_menu.addAction("Crear Proyecto")
        crear_proyecto.triggered.connect(self.crea_proyecto)
        
        abrir_proyecto = file_menu.addAction("Abrir proyecto")
        abrir_proyecto.triggered.connect(self.carga_proyecto)
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Salir")
        exit_action.triggered.connect(self.close)
        
        menu_bar.addMenu(file_menu)
        main_layout.addWidget(menu_bar)
        
        # Panel de pestañas
        self.tab_panel = QTabWidget()
        
        
        # Crear pestañas
        agregar_pestana_seguimiento(self.tab_panel)
        PestanaDatosSolicitud(self.tab_panel)        
        PestanaCaracteristicasSector(self.tab_panel)
        PestanaCaracteristicasConstruccion(self.tab_panel)
        PestanaCondicionesValuacion(self.tab_panel)
        agregar_pestana_imagenes(self.tab_panel)       
        
        
        main_layout.addWidget(self.tab_panel)
        
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)
        
    
    def seleccionar_ubicacion(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
    def crea_proyecto(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
            
    def carga_proyecto(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
    
    def iniciar_generacion(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_progreso)
        self.timer.start(100)
    
    def actualizar_progreso(self):
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
        else:
            self.timer.stop()
            self.procesar_informe()
            self.progress_bar.hide()
    
    def procesar_informe(self):
        # Recolectar datos de todas las pestañas
        
        # Obtener todas las matrículas
        matriculas = []
        for i in range(self.matricula_layout.count()):
            item = self.matricula_layout.itemAt(i)
            if item and isinstance(item, QHBoxLayout):
                line_edit = item.itemAt(0).widget()
                if line_edit and line_edit.text():
                    matriculas.append(line_edit.text())
        
        contenido = f"""
        --- DATOS DE LA SOLICITUD ---
        Cliente: {self.cliente.text()}
        Documento ID: {self.doc_identidad.text()}
        Destinatario: {self.destinatario.text()}
        Fecha Visita: {self.fecha_visita.date().toString("dd/MM/yyyy")}
        Fecha Informe: {self.fecha_informe.date().toString("dd/MM/yyyy")}
        
        --- INFORMACIÓN JURÍDICA ---
        Propietario: {self.propietario.text()}
        ID Propietario: {self.id_propietario.text()}
        Documento Propiedad: {self.doc_propiedad.toPlainText()}
        Matrícula: {self.matricula_inmobiliaria.text()}
        Cédula Catastral: {self.cedula_catastral.text()}
        Adquisición: {self.modo_adquisicion.currentText()}
        Limitaciones: {self.limitaciones.toPlainText()}
        
        --- CARACTERÍSTICAS DEL SECTOR ---
        Zona: {self.zona.currentText()}
        Equipamientos: {self.equipamientos.toPlainText()}
        Infraestructura: {self.infrastructure.toPlainText()}
        Riesgos: {self.riesgos.toPlainText()}
        """
        
        file_path = f"{self.default_save_path}/informe_{time.strftime('%Y%m%d-%H%M%S')}"
        success, resultado = generar_informe(contenido, file_path)
        
        if success:
            QMessageBox.information(self, "Éxito", f"Informe guardado en:\n{resultado}")
        else:
            QMessageBox.critical(self, "Error", f"Error al generar informe:\n{resultado}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportApp()
    window.show()
    sys.exit(app.exec())