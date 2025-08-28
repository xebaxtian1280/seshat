from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QScrollArea, QHBoxLayout, QComboBox, QHeaderView
)
from PyQt6.QtCore import Qt
from DB import DB 

class PestanaSeguimiento(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout_principal = QVBoxLayout(self)
        
        # Crear un área de desplazamiento
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout_principal.addWidget(self.scroll_area)
        
        # Contenedor interno para el contenido desplazable
        self.contenedor_scroll = QWidget()
        self.scroll_area.setWidget(self.contenedor_scroll)
        
        # Layout para el contenedor interno
        self.layout_contenedor = QVBoxLayout(self.contenedor_scroll)
        
        # Grupo de filtros
        self.grupo_filtros = QGroupBox("Filtros de búsqueda")
        self.layout_filtros = QHBoxLayout(self.grupo_filtros)
        
        # Columna 1: Filtros básicos
        columna_1 = QVBoxLayout()
        self.filtro_id = QLineEdit()
        self.filtro_id.setPlaceholderText("Buscar por ID")
        
        self.filtro_matricula = QLineEdit()
        self.filtro_matricula.setPlaceholderText("Buscar por Matrícula Inmobiliaria")
        
        columna_1.addWidget(QLabel("ID:"))
        columna_1.addWidget(self.filtro_id)
        columna_1.addWidget(QLabel("Matrícula Inmobiliaria:"))
        columna_1.addWidget(self.filtro_matricula)
        
        # Columna 2: Filtros del cliente y perito
        columna_2 = QVBoxLayout()
        self.filtro_id_cliente = QLineEdit()
        self.filtro_id_cliente.setPlaceholderText("Buscar por ID del Cliente")
        
        self.filtro_nombre_perito = QComboBox()
        self.filtro_nombre_perito.addItems(["Perito 1", "Perito 2", "Perito 3"])  # Lista de ejemplo
        
        self.filtro_id_perito = QLineEdit()
        self.filtro_id_perito.setPlaceholderText("Buscar por ID del Perito")
        
        columna_1.addWidget(QLabel("ID del Cliente:"))
        columna_1.addWidget(self.filtro_id_cliente)
        columna_1.addStretch()  # Espaciador para alinear los filtros
        columna_2.addWidget(QLabel("Nombre del Perito:"))
        columna_2.addWidget(self.filtro_nombre_perito)
        columna_2.addWidget(QLabel("ID del Perito:"))
        columna_2.addWidget(self.filtro_id_perito)
        
        # Columna 3: Filtro del revisor y botón de búsqueda
        columna_3 = QVBoxLayout()
        self.filtro_nombre_revisor = QComboBox()
        self.filtro_nombre_revisor.addItems(["", "Revisor 2", "Revisor 3"])  # Lista de ejemplo
        
        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_seguimiento)
        
        columna_2.addWidget(QLabel("Nombre del Revisor:"))
        columna_2.addWidget(self.filtro_nombre_revisor)
        columna_2.addStretch()  # Espaciador para alinear el botón al final
        
        
        # Agregar las columnas al layout de filtros
        self.layout_filtros.addLayout(columna_1)
        self.layout_filtros.addLayout(columna_2)        
        self.layout_filtros.addWidget(self.boton_buscar, alignment=Qt.AlignmentFlag.AlignCenter) 
        
        # Agregar el grupo de filtros al contenedor
        self.layout_contenedor.addWidget(self.grupo_filtros)
        
        # Tabla de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(7)
        self.tabla_resultados.setHorizontalHeaderLabels(["ID Avaluo", "Nombre Cliente", "ID cliente", "No. de Inmuebles", "Perito", "Revisor", "Acciones"])
        self.tabla_resultados.horizontalHeader().setStretchLastSection(True)
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout_contenedor.addWidget(self.tabla_resultados, stretch=1)
        
        self.cargar_datos_seguimiento()
        
    def cargar_datos_seguimiento(self):
        """
        Consulta la tabla 'Avaluos' de la base de datos y agrega los datos a la tabla_resultados.
        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
            db.conectar()
            # Consulta SQL para obtener los datos de la tabla 'Avaluos'
            consulta = """
            SELECT a."Avaluo_id" , a.nombre_cliente , a.id_cliente
            from "Avaluos" a 
            """
            
            # Ejecutar la consulta
            
            resultados = db.consultar(consulta)
            
            # Limpiar la tabla antes de agregar nuevos datos
            self.tabla_resultados.setRowCount(0)
            print(f"Resultados obtenidos: {resultados}")
            
            # Agregar los resultados a la tabla_resultados
            for fila, resultado in enumerate(resultados):
                self.tabla_resultados.insertRow(fila)
                for columna, valor in enumerate(resultado):
                    self.tabla_resultados.setItem(fila, columna, QTableWidgetItem(str(valor)))
                
                # Agregar un botón de acción en la última columna
                boton_accion = QPushButton("Ver")
                boton_accion.clicked.connect(lambda _, id_avaluo=resultado[0]: self.ver_avaluo(id_avaluo))
                self.tabla_resultados.setCellWidget(fila, 6, boton_accion)
        
        except Exception as e:
            print(f"Error al cargar los datos de seguimiento: {e}")    
    def buscar_seguimiento(self):
        """
        Función para buscar seguimientos según los filtros ingresados.
        """
        # Obtener valores de los filtros
        id_filtro = self.filtro_id.text()
        nombre_filtro = self.filtro_nombre.text()
        
        # Simular resultados de búsqueda
        resultados = [
            {"id": 1, "nombre": "Seguimiento 1"},
            {"id": 2, "nombre": "Seguimiento 2"},
            {"id": 3, "nombre": "Seguimiento 3"},
        ]
        
        # Filtrar resultados
        resultados_filtrados = [
            r for r in resultados
            if (not id_filtro or str(r["id"]) == id_filtro) and
               (not nombre_filtro or nombre_filtro.lower() in r["nombre"].lower())
        ]
        
        # Limpiar la tabla
        self.tabla_resultados.setRowCount(0)
        
        # Agregar resultados a la tabla
        for fila, resultado in enumerate(resultados_filtrados):
            self.tabla_resultados.insertRow(fila)
            self.tabla_resultados.setItem(fila, 0, QTableWidgetItem(str(resultado["id"])))
            self.tabla_resultados.setItem(fila, 1, QTableWidgetItem(resultado["nombre"]))
            
            # Botón de acción
            boton_accion = QPushButton("Ver")
            boton_accion.clicked.connect(lambda _, id=resultado["id"]: self.ver_seguimiento(id))
            self.tabla_resultados.setCellWidget(fila, 2, boton_accion)
    
    def ver_seguimiento(self, id):
        """
        Función para manejar la acción de ver un seguimiento.
        """
        print(f"Ver seguimiento con ID: {id}")


def agregar_pestana_seguimiento(tab_panel):
    """
    Función para agregar la pestaña de seguimiento al QTabWidget.
    """
    pestana = PestanaSeguimiento()
    tab_panel.addTab(pestana, "Seguimiento")