import numpy as _np
from pydm.PyQt.QtCore import pyqtSignal, pyqtSlot, pyqtProperty
from pydm.widgets.channel import PyDMChannel
from pydm.widgets.QLed import QLed

class PyDMLed(QLed):

    #Tell Designer what signals are available.
    __pyqtSignals__ = ("connected_signal()",
                       "disconnected_signal()")

    #Internal signals, used by the state machine
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, init_channel='', bit=-1, enum_map=None):
        super(PyDMLed, self).__init__(parent)
        self._value = None
        self.pvbit = bit

        self._enum_strings = None
        self._enum_map = enum_map
        self._count = None
        self._isArray = False

        self._connected = False
        self._channels = None
        self._channel = init_channel
        self.setEnabled(False)

    @pyqtProperty(int)
    def pvbit(self): return self._bit
    @pvbit.setter
    def pvbit(self, bit):
        self._bit = -1
        self._mask = None
        if bit >= 0 :
            self._bit = int(bit)
            self._mask = 1 << bit

    # This property is not available to designer yet
    def enumMap(self): return self._enum_map
    def setEnumMap(self, enum_map):
        self._enum_map = enum_map

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        self.setEnabled(connected)
        if connected:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    def receiveValue(self, value):
        if self._enum_strings is None: #PV of type integer or float
            value = int(value)
            if self._bit < 0: #Led represents value of PV
                self.setValue(1 if value else 0)
            else: #Led represents specific bit of PV
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

    @pyqtSlot(_np.ndarray)
    def receiveWaveform(self,value):
        self._isArray = True
        if self._bit < 0: return
        if self._bit >= self._count: return
        self.setValue(1   if value[self._bit] else   0)

    @pyqtSlot(int)
    def receiveCount(self,value):
        self._count = int(value)

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
                            enum_strings_slot=self.enumStringsChanged,
                            waveform_slot = self.receiveWaveform,
                            count_slot = self.receiveCount)]
