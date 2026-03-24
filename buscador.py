from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
import os.path

# Importamos nuestro widget
from .buscador_dockwidget import BuscadorDinamicoDockWidget

class BuscadorPlugin:
    """Clase principal del Plugin de QGIS."""

    def __init__(self, iface):
        """Constructor."""
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        
        # Inicializamos variables
        self.dockwidget = None
        self.action = None

    def initGui(self):
        """Se ejecuta al cargar el plugin en QGIS."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        
        # Crear la acción que abrirá el plugin
        self.action = QAction(
            QIcon(icon_path),
            "Buscador Dinámico",
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)

        # Añadir al menú de Plugins y a la barra de herramientas
        self.iface.addPluginToMenu("&Buscador Dinámico", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        """Se ejecuta al desactivar el plugin."""
        if self.action:
            self.iface.removePluginMenu("&Buscador Dinámico", self.action)
            self.iface.removeToolBarIcon(self.action)
        
        if self.dockwidget:
            self.iface.removeDockWidget(self.dockwidget)

    def run(self):
        """Ejecuta el plugin."""
        if not self.dockwidget:
            self.dockwidget = BuscadorDinamicoDockWidget()
        
        # Mostrar el dock widget
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
        self.dockwidget.show()
