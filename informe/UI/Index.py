import sys, os

# ============================================================================
# CONFIGURACIÓN PARA EVITAR ERRORES DE VULKAN/COMPOSITOR EN QWEBENGINEVIEW
# ============================================================================
# Estas variables DEBEN configurarse ANTES de importar cualquier módulo de Qt
# Soluciona: "Backend texture is not a Vulkan texture" / "Compositor returned null texture"

# Deshabilitar aceleración GPU en Chromium (usado por QWebEngineView)
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu --disable-software-rasterizer --no-sandbox --disable-setuid-sandbox'

# Deshabilitar sandbox de Chromium (necesario en algunos sistemas Linux)
os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'

# Forzar rendering sin aceleración OpenGL
os.environ['QT_XCB_GL_INTEGRATION'] = 'none'

# Usar software rendering en Mesa
os.environ['LIBGL_ALWAYS_SOFTWARE'] = '1'

# ============================================================================

import subprocess
import time
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QProgressBar,
                             QFileDialog, QMenuBar, QMenu, QTabWidget, QScrollArea,
                             QDialog, QLabel, QLineEdit, QPushButton, QFormLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QSystemTrayIcon
# Importar las pestañas

from Pestana_Imagenes import agregar_pestana_imagenes
from Pestana_Datos_solicitud import PestanaDatosSolicitud
from Pestana_caracteristicas_sector import PestanaCaracteristicasSector
from Pestana_caracteristicas_construccion import PestanaCaracteristicasConstruccion
from Pestana_condiciones_valuacion import PestanaCondicionesValuacion
from Pestana_seguimiento import PestanaSeguimiento
from DB import DB

from Funciones import Funciones

# Configurar atributos de Qt ANTES de crear QApplication
# Compartir contextos OpenGL entre widgets
QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
# Usar OpenGL por software (evita problemas con drivers)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL)

usuario_global = ""
password_global = ""

