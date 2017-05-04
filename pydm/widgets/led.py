from pydm.PyQt.QtGui import QLabel, QApplication, QColor, QPalette, QWidget
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty, QState, QStateMachine, QPropertyAnimation, QByteArray
from pydm.widgets.channel import PyDMChannel
from .QLed import QLed

class PyDMLed(QLed):

    #Tell Designer what signals are available.
    __pyqtSignals__ = ("connected_signal()",
                       "disconnected_signal()")

    #Internal signals, used by the state machine
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, init_channel=None, bit=0, enum_map={}):
        super(PyDMLed, self).__init__(parent)
        self._value = None

        if bit is not None:
            self._bit = int(bit)
            self._mask = 1 << bit
        else:
            self._bit = None
            self._mask = None

        self._enum_strings = None
        self._enum_map = enum_map

        self._connected = False
        self._channels = None
        self._channel = init_channel

    def pvbit(self): return self._bit
    def setPvBit(self, newBit):
        if newBit >= 0:
            self._bit=newBit
            self.update()
    pvbit=pyqtProperty(int, pvbit, setPvBit)

    # This property is not available to desiner yet
    def enumMap(self): return self._enum_map
    def setEnumMap(self, enum_map):
        self._enum_map = enum_map

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        if connected:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    def receiveValue(self, value):
        if self._enum_strings is None: #PV of type integer or float
            if self._bit is None: #Led represents value of PV
                if isinstance(value, str):
                    value = int(value)
                if value:
                    self.setValue(1)
                else:
                    self.setValue(0)
            else: #Led represents specific bit of PV
                value = int(value)
                bit_val = (value & self._mask) >> self._bit
                self.setValue(bit_val)
        else: #PV of type ENUM
            self.setValue(1)
            if self._enum_map is None:
                self.setOnColour(value)
            else:
                if self._enum_strings is not None and isinstance(value, int):
                    enum_name = self._enum_strings[value]
                    color = self._enum_map[enum_name]
                    self.setOnColour(color)

        #TODO: PV of type array


    @pyqtSlot(tuple)
    def enumStringsChanged(self, enum_strings):
        if enum_strings != self._enum_strings:
            self._enum_strings = enum_strings
            self.receiveValue(self._value)

    def getChannel(self):
        return str(self._channel)
    def setChannel(self, value):
        if self._channel != value:
            self._channel = str(value)
    def resetChannel(self):
        if self._channel != None:
            self._channel = None
    channel = pyqtProperty(str, getChannel, setChannel, resetChannel)

    def channels(self):
        return [PyDMChannel(address=self._channel,
                            connection_slot=self.connectionStateChanged,
                            value_slot=self.receiveValue,
                            enum_strings_slot=self.enumStringsChanged)]
