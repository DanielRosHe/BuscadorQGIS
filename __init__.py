def classFactory(iface):
    from .buscador import BuscadorPlugin
    return BuscadorPlugin(iface)