class LoginDialog(QDialog):
    """Diálogo de autenticación de usuario"""
    
    # Credenciales por defecto (en producción deberían estar en BD)
    USUARIOS_VALIDOS = {
        "admin": "admin123",
        "usuario": "usuario123"
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inicio de Sesión - Sistema de Gestión de Informes")
        self.setModal(True)
        self.setFixedSize(400, 200)
        self.intentos_fallidos = 0
        self.max_intentos = 3
        self.usuario_autenticado = None
        self.password_usuario = None  # Almacenar el password del usuario
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Iniciar Sesión")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Campo de usuario
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Ingrese su usuario")
        form_layout.addRow("Usuario:", self.usuario_input)
        
        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.returnPressed.connect(self.validar_credenciales)
        form_layout.addRow("Contraseña:", self.password_input)
        
        layout.addLayout(form_layout)
        
        # Mensaje de error
        self.mensaje_error = QLabel("")
        self.mensaje_error.setStyleSheet("color: red; font-size: 12px;")
        self.mensaje_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mensaje_error)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        self.btn_ingresar = QPushButton("Ingresar")
        self.btn_ingresar.clicked.connect(self.validar_credenciales)
        self.btn_ingresar.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.cancelar)
        self.btn_cancelar.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        
        botones_layout.addWidget(self.btn_ingresar)
        botones_layout.addWidget(self.btn_cancelar)
        
        layout.addLayout(botones_layout)
        
        self.setLayout(layout)
        
        # Focus en el campo de usuario
        self.usuario_input.setFocus()
    
    def validar_credenciales(self):
        """Valida las credenciales ingresadas"""
        usuario = self.usuario_input.text().strip()
        password = self.password_input.text()

        print( not usuario or not password)
        if not usuario or not password:
            self.mostrar_error("Por favor ingrese usuario y contraseña")
            return
        
        try:
            # Crear una instancia de la clase DB
            db = DB(host="192.168.0.9", database="seshat_db", user=usuario, password=password)
            if db.conectar():
                self.usuario_autenticado = usuario
                self.password_usuario = password  # Almacenar password en la instancia
                global usuario_global, password_global
                usuario_global = usuario
                password_global = password
                self.accept()  # Cerrar diálogo con éxito
            else:
                self.intentos_fallidos += 1
                intentos_restantes = self.max_intentos - self.intentos_fallidos
                
                if self.intentos_fallidos >= self.max_intentos:
                    QMessageBox.critical(
                        self,
                        "Acceso Denegado",
                        "Ha excedido el número máximo de intentos. La aplicación se cerrará."
                    )
                    self.reject()  # Cerrar diálogo con fallo
                    sys.exit(1)  # Cerrar aplicación
                else:
                    self.mostrar_error(
                        f"Usuario o contraseña incorrectos. "
                        f"Intentos restantes: {intentos_restantes}"
                    )
                    self.password_input.clear()
                    self.password_input.setFocus()
            db.cerrar_conexion()
        except Exception as e:
            self.mostrar_error("Error al intentar conectarse con la base de datos")
            print(f"Error al intentar loguearse: {e}")
            
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en el diálogo"""
        self.mensaje_error.setText(mensaje)
        # Limpiar mensaje después de 3 segundos
        QTimer.singleShot(5000, lambda: self.mensaje_error.setText(""))
    
    def cancelar(self):
        """Cancela el login y cierra la aplicación"""
        respuesta = QMessageBox.question(
            self,
            "Cancelar",
            "¿Está seguro que desea cancelar? La aplicación se cerrará.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        """ if respuesta == QMessageBox.StandardButton.Yes:
            self.reject()
            sys.exit(0)
 """

class ReportApp(QMainWindow):
    
    def __init__(self, usuario_autenticado=None, password_usuario=None):
        super().__init__()
        
        self.setWindowTitle("Sistema de Gestión de Informes")
        self.create_tray_icon_with_file() # Asegúrate de tener un icono en la ruta especificada
        #self.setMinimumSize(1000, 700)

        self.basededatos = "seshat_db"
        
        # Almacenar credenciales del usuario autenticado
        self.usuario_autenticado = usuario_autenticado
        self.password_usuario = password_usuario
        self.db_host = "192.168.0.9"  # Configurar según tu entorno
        self.db_user = usuario_global    # Usuario de BD (puedes cambiarlo)
        self.db_password = password_global # Password de BD (puedes cambiarlo)

        self.showMaximized()
        
        self.default_save_path = ""
        self.file_path = None
        self.pestana_anterior = 0
        self.init_ui()

    def init_ui(self):
        # Configurar widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Barra de menú integrada en el panel
        menu_bar = QMenuBar()
        self.file_menu = QMenu("&Archivo", self)
        
        # Acciones del menú
        generar_action = self.file_menu.addAction("Seguimiento")
        generar_action.triggered.connect(lambda: self.volver_a_seguimiento())
        
        generar_action = self.file_menu.addAction("Radicar Solicitud")
        generar_action.triggered.connect(lambda: Funciones.agregar_pestanas_avaluo(self,"",self.tab_panel, ventana_principal=self))
        
        ubicacion_action = self.file_menu.addAction("Guardar Como")
        ubicacion_action.triggered.connect(self.seleccionar_ubicacion)
        
        crear_proyecto = self.file_menu.addAction("Crear Proyecto")
        crear_proyecto.triggered.connect(self.crea_proyecto)
        
        self.file_menu.addSeparator()
        exit_action = self.file_menu.addAction("Salir")
        exit_action.triggered.connect(self.close)
        
        menu_bar.addMenu(self.file_menu)

        

        # Barra de proyecto integrada en el panel

        self.file_proyecto = QMenu("&Proyecto", self)

        abrir_proyecto = self.file_proyecto.addAction("Directorio del proyecto")
        abrir_proyecto.triggered.connect(self.carga_proyecto)

        generar_action = self.file_proyecto.addAction("Generar Informe")
        generar_action.triggered.connect(self.iniciar_generacion)
        
        generar_ficha_action = self.file_proyecto.addAction("Generar Ficha Predial")
        generar_ficha_action.triggered.connect(self.iniciar_generacion_ficha_predial)

        menu_bar.addMenu(self.file_proyecto)
        self.file_proyecto.menuAction().setVisible(False)  # Oculto por defecto

        main_layout.addWidget(menu_bar)

        # Panel de pestañas
        self.tab_panel = QTabWidget()

        self.tab_panel.currentChanged.connect(lambda: self.on_tab_changed(self.tab_panel, self.tab_panel.currentIndex()))
        self.tab_panel.tabCloseRequested.connect(lambda: self.on_tab_changed(self.tab_panel, self.tab_panel.currentIndex()))

        # Crear las pestañas

        self.pestana_seguimiento = PestanaSeguimiento(self.tab_panel, ventana_principal=self)
        
        # Conectar la señal de PestanaSeguimiento
        self.pestana_seguimiento.id_avaluo_seleccionado.connect(self.recibir_id_avaluo)
        
        
        main_layout.addWidget(self.tab_panel)
        
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)
    
    def obtener_conexion_db(self):
        """
        Retorna una instancia de DB con las credenciales del usuario autenticado.
        Las pestañas pueden llamar este método para obtener una conexión a la base de datos.
        
        Ejemplo de uso desde una pestaña:
            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()
            # Realizar operaciones...
            db.cerrar_conexion()
        """
        db = DB(
            host=self.db_host,
            database=self.basededatos,
            user=self.usuario_autenticado,
            password=self.password_usuario
        )
        return db
    
    def get_usuario_info(self):
        """
        Retorna información del usuario autenticado.
        Útil para mostrar en la interfaz o para auditoría.
        """
        return {
            'usuario': self.usuario_autenticado,
            'base_datos': self.basededatos,
            'host': self.db_host
        }

    def on_tab_changed(self, tab_panel, index):
        print(f"Cambio a la pestaña con índice: {index}")
        if self.pestana_anterior == None:
            self.pestana_anterior = index
        else:
            # Obtén el widget actual de la pestaña
            pestana_actual = tab_panel.widget(self.pestana_anterior)
            # Verifica si tiene el atributo mi_pestana
            if hasattr(pestana_actual, "mi_pestana"):
                instancia_real = pestana_actual.mi_pestana
                print(f"la pestaña anterior es: {instancia_real} con index {self.pestana_anterior}")
                if hasattr(instancia_real, "on_tab_changed"):
                    instancia_real.on_tab_changed(tab_panel, self.pestana_anterior)
            self.pestana_anterior = index

    def create_tray_icon_with_file(self):
        self.tray_icon = QSystemTrayIcon()
        try:
            icon = QIcon("./Logo.png")  # Usa la ruta correcta
            self.tray_icon.setIcon(icon)
        except Exception:
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.GlobalColor.red)
            self.tray_icon.setIcon(QIcon(pixmap))
        self.tray_icon.show()
        
    def volver_a_seguimiento(self):
        
        """
        Vuelve a la pestaña de seguimiento y cierra las demás pestañas.
        """
        self.file_proyecto.menuAction().setVisible(False)  # Ocultar menú Proyecto
        
        try:
            # Crear las pestañas con el id_avaluo            
            
            for index in range(self.tab_panel.count()):
                
                """ widget = self.tab_panel.widget(index)
                validacion=(self.tab_panel.tabText(index) == "PestanaDatosSolicitud") """
                print(f"Cerrando pestaña: {self.tab_panel.tabText(index)} con idex {index}")
                
                self.tab_panel.removeTab(0)
                
            
            # Crear las pestaña seguimiento
            self.pestana_seguimiento = PestanaSeguimiento(self.tab_panel, ventana_principal=self)
            
            # Conectar la señal de Pestaña Seguimiento
            self.pestana_seguimiento.id_avaluo_seleccionado.connect(self.recibir_id_avaluo)
                
            
    
        except Exception as e:
            print(f"Error al agregar las pestañas: {e}") 
    
    def recibir_id_avaluo(self, id_avaluo):
        """
        Maneja el id_avaluo recibido desde PestanaSeguimiento.
        """
        print(f"ID Avaluo recibido en Index: {id_avaluo}")
        # Pasar el id_avaluo a la pestaña Datos de Solicitud
        self.id_avaluo = id_avaluo
        self.file_proyecto.menuAction().setVisible(True)  # Mostrar menú Proyecto al abrir avalúo
    
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
        """Abre el directorio del proyecto desde path_trabajo en la base de datos"""
        try:
            # Verificar que hay un avalúo seleccionado
            if not hasattr(self, 'id_avaluo') or self.id_avaluo is None:
                QMessageBox.warning(self, "Advertencia", "No hay ningún avalúo seleccionado")
                return
            
            # Conectar a la base de datos
            db = self.obtener_conexion_db()
            db.conectar()
            
            # Consultar el path_trabajo
            consulta = """
                SELECT path_trabajo 
                FROM "Avaluos" 
                WHERE "Avaluo_id" = %s
            """
            resultado = db.consultar(consulta, (self.id_avaluo,))
            
            if resultado and resultado[0][0]:
                path_trabajo = resultado[0][0]
                
                # Verificar que el directorio existe
                if os.path.exists(path_trabajo):
                    # Abrir el explorador de archivos en el directorio
                    subprocess.run(['xdg-open', path_trabajo])
                else:
                    QMessageBox.warning(self, "Directorio no encontrado", 
                                      f"El directorio no existe:\n{path_trabajo}")
            else:
                QMessageBox.information(self, "Sin directorio", 
                                       "No se ha configurado un directorio de trabajo para este avalúo")
            
            db.cerrar_conexion()
            
        except Exception as e:
            print(f"Error al abrir el directorio del proyecto: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir el directorio: {str(e)}")
        
    
    def iniciar_generacion(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_progreso)
        self.timer.start(100)
    
    def iniciar_generacion_ficha_predial(self):
        """Inicia el proceso de generación de la ficha predial"""
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_progreso_ficha)
        self.timer.start(100)
    
    def actualizar_progreso(self):
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
        else:
            self.timer.stop()
            self.procesar_informe()
            self.progress_bar.hide()
    
    def actualizar_progreso_ficha(self):
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
        else:
            self.timer.stop()
            self.procesar_ficha_predial()
            self.progress_bar.hide()
    
    def procesar_informe(self):
        
        print("El id avaluo actual es:", getattr(self, 'id_avaluo', None))
        self.id_avaluo = getattr(self, 'id_avaluo', None)
        
        # Conectar a la base de datos
        db = DB(host="localhost", database=self.basededatos, user=usuario_global, password=password_global)
        db.conectar()           
        
        
        # Recolectar datos de todas las pestañas
        success, resultado = False, "No se ha iniciado la generación del informe." 
        try:
                        
            print(f"Cargando datos para el avalúo con ID: {self.id_avaluo}")
    
            # Consulta SQL para obtener los datos de la solicitud
            consulta = """
            select a.nombre_cliente , a.id_cliente , a.destinatario, a.fecha_visita ,a.fecha_avaluo , a.tipo_avaluo, a.file_path
            FROM "Avaluos" a 
            left join inmuebles i on a."Avaluo_id" = i.avaluo_id 
            WHERE a."Avaluo_id" = 2
            """.replace("2", str(self.id_avaluo))
            
            resultado = db.consultar(consulta)
            
            if self.default_save_path == "" and resultado[0][6] == None:
                QMessageBox.warning(self, "Ubicación no seleccionada", 
                                    "Por favor, selecciona una ubicación para guardar el informe.")
                self.crea_proyecto()
                
            
            
            # Verificar si se encontraron datos
            
            if self.file_path == None and resultado[0][6] == None:
                
                self.file_path = f"{self.default_save_path}/informe_{time.strftime('%Y%m%d-%H%M%S')}.tex"
                print("Guardando en:", self.file_path)
                db.insertar(
                    """UPDATE "Avaluos" SET file_path = %s WHERE "Avaluo_id" = %s"""
                    , (self.file_path, str(self.id_avaluo)))
                print("Path guardado:", self.file_path)
                
            else:
                self.file_path = resultado[0][6]
                print("Ruta del archivo:", self.file_path)
                
            if resultado:       
                  
                success, resultado = self.generar_informe(resultado, "./Base/Informe.tex",self.file_path)             

            else:
                print(f"No se encontraron datos para el avalúo con ID: {self.id_avaluo}")
    
        except Exception as e:
            print(f"Error al cargar los datos de la solicitud: {e}")
        
        # Obtener todas las matrículas
        """ matriculas = []
        for i in range(self.matricula_layout.count()):
            item = self.matricula_layout.itemAt(i)
            if item and isinstance(item, QHBoxLayout):
                line_edit = item.itemAt(0).widget()
                if line_edit and line_edit.text():
                    matriculas.append(line_edit.text()) """

        db.cerrar_conexion()
        
        if success:
            QMessageBox.information(self, "Éxito", f"Informe guardado en:\n{resultado}")
        else:
            QMessageBox.critical(self, "Error", f"Error al generar informe:\n{resultado}")

    def procesar_ficha_predial(self):
        """Procesa y genera la ficha predial del inmueble"""
        print("El id avaluo actual es:", getattr(self, 'id_avaluo', None))
        self.id_avaluo = getattr(self, 'id_avaluo', None)
        
        if not self.id_avaluo:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ningún avalúo.")
            return
        
        # Conectar a la base de datos
        db = DB(host=self.db_host, database=self.basededatos, user=usuario_global, password=password_global)
        db.conectar()
        
        success, resultado = False, "No se ha iniciado la generación de la ficha predial."
        
        try:
            print(f"Cargando datos para la ficha predial del avalúo ID: {self.id_avaluo}")
            
            # Consulta SQL para obtener los datos del inmueble y avalúo
            consulta = """
            SELECT 
                a.nombre_cliente,
                a.id_cliente,
                a.destinatario,
                a.fecha_visita,
                a.fecha_avaluo,
                a.tipo_avaluo,
                i.matricula_inmobiliaria,
                i.tipo_inmueble,
                i.direccion,
                i.barrio,
                m.nombre as municipio,
                d.nombre as departamento,
                i.cedula_catastral,
                i.modo_adquicision,
                i.area_catastro,
                i.area_documentos_juridicos,
                i.area_levantamiento_topografico,
                i.propietario,
                i.id_propietario,
                i.lindero_norte,
                i.lindero_sur,
                i.lindero_Oriental,
                i.lindero_Occidental,
                i.doc_propiedad,
                a.zona,
                CONCAT(p.nombre, ' ', p.apellido) as perito_nombre,
                p.id_peritos,
                i.longitud,
                i.latitud,
                i.numpre,
                i.limitaciones,
                i.topografia,
                cs.descripcion_usos,
                us.path_imagen,
                a.path_trabajo
            FROM "Avaluos" a
            LEFT JOIN inmuebles i ON a."Avaluo_id" = i.avaluo_id
            LEFT JOIN municipios m ON i.municipio = m.id
            LEFT JOIN departamentos d ON i.departamento = d.id
            LEFT JOIN peritos p ON a.id_peritos = p.id_peritos
            left join caracteristicas_sector cs on a."Avaluo_id" = cs.id_avaluo
            left join usos_sector us  on cs.id  = us.caracteristicas_sector_id 
            WHERE a."Avaluo_id" = %s
            """
            
            resultado_consulta = db.consultar(consulta, (self.id_avaluo,))
            
            if not resultado_consulta:
                QMessageBox.warning(self, "Error", "No se encontraron datos para el avalúo seleccionado.")
                db.cerrar_conexion()
                return
            
            # Determinar la ruta de guardado
            
            
            self.default_save_path = resultado_consulta[0][34] or self.default_save_path
            print("Ruta de guardado obtenida de la base de datos:", self.default_save_path)
            
            # Generar nombre de archivo para la ficha predial
            ficha_path = f"{self.default_save_path}/Ficha_Predial/ficha_predial_{self.id_avaluo}.tex"
            print("Ruta de guardado para ficha predial:", ficha_path)
            print("Guardando ficha predial en:", ficha_path)
            
            # Generar la ficha predial
            success, resultado = self.generar_ficha_predial(
                resultado_consulta[0], 
                "./FICHA_PREDIAL_LATEX/FICHA_V3.tex",
                ficha_path
            )
            
        except Exception as e:
            print(f"Error al procesar la ficha predial: {e}")
            success = False
            resultado = str(e)
        
        db.cerrar_conexion()
        
        if success:
            QMessageBox.information(self, "Éxito", f"Ficha predial guardada en:\n{resultado}")
        else:
            QMessageBox.critical(self, "Error", f"Error al generar ficha predial:\n{resultado}")

    def generar_informe(self, texto, template_path="Base/Informe.tex", output_name="../Resultados/informe"):
        """
        Genera un informe LaTeX desde una plantilla y texto dinámico.
        
        Args:
            texto (str): Contenido a insertar
            template_path (str): Ruta de la plantilla .tex
            output_name (str): Nombre base del archivo de salida
        """
        
        # Leer plantilla
        print("template_path", output_name)

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                plantilla = f.read()
        except FileNotFoundError:
            print(f"Error: No se encontró {template_path}")
            return

        # Escapar caracteres especiales de LaTeX
        #texto_procesado = texto.replace("&", "\&").replace("%", "\%").replace("$", "\$")
        cliente= texto[0][0]
        documento_id=str(texto[0][1])
        destinatario=texto[0][2]
        fecha_visita=texto[0][3].date().strftime("%d/%m/%Y")
        fecha_informe=texto[0][4].date().strftime("%d/%m/%Y") 
        tipo_avaluo = texto[0][5]
        # Reemplazar marcadores en la plantilla
        informe_final = plantilla.replace("%CLIENTE%", cliente)
        informe_final = informe_final.replace("%DOCUMENTO_ID%", documento_id)
        informe_final = informe_final.replace("%DESTINATARIO%", destinatario)
        informe_final = informe_final.replace("FECHA_VISITA%", fecha_visita)
        informe_final = informe_final.replace("FECHA_INFORME%", fecha_informe)
        informe_final = informe_final.replace("%TIPO_AVALUO%", tipo_avaluo)       
        
        # Guardar archivo .tex
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(informe_final)
            print(f"Archivo .tex guardado en {output_name}")
            
        # Compilar el archivo .tex a PDF
        try:
            print(f"Compilando {output_name} a PDF...")
            subprocess.run(["pdflatex", output_name], check=True,cwd=os.path.dirname(os.path.abspath(output_name)))  # Establecer el directorio de trabajo)
            subprocess.run(["pdflatex", output_name], check=True,cwd=os.path.dirname(os.path.abspath(output_name)))  # Se ejecuta dos veces para referencias cruzadas)
            print(f"PDF generado correctamente: {output_name}.pdf")

            # Retornar el archivo PDF generado
            return True, f"{output_name}.pdf"
        except subprocess.CalledProcessError as e:
            print(f"Error al compilar el archivo .tex: {e}")
            return False, None
        except FileNotFoundError:
            print("Error: El comando 'pdflatex' no se encontró. Asegúrate de que está instalado y en el PATH.")
            return False, None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False, None
            
            
        
        # Compilar a PDF
        try:
            subprocess.run(["pdflatex", f"{output_name}.tex"], check=True)
            print(f"\nPDF generado: {output_name}.pdf")
            
            # Limpiar archivos auxiliares
            for ext in [".aux", ".log", ".out"]:
                archivo = f"{output_name}{ext}"
                if os.path.exists(archivo):
                    os.remove(archivo)
            
                 
        except FileNotFoundError:
            print("\n¡Error! Necesitas LaTeX instalado (pdflatex)")
    
    def generar_ficha_predial(self, datos, template_path="FICHA_PREDIAL_LATEX/FICHA_V3.tex", output_name="ficha_predial"):
        """
        Genera una ficha predial LaTeX desde una plantilla con los datos del inmueble.
        
        Args:
            datos (tuple): Tupla con los datos del inmueble y avalúo
            template_path (str): Ruta de la plantilla .tex
            output_name (str): Nombre base del archivo de salida
            
        Returns:
            tuple: (success: bool, resultado: str con la ruta del PDF o mensaje de error)
        """
        
        try:
            # Leer plantilla
            with open(template_path, "r", encoding="utf-8") as f:
                plantilla = f.read()
        except FileNotFoundError:
            print(f"Error: No se encontró {template_path}")
            return False, f"No se encontró la plantilla: {template_path}"
        
        try:
            # Extraer datos de la tupla
            cliente = datos[0] or ""
            doc_identidad = str(datos[1]) if datos[1] else ""
            destinatario = datos[2] or ""
            fecha_visita = datos[3].strftime("%d/%m/%Y") if datos[3] else ""
            fecha_informe = datos[4].strftime("%d/%m/%Y") if datos[4] else ""
            tipo_avaluo = datos[5] or ""
            matricula = datos[6] or ""
            tipo_inmueble = datos[7] or ""
            direccion = datos[8] or ""
            barrio = datos[9] or ""
            municipio = datos[10] or ""
            departamento = datos[11] or ""
            cedula_catastral = datos[12] or ""
            modo_adquisicion = datos[13] or ""
            area_catastro = str(datos[14]) if datos[14] else "0"
            area_documentos = str(datos[15]) if datos[15] else "0"
            area_levantamiento = str(datos[16]) if datos[16] else "0"
            propietario = datos[17] or ""
            id_propietario = str(datos[18]) if datos[18] else ""
            lindero_norte = datos[19] or ""
            lindero_sur = datos[20] or ""
            lindero_oriental = datos[21] or ""
            lindero_occidental = datos[22] or ""
            doc_propiedad = datos[23] or ""
            zona = datos[24] or ""
            perito = datos[25] or ""
            tarjeta_profesional = str(datos[26]) if datos[26] else ""
            longitud = str(datos[27]) if datos[27] else ""
            latitud = str(datos[28]) if datos[28] else ""
            numpre = str(datos[29]) if datos[29] else ""
            limitaciones = datos[30] or ""
            topografia = datos[31] or ""
            usos = datos[32] or ""
            path_imagen_uso = datos[33] or ""
            
            # Función auxiliar para escapar caracteres especiales de LaTeX
            def escapar_latex(texto):
                if not texto:
                    return ""
                texto = str(texto)
                # Reemplazos básicos para LaTeX
                replacements = {
                    '&': r'\&',
                    '%': r'\%',
                    '$': r'\$',
                    '#': r'\#',
                    '_': r'\_',
                    '{': r'\{',
                    '}': r'\}',
                    '~': r'\textasciitilde{}',
                    '^': r'\^{}',
                    '\\': r'\textbackslash{}',
                }
                for old, new in replacements.items():
                    texto = texto.replace(old, new)
                return texto
            
            # Reemplazar marcadores en la plantilla
            ficha_final = plantilla.replace("%CLIENTE%", escapar_latex(cliente))
            ficha_final = ficha_final.replace("%DOCUMENTO_ID%", escapar_latex(doc_identidad))
            ficha_final = ficha_final.replace("%DESTINATARIO%", escapar_latex(destinatario))
            ficha_final = ficha_final.replace("%FECHA_VISITA%", escapar_latex(fecha_visita))
            ficha_final = ficha_final.replace("%FECHA_INFORME%", escapar_latex(fecha_informe))
            ficha_final = ficha_final.replace("%TIPO_AVALUO%", escapar_latex(tipo_avaluo))
            ficha_final = ficha_final.replace("%MATRICULA%", escapar_latex(matricula))
            ficha_final = ficha_final.replace("%TIPO_INMUEBLE%", escapar_latex(tipo_inmueble))
            ficha_final = ficha_final.replace("%DIRECCION%", escapar_latex(direccion))
            ficha_final = ficha_final.replace("%BARRIO%", escapar_latex(barrio))
            ficha_final = ficha_final.replace("%MUNICIPIO%", escapar_latex(municipio))
            ficha_final = ficha_final.replace("%DEPARTAMENTO%", escapar_latex(departamento))
            ficha_final = ficha_final.replace("%CEDULA_CATASTRAL%", escapar_latex(cedula_catastral))
            ficha_final = ficha_final.replace("%MODO_ADQUISICION%", escapar_latex(modo_adquisicion))
            ficha_final = ficha_final.replace("%AREA_CATASTRO%", escapar_latex(area_catastro))
            ficha_final = ficha_final.replace("%AREA_DOCUMENTOS%", escapar_latex(area_documentos))
            ficha_final = ficha_final.replace("%AREA_LEVANTAMIENTO%", escapar_latex(area_levantamiento))
            ficha_final = ficha_final.replace("%PROPIETARIO%", escapar_latex(propietario))
            ficha_final = ficha_final.replace("%ID_PROPIETARIO%", escapar_latex(id_propietario))
            ficha_final = ficha_final.replace("%LINDERO_NORTE%", escapar_latex(lindero_norte))
            ficha_final = ficha_final.replace("%LINDERO_SUR%", escapar_latex(lindero_sur))
            ficha_final = ficha_final.replace("%LINDERO_ORIENTAL%", escapar_latex(lindero_oriental))
            ficha_final = ficha_final.replace("%LINDERO_OCCIDENTAL%", escapar_latex(lindero_occidental))
            ficha_final = ficha_final.replace("%DOC_PROPIEDAD%", escapar_latex(doc_propiedad))
            ficha_final = ficha_final.replace("%ZONA%", escapar_latex(zona))
            ficha_final = ficha_final.replace("%PERITO%", escapar_latex(perito))
            ficha_final = ficha_final.replace("%TARJETA_PROFESIONAL%", escapar_latex(tarjeta_profesional))
            ficha_final = ficha_final.replace("%LONGITUD%", escapar_latex(longitud))
            ficha_final = ficha_final.replace("%LATITUD%", escapar_latex(latitud))
            ficha_final = ficha_final.replace("%NUMPRE%", escapar_latex(numpre))
            ficha_final = ficha_final.replace("%LIMITACIONES%", escapar_latex(limitaciones))
            ficha_final = ficha_final.replace("%TOPOGRAFIA%", escapar_latex(topografia))
            ficha_final = ficha_final.replace("%USOS%", escapar_latex(usos))
            ficha_final = ficha_final.replace("%PATH_IMAGEN_USO%", escapar_latex(path_imagen_uso))
            
            # Guardar archivo .tex
            with open(output_name, "w", encoding="utf-8") as f:
                f.write(ficha_final)
            print(f"Archivo .tex guardado en {output_name}")
            
            # Compilar el archivo .tex a PDF
            print(f"Compilando {output_name} a PDF...")
            directorio_trabajo = os.path.dirname(os.path.abspath(output_name))
            
            # Ejecutar pdflatex dos veces para resolver referencias cruzadas
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", os.path.basename(output_name)], 
                check=True, 
                cwd=directorio_trabajo,
                capture_output=True
            )
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", os.path.basename(output_name)], 
                check=True, 
                cwd=directorio_trabajo,
                capture_output=True
            )
            
            pdf_path = output_name.replace('.tex', '.pdf')
            print(f"PDF generado correctamente: {pdf_path}")
            
            # Limpiar archivos auxiliares
            base_name = output_name.replace('.tex', '')
            for ext in [".aux", ".log", ".out", ".toc"]:
                archivo_aux = f"{base_name}{ext}"
                if os.path.exists(archivo_aux):
                    try:
                        os.remove(archivo_aux)
                    except:
                        pass
            
            return True, pdf_path
            
        except subprocess.CalledProcessError as e:
            print(f"Error al compilar el archivo .tex: {e}")
            return False, "Error al compilar el documento con pdflatex"
        except FileNotFoundError:
            print("Error: El comando 'pdflatex' no se encontró.")
            return False, "pdflatex no está instalado o no está en el PATH"
        except Exception as e:
            print(f"Error inesperado al generar ficha predial: {e}")
            return False, str(e)
        
if __name__ == "__main__":
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    
    # Configuración adicional para QWebEngineView
    # Esto ayuda a prevenir errores de rendering
    app.setApplicationName("Seshat - Sistema de Avalúos")
    app.setOrganizationName("Interval")
    
    print("[INFO] Aplicación iniciada con configuración anti-Vulkan")
    print(f"[INFO] Qt Version: {app.applicationVersion()}")
    
    # Mostrar diálogo de login
    login_dialog = LoginDialog()
    
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        # Si el login es exitoso, mostrar ventana principal
        print(f"Usuario autenticado: {login_dialog.usuario_autenticado}")
        window = ReportApp(
            usuario_autenticado=login_dialog.usuario_autenticado,
            password_usuario=login_dialog.password_usuario
        )
        window.show()
        sys.exit(app.exec())
    else:
        # Si el login falla o se cancela, cerrar la aplicación
        print("Acceso denegado o cancelado")
        sys.exit(0)