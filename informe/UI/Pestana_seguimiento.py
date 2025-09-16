from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QScrollArea, QHBoxLayout, QComboBox, QHeaderView, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from DB import DB 

from Pestana_Imagenes import agregar_pestana_imagenes
from Pestana_Datos_solicitud import PestanaDatosSolicitud
from Pestana_caracteristicas_sector import PestanaCaracteristicasSector
from Pestana_caracteristicas_construccion import PestanaCaracteristicasConstruccion
from Pestana_condiciones_valuacion import PestanaCondicionesValuacion

class PestanaSeguimiento(QWidget):
    
    # Señal personalizada para enviar el id_avaluo
    id_avaluo_seleccionado = pyqtSignal(str)
    
    def __init__(self, tab_panel: QTabWidget):
        super().__init__()
        
        self.tab_panel = tab_panel
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
        
        # Columna 3: Filtro del revisor y botón de búsqueda
        columna_3 = QVBoxLayout()
        self.filtro_nombre_revisor = QComboBox()
        
        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_seguimiento)
        self.cargar_revisores()
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
        self.tabla_resultados.setHorizontalHeaderLabels(["ID Avaluo", "Nombre Cliente", "ID cliente", "Perito", "Revisor","No. de Inmuebles","Estado", "Acciones"])
        self.tabla_resultados.horizontalHeader().setStretchLastSection(True)
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout_contenedor.addWidget(self.tabla_resultados, stretch=1)
        
        self.cargar_datos_seguimiento(tab_panel)
        
        tab_panel.addTab(self.scroll_area, "Seguimiento")       
    
    
    def cargar_peritos(self):
        """
        Consulta la tabla 'peritos' de la base de datos y agrega los nombres de los peritos a self.filtro_nombre_perito.
        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
            db.conectar()
    
            # Consulta SQL para obtener los nombres de los peritos
            consulta = "SELECT nombre FROM peritos"            
            resultados = db.consultar(consulta)
    
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.filtro_nombre_perito.clear()
    
            # Agregar los nombres de los peritos al QComboBox
            for resultado in resultados:
                self.filtro_nombre_perito.addItem(resultado[0])  # resultado[0] contiene el nombre del perito
    
        except Exception as e:
            print(f"Error al cargar los peritos: {e}")
            
    def cargar_revisores(self):
        """
        Consulta la tabla 'peritos' de la base de datos y agrega los nombres de los peritos a self.filtro_nombre_perito.
        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
            db.conectar()
    
            # Consulta SQL para obtener los nombres de los peritos
            consulta = "SELECT nombre FROM revisores"            
            resultados = db.consultar(consulta)
    
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.filtro_nombre_revisor.clear()
    
            # Agregar los nombres de los peritos al QComboBox
            for resultado in resultados:
                self.filtro_nombre_revisor.addItem(resultado[0])  # resultado[0] contiene el nombre del perito
    
        except Exception as e:
            print(f"Error al cargar los peritos: {e}")
    
    def cargar_datos_seguimiento(self, tab_panel):
        """
        Consulta la tabla 'Avaluos' de la base de datos y agrega los datos a la tabla_resultados.
        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
            db.conectar()
            # Consulta SQL para obtener los datos de la tabla 'Avaluos'
            consulta = """
            SELECT 
                a."Avaluo_id", 
                a.nombre_cliente, 
                a.id_cliente, 
                CONCAT(p.nombre, ' ', p.apellido) AS perito_nombre,
                CONCAT(r.nombre, ' ', r.apellido) AS revisor_nombre
            FROM "Avaluos" a
            LEFT JOIN 
                peritos p ON a.id_peritos  = p.id_peritos 
            LEFT JOIN 
                revisores r ON a.id_revisor  = r.id_revisor 
            """

            # Ejecutar la consulta
            
            resultados = db.consultar(consulta)
            
            # Limpiar la tabla antes de agregar nuevos datos
            self.tabla_resultados.setRowCount(0)
            
            # Agregar los resultados a la tabla_resultados
            for fila, resultado in enumerate(resultados):
                self.tabla_resultados.insertRow(fila)
                for columna, valor in enumerate(resultado):
                    self.tabla_resultados.setItem(fila, columna, QTableWidgetItem(str(valor)))
                
                # Agregar un botón de acción en la última columna
                boton_accion = QPushButton("Ver")
                id_avaluo=str(resultado[0])
                print("ID Avaluo:", id_avaluo)
                boton_accion.setProperty("id_avaluo", id_avaluo)  # Asignar el id_avaluo como propiedad
                boton_accion.clicked.connect(lambda:self.manejar_click_boton())
                # boton_accion.clicked.connect(lambda id_avaluo=id_avaluo: print(f"Botón presionado con id_avaluo: {id_avaluo}") or self.agregar_pestanas_avaluo(id_avaluo, tab_panel))
                # Pasar el ID del avalúo al método agregar_pestanas_avaluo
                self.tabla_resultados.setCellWidget(fila, 6, boton_accion)
        
        except Exception as e:
            print(f"Error al cargar los datos de seguimiento: {e}")   
            
        # Método para manejar el clic del botón
    
    def manejar_click_boton(self):
        boton = self.sender()  # Obtener el botón que disparó la señal
        id_avaluo = boton.property("id_avaluo")  # Recuperar el id_avaluo
        print(f"Botón presionado con id_avaluo: {id_avaluo}")
        self.id_avaluo_seleccionado.emit(id_avaluo)  # Emitir la señal con el id_avaluo
        self.agregar_pestanas_avaluo(id_avaluo, self.tab_panel)
    
    def agregar_pestanas_avaluo(self, id_avaluo, tab_panel):
        
        """
        Agrega las pestañas relacionadas con el avalúo al accionar el botón 'boton_accion'.
        Pasa el id_avaluo a cada pestaña para cargar la información correspondiente.
        
        :param id_avaluo: ID del avalúo seleccionado.
        """
        
        try:
            # Crear las pestañas con el id_avaluo
            
            """ pestana_solicitud = PestanaDatosSolicitud(id_avaluo)
            pestana_sector = PestanaCaracteristicasSector(id_avaluo)
            pestana_construccion = PestanaCaracteristicasConstruccion(id_avaluo)
            pestana_valuacion = PestanaCondicionesValuacion(id_avaluo)
            pestana_imagenes = agregar_pestana_imagenes(id_avaluo) """
            
            
            for index in range(tab_panel.count()):
                
                widget = tab_panel.widget(index)
                validacion=(tab_panel.tabText(index) == "PestanaDatosSolicitud")
                
                if tab_panel.tabText(index) == "Datos de la Solicitud":
                    # Si la pestaña ya existe, mover a esa pestaña y actualizar el id_avaluo
                    tab_panel.setCurrentIndex(index)
                    widget.cargar_datos_solicitud(id_avaluo)  # Método para actualizar los datos con el nuevo id_avaluo
                    print(f"Movido a la pestaña existente 'PestanaDatosSolicitud' con id_avaluo: {id_avaluo}")
                    seguimiento_index = tab_panel.indexOf(self)
                    if seguimiento_index != -1:
                        tab_panel.removeTab(seguimiento_index)
                        print("Pestaña de seguimiento cerrada.")
                    return  # Salir de la función para evitar agregar pestañas duplicadas
                
            # Agregar las pestañas al QTabWidget
            PestanaDatosSolicitud(tab_panel, id_avaluo)   
            print(f"Movido a la pestaña existente 'PestanaDatosSolicitud' con id_avaluo: {id_avaluo}")
            """ PestanaCaracteristicasSector(self.tab_panel)
            PestanaCaracteristicasConstruccion(self.tab_panel)
            PestanaCondicionesValuacion(self.tab_panel)
            agregar_pestana_imagenes(self.tab_panel)  """
            
            tab_panel.setCurrentIndex(index+1)
            
            seguimiento_index = tab_panel.indexOf(self)
            print("Cantidad de pesta;as : ",(seguimiento_index))
            if tab_panel.count()>1:
                tab_panel.removeTab(index)
                print("Pestaña de seguimiento cerrada.")
    
            print(f"Pestañas agregadas para el avalúo con ID: {id_avaluo}")
                
            
    
        except Exception as e:
            print(f"Error al agregar las pestañas: {e}") 
    
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