import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar,
                             QFileDialog, QMenuBar, QMenu, QTabWidget, QTextEdit, 
                             QFormLayout, QSpinBox, QComboBox, QDateEdit)
from PyQt6.QtCore import Qt, QTimer, QDate
from funciones import generar_informe

class ReportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Informes")
        self.setMinimumSize(1000, 700)
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
        
        ubicacion_action = file_menu.addAction("Seleccionar ubicación")
        ubicacion_action.triggered.connect(self.seleccionar_ubicacion)
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Salir")
        exit_action.triggered.connect(self.close)
        
        menu_bar.addMenu(file_menu)
        main_layout.addWidget(menu_bar)
        
        # Panel de pestañas
        tab_panel = QTabWidget()
        
        # Crear pestañas
        self.crear_pestana_datos_solicitud(tab_panel)
        self.crear_pestana_info_basica(tab_panel)
        self.crear_pestana_info_juridica(tab_panel)
        self.crear_pestana_caracteristicas_sector(tab_panel)
        
        main_layout.addWidget(tab_panel)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)
    
    def crear_pestana_datos_solicitud(self, tab_panel):
        pestana = QWidget()
        main_layout = QHBoxLayout(pestana)
        
        # Columna izquierda (Datos de solicitud existentes)
        left_layout = QFormLayout()
        
        # Campos Cliente
        self.solicitante = QLineEdit()
        self.destinatario = QLineEdit()
        self.numero_identificacion = QLineEdit()
        
        self.fecha_solicitud = QDateEdit(QDate.currentDate())
        self.fecha_visita = QDateEdit(QDate.currentDate())
        self.fecha_informe = QDateEdit(QDate.currentDate())
        self.numero_referencia = QLineEdit()
        self.tipo_solicitud = QComboBox()
        self.tipo_solicitud.addItems(["Originacion", "Actualizacion", "Avaluo por escritorio", "Concepto de valor"])
        
        left_layout.addRow("Solicitante:", self.solicitante)
        left_layout.addRow("Destinatario:", self.destinatario)
        left_layout.addRow("Documento de ID:", self.numero_identificacion)
        left_layout.addRow("Fecha de solicitud:", self.fecha_solicitud)
        left_layout.addRow("Fecha de visita:", self.fecha_visita)
        left_layout.addRow("Fecha de informe:", self.fecha_informe)
        left_layout.addRow("Número de referencia:", self.numero_referencia)
        left_layout.addRow("Tipo de solicitud:", self.tipo_solicitud)
        
        # Columna derecha (Datos del inmueble)
        right_layout = QFormLayout()
        
        # Campos nuevos del inmueble
        self.direccion_inmueble = QLineEdit()
        self.barrio_inmueble = QLineEdit()
        self.ciudad_inmueble = QLineEdit()
        self.departamento_inmueble = QLineEdit()
        
        self.tipo_avaluo = QComboBox()
        self.tipo_avaluo.addItems(["Comercial", "Jurídico", "Financiero", "Seguros"])
        
        self.latitud = QLineEdit()
        self.latitud.setPlaceholderText("Ej: 4.6097")
        self.longitud = QLineEdit()
        self.longitud.setPlaceholderText("Ej: -74.0817")
        
        # Documentación dinámica
        self.documentacion_layout = QVBoxLayout()
        self.btn_agregar_doc = QPushButton("Agregar Documento")
        self.btn_agregar_doc.clicked.connect(self.agregar_campo_documento)
        
        # Campos iniciales
        self.agregar_campo_documento()  # Primer campo por defecto
        
        right_layout.addRow("Dirección del inmueble:", self.direccion_inmueble)
        right_layout.addRow("Barrio:", self.barrio_inmueble)
        right_layout.addRow("Ciudad:", self.ciudad_inmueble)
        right_layout.addRow("Departamento:", self.departamento_inmueble)
        right_layout.addRow("Tipo de avalúo:", self.tipo_avaluo)
        right_layout.addRow(QLabel("Coordenadas:"))
        right_layout.addRow("Latitud:", self.latitud)
        right_layout.addRow("Longitud:", self.longitud)
        right_layout.addRow(QLabel("Documentación aportada:"))
        right_layout.addRow(self.btn_agregar_doc)
        right_layout.addRow(self.documentacion_layout)
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        
        tab_panel.addTab(pestana, "Datos de la Solicitud")

    def agregar_campo_documento(self):
        campo = QLineEdit()
        campo.setPlaceholderText("Nombre del documento")
        campo.setClearButtonEnabled(True)
        self.documentacion_layout.addWidget(campo)
    
    def crear_pestana_info_basica(self, tab_panel):
        pestana = QWidget()
        layout = QFormLayout()
        
        self.nombre_proyecto = QLineEdit()
        self.ubicacion = QLineEdit()
        self.area_total = QSpinBox()
        self.area_total.setRange(0, 1000000)
        self.descripcion = QTextEdit()
        
        layout.addRow("Nombre del proyecto:", self.nombre_proyecto)
        layout.addRow("Ubicación física:", self.ubicacion)
        layout.addRow("Área total (m²):", self.area_total)
        layout.addRow("Descripción:", self.descripcion)
        
        pestana.setLayout(layout)
        tab_panel.addTab(pestana, "Información Básica")
    
    def crear_pestana_info_juridica(self, tab_panel):
        pestana = QWidget()
        layout = QFormLayout()
        
        self.estado_juridico = QComboBox()
        self.estado_juridico.addItems(["En trámite", "Aprobado", "Rechazado", "En revisión"])
        self.numero_escritura = QLineEdit()
        self.fecha_escritura = QDateEdit()
        self.observaciones = QTextEdit()
        
        layout.addRow("Estado jurídico:", self.estado_juridico)
        layout.addRow("Número de escritura:", self.numero_escritura)
        layout.addRow("Fecha de escritura:", self.fecha_escritura)
        layout.addRow("Observaciones legales:", self.observaciones)
        
        pestana.setLayout(layout)
        tab_panel.addTab(pestana, "Información Jurídica")
    
    def crear_pestana_caracteristicas_sector(self, tab_panel):
        pestana = QWidget()
        layout = QFormLayout()
        
        self.zona = QComboBox()
        self.zona.addItems(["Residencial", "Comercial", "Industrial", "Mixto"])
        self.equipamientos = QTextEdit()
        self.infrastructure = QTextEdit()
        self.riesgos = QTextEdit()
        
        layout.addRow("Zona:", self.zona)
        layout.addRow("Equipamientos urbanos:", self.equipamientos)
        layout.addRow("Infraestructura:", self.infrastructure)
        layout.addRow("Riesgos identificados:", self.riesgos)
        
        pestana.setLayout(layout)
        tab_panel.addTab(pestana, "Características del Sector")
    
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
        contenido = f"""
        --- DATOS DE LA SOLICITUD ---
        Solicitante: {self.solicitante.text()}
        Fecha: {self.fecha_solicitud.date().toString("dd/MM/yyyy")}
        Referencia: {self.numero_referencia.text()}
        Tipo: {self.tipo_solicitud.currentText()}
        
        --- INFORMACIÓN BÁSICA ---
        Proyecto: {self.nombre_proyecto.text()}
        Ubicación: {self.ubicacion.text()}
        Área: {self.area_total.value()} m²
        Descripción: {self.descripcion.toPlainText()}
        
        --- INFORMACIÓN JURÍDICA ---
        Estado: {self.estado_juridico.currentText()}
        Escritura: {self.numero_escritura.text()}
        Fecha Escritura: {self.fecha_escritura.date().toString("dd/MM/yyyy")}
        Observaciones: {self.observaciones.toPlainText()}
        
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