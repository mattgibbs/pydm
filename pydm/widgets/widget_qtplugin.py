from .qtplugin_base import qtplugin_factory
from .widget import PyDMWidget

PyDMWidgetPlugin = qtplugin_factory(PyDMWidget, is_container=True)
