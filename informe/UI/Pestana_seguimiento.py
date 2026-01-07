from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QScrollArea, QHBoxLayout, QComboBox, QHeaderView, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from DB import DB 

from Pestana_Imagenes import agregar_pestana_imagenes
#`from Pestana_Datos_solicitud import PestanaDatosSolicitud
from Pestana_caracteristicas_sector import PestanaCaracteristicasSector
from Pestana_caracteristicas_construccion import PestanaCaracteristicasConstruccion
from Pestana_condiciones_valuacion import PestanaCondicionesValuacion
from Funciones import Funciones

class PestanaSeguimiento(QWidget):
    
    # Señal personalizada para enviar el id_avaluo
    id_avaluo_seleccionado = pyqtSignal(str)

    
    
    def __init__(self, tab_panel: QTabWidget, ventana_principal=None):
        super().__init__()
        
        self.tab_panel = tab_panel
        self.ventana_principal = ventana_principal
        # Layout principal
        self.basededatos = 'seshat_db'
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
        self.cargar_peritos()  # Cargar los nombres de los peritos desde la base de datos
        
        self.filtro_id_perito = QLineEdit()
        self.filtro_id_perito.setPlaceholderText("Buscar por ID del Perito")
        
        columna_1.addWidget(QLabel("ID del Cliente:"))
        columna_1.addWidget(self.filtro_id_cliente)
        columna_1.addStretch()  # Espaciador para alinear los filtros
        columna_2.addWidget(QLabel("Nombre del Perito:"))
        columna_2.addWidget(self.filtro_nombre_perito)
        columna_2.addWidget(QLabel("ID del Perito:"))
        columna_2.addWidget(self.filtro_id_perito)
        
        # Columna 3: Filtro del revisor y botón de búsqueda y limpiar
        columna_3 = QVBoxLayout()
        self.filtro_nombre_revisor = QComboBox()
        
        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_seguimiento)
        
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_limpiar.clicked.connect(self.limpiar_filtros)
        
        
        self.cargar_revisores()
        columna_2.addWidget(QLabel("Nombre del Revisor:"))
        columna_2.addWidget(self.filtro_nombre_revisor)
        columna_2.addStretch()  # Espaciador para alinear el botón al final
        
        
        # Agregar las columnas al layout de filtros
        self.layout_filtros.addLayout(columna_1)
        self.layout_filtros.addLayout(columna_2)        
        self.layout_filtros.addWidget(self.boton_buscar, alignment=Qt.AlignmentFlag.AlignCenter )
        self.layout_filtros.addWidget(self.boton_limpiar, alignment=Qt.AlignmentFlag.AlignCenter ) 
         

        # Agregar el grupo de filtros al contenedor
        self.layout_contenedor.addWidget(self.grupo_filtros)
        
        # Tabla de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(8)
        self.tabla_resultados.setHorizontalHeaderLabels(["ID Avaluo", "Nombre Cliente", "ID cliente", "Perito", "Revisor","Estado","No. de Inmuebles" , "Acciones"])
        self.tabla_resultados.horizontalHeader().setStretchLastSection(True)
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout_contenedor.addWidget(self.tabla_resultados, stretch=1)
        
        self.cargar_datos_seguimiento(tab_panel)
        
        tab_panel.addTab(self.scroll_area, "Seguimiento")       
    
    def limpiar_filtros(self):
        """
        Limpia todos los filtros y actualiza la información de la tabla.
        """
        # Limpiar los valores de los filtros
        self.filtro_id.clear()
        self.filtro_matricula.clear()
        self.filtro_id_cliente.clear()
        self.filtro_nombre_perito.setCurrentIndex(0)  # Seleccionar el primer elemento (vacío)
        self.filtro_id_perito.clear()
        self.filtro_nombre_revisor.setCurrentIndex(0)  # Seleccionar el primer elemento (vacío)
    
        # Actualizar la información de la tabla
        self.cargar_datos_seguimiento(self.tab_panel)
    
    def cargar_peritos(self):
        """
        Consulta la tabla 'peritos' de la base de datos y agrega los nombres de los peritos a self.filtro_nombre_perito.
        """
        try:
            # Crear una instancia de la clase DB
            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()
    
            # Consulta SQL para obtener los nombres de los peritos
            consulta = "SELECT nombre FROM peritos"            
            resultados = db.consultar(consulta)
    
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.filtro_nombre_perito.clear()
    
            # Agregar los nombres de los peritos al QComboBox
            self.filtro_nombre_perito.addItem("")
            for resultado in resultados:
                self.filtro_nombre_perito.addItem(resultado[0])  # resultado[0] contiene el nombre del perito
            db.cerrar_conexion()
        except Exception as e:
            print(f"Error al cargar los peritos: {e}")
            
    def cargar_revisores(self):
        """
        Consulta la tabla 'peritos' de la base de datos y agrega los nombres de los peritos a self.filtro_nombre_perito.
        """
        try:
            # Crear una instancia de la clase DB
            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()
    
            # Consulta SQL para obtener los nombres de los peritos
            consulta = "SELECT nombre FROM revisores"            
            resultados = db.consultar(consulta)
    
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.filtro_nombre_revisor.clear()
            self.filtro_nombre_revisor.addItem("") 
            # Agregar los nombres de los peritos al QComboBox
            for resultado in resultados:
                self.filtro_nombre_revisor.addItem(resultado[0])  # resultado[0] contiene el nombre del perito
            db.cerrar_conexion()
        except Exception as e:
            print(f"Error al cargar los peritos: {e}")
    
    def cargar_datos_seguimiento(self, tab_panel):
        """
        Consulta la tabla 'Avaluos' de la base de datos y agrega los datos a la tabla_resultados.
        """
        try:
            # Crear una instancia de la clase DB
            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()
            # Consulta SQL para obtener los datos de la tabla 'Avaluos'
            consulta = """
            SELECT 
                a."Avaluo_id", 
                a.nombre_cliente, 
                a.id_cliente, 
                CONCAT(p.nombre, ' ', p.apellido) AS perito_nombre,
                CONCAT(r.nombre, ' ', r.apellido) AS revisor_nombre,
                a.estado
            FROM "Avaluos" a
            LEFT JOIN 
                peritos p ON a.id_peritos  = p.id_peritos 
            LEFT JOIN 
                revisores r ON a.id_revisor  = r.id_revisor 
            ORDER BY a."Avaluo_id" ASC
            """

            # Ejecutar la consulta
            
            resultados = db.consultar(consulta)
            
            # Limpiar la tabla antes de agregar nuevos datos
            self.tabla_resultados.setRowCount(0)
            
            # Agregar los resultados a la tabla_resultados
            self.agregar_resultados_tabla(db, resultados)
            db.cerrar_conexion()
        except Exception as e:
            print(f"Error al cargar los datos de seguimiento: {e}")   
            
        # Método para manejar el clic del botón
    
    def agregar_resultados_tabla(self, db, resultados):
        for fila, resultado in enumerate(resultados):
                self.tabla_resultados.insertRow(fila)
                for columna, valor in enumerate(resultado):
                    self.tabla_resultados.setItem(fila, columna, QTableWidgetItem(str(valor)))
                    
                # Calcula y agrega el numero de matriculas por avaluo
                self.tabla_resultados.setItem(fila, 7, QTableWidgetItem("En Proceso"))
                query = """ SELECT COUNT(*) FROM inmuebles WHERE avaluo_id = x; """.replace("x", str(resultado[0]))
                id_avaluo = resultado[0]
                numero_inmuebles = db.consultar(query, (id_avaluo,))
                print(f"ID Avaluo: {resultado[0]}, Número de inmuebles: {numero_inmuebles[0][0]}")
                self.tabla_resultados.setItem(fila, 6, QTableWidgetItem(str(numero_inmuebles[0][0])))
                
                # Agregar un botón de acción en la última columna
                boton_accion = QPushButton("Ver")
                id_avaluo=str(resultado[0])
                print("ID Avaluo:", id_avaluo)
                boton_accion.setProperty("id_avaluo", id_avaluo)  # Asignar el id_avaluo como propiedad
                boton_accion.clicked.connect(lambda:self.manejar_click_boton())
                # boton_accion.clicked.connect(lambda id_avaluo=id_avaluo: print(f"Botón presionado con id_avaluo: {id_avaluo}") or self.agregar_pestanas_avaluo(id_avaluo, tab_panel))
                # Pasar el ID del avalúo al método agregar_pestanas_avaluo
                self.tabla_resultados.setCellWidget(fila, 7, boton_accion)
    
    def manejar_click_boton(self):
        boton = self.sender()  # Obtener el botón que disparó la señal
        id_avaluo = boton.property("id_avaluo")  # Recuperar el id_avaluo
        print(f"Botón presionado con id_avaluo: {id_avaluo}")
        self.id_avaluo_seleccionado.emit(id_avaluo)  # Emitir la señal con el id_avaluo
        Funciones.agregar_pestanas_avaluo(self, id_avaluo, self.tab_panel, ventana_principal=self.ventana_principal)
        #self.agregar_pestanas_avaluo(id_avaluo, self.tab_panel)
    
    def buscar_seguimiento(self):
        # Construir la consulta SQL dinámica
        query = """
        SELECT 
            a."Avaluo_id", 
            a.nombre_cliente, 
            a.id_cliente, 
            CONCAT(p.nombre, ' ', p.apellido) AS perito_nombre,
            CONCAT(r.nombre, ' ', r.apellido) AS revisor_nombre
        FROM "Avaluos" a
        LEFT JOIN 
            peritos p ON a.id_peritos = p.id_peritos 
        LEFT JOIN 
            revisores r ON a.id_revisor = r.id_revisor
        WHERE 1=1
        """
        parametros = []
        # Agregar filtros dinámicamente
        if self.filtro_id.text():
            query += """ AND a."Avaluo_id" = %s"""
            parametros.append(self.filtro_id.text())
        """ if self.filtro_id_cliente.text():
            query += " AND matricula_inmobiliaria ILIKE %s"
            parametros.append(f"%{self.filtro_id_cliente.text()}%") """
        if self.filtro_id_perito.text():
            query += " AND a.id_cliente = %s"
            parametros.append(self.filtro_id_perito.text())
        if self.filtro_matricula.text():
            query += " AND p.nombre ILIKE %s"
            parametros.append(f"%{self.filtro_matricula.text()}%")
        if self.filtro_nombre_perito.currentText():
            query += " AND p.nombre = %s"
            parametros.append(self.filtro_nombre_perito.currentText())
        if self.filtro_nombre_revisor.currentText():
            query += " AND r.nombre ILIKE %s"
            parametros.append(f"%{self.filtro_nombre_revisor.currentText()}%")
            
        print("Consulta SQL:", query)
        # Ejecutar la consulta
        db = self.ventana_principal.obtener_conexion_db()
        db.conectar()
        resultados = db.consultar(query, parametros)
        
        # Limpiar la tabla
        self.tabla_resultados.setRowCount(0)
        
        # Agregar resultados a la tabla
        
         # Agregar los resultados a la tabla_resultados
        self.agregar_resultados_tabla(db, resultados)
        db.cerrar_conexion()
       
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