import datetime as _datetime
from pydm.PyQt.QtGui import QListWidget, QColor
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from pydm.widgets.channel import PyDMChannel

## Possible Improvements:
#   - Set color of log according to alarmSeverity

class PyDMLogLabel(QListWidget):
    #Tell Designer what signals are available.
    __pyqtSignals__ = ("send_value_signal(str)",
                       "connected_signal()",
                       "disconnected_signal()")

    #Internal signals, used by the state machine
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    #Usually, this widget will get this from its parent pydm application.  However, in Designer, the parent isnt a pydm application, and doesn't know what a color map is.  The following two color maps are provided for that scenario.
    local_alarm_severity_color_map = {
        0: QColor(0, 0, 0), #NO_ALARM
        1: QColor(200, 200, 20), #MINOR_ALARM
        2: QColor(240, 0, 0), #MAJOR_ALARM
        3: QColor(240, 0, 240) #INVALID_ALARM
    }
    local_connection_status_color_map = {
        False: QColor(0, 0, 0),
        True: QColor(0, 0, 0,)
    }

    def __init__(self, parent=None, init_channel=None):
        super(PyDMLogLabel, self).__init__(parent)
        self._channels = None
        self._channel = init_channel
        self._connected = False
        self._max_count = 1000
        self._prec = 0
        self.format_string = None
        self.enum_strings = None

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def receiveValue(self, new_value):
        if self.count() > self._max_count: self.clear()
        now_ = _datetime.datetime.now().strftime('%Y/%M/%d-%H:%M:%S')
        if self.enum_strings and isinstance(new_value, int):
            new_value = self.enum_strings[new_value]
        elif isinstance(new_value, float) and self.format_string:
            new_value = self.format_string.format(new_value)
        else:
            new_value = str(new_value)
        self.addItem(now_+ '  ' + new_value)

    #false = disconnected, true = connected
    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        if connected:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()

    @pyqtSlot(tuple)
    def enumStringsChanged(self, enum_strings):
        if enum_strings != self.enum_strings:
            self.enum_strings = enum_strings
            self.receiveValue(self.value)

    @pyqtProperty(str)
    def channel(self): return str(self._channel)
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = str(value)

    @pyqtProperty(int)
    def precision(self): return self._prec
    @precision.setter
    def precision(self, new_prec):
        if self._prec != int(new_prec) and new_prec >= 0:
            self._prec = int(new_prec)
            self.format_string = "{:." + str(self._prec) + "f}"

    @pyqtProperty(int)
    def maxCount(self): return int(self._max_count)
    @maxCount.setter
    def maxCount(self,value): self._max_count = int(value)

    def channels(self):
      if self._channels != None:
        return self._channels
      self._channels = [PyDMChannel(address=self.channel,
                                    connection_slot=self.connectionStateChanged,
                                    value_slot=self.receiveValue,
                                    enum_strings_slot=self.enumStringsChanged)]
      return self._channels
