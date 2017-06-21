import numpy as _np
from ..PyQt.QtGui import QCheckBox, QApplication, QColor, QPalette
from ..PyQt.QtCore import pyqtSignal, pyqtSlot, pyqtProperty, QState, QStateMachine, QPropertyAnimation
from .channel import PyDMChannel

class PyDMCheckbox(QCheckBox):
    __pyqtSignals__ = ("connected_signal()",
                     "disconnected_signal()",
                     "no_alarm_signal()",
                     "minor_alarm_signal()",
                     "major_alarm_signal()",
                     "invalid_alarm_signal()")

    #Emitted when the user changes the value.
    send_value_signal = pyqtSignal(str)
    send_waveform_signal = pyqtSignal(_np.ndarray)

    def __init__(self, parent=None, init_channel=None, bit=-1):
        super(PyDMCheckbox, self).__init__(parent)
        self._channel = init_channel
        self._channels = None
        self._connected = False
        self._write_access = False
        self.checkEnableState()
        self.pvbit = bit
        self._value = None
        self._count = -2
        self._isArray = False
        self.clicked.connect(self.sendValue)
        self.clicked.connect(self.sendWaveform)

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    def receiveValue(self, value):
        self._isArray = False
        self._value = int(value)
        value = int(value)
        if self._bit >= 0:#Led represents specific bit of PV
            value = (value >> self._bit) & 1 # shifts value _bit times to the right and bitwise and with 1
        self.setChecked(True if value else False)

    @pyqtSlot(_np.ndarray)
    def receiveWaveform(self,value):
        self._isArray = True
        self._value = value
        if self._bit < 0 or self._count is None: return
        if self._bit >= self._count: return
        self.setChecked(True   if value[self._bit] else   False)

    @pyqtSlot(int)
    def receiveCount(self,value):
        self._count = int(value)

    @pyqtSlot(bool)
    def sendValue(self, checked):
        if self._isArray: return
        new_val = 1 if checked else 0
        if self._bit >=0:
            new_val = int(self._value)
            new_val ^= (-checked ^ new_val) & (1 << self._bit) #I didn't try to understand: https://stackoverflow.com/questions/47981/how-do-you-set-clear-and-toggle-a-single-bit
        self.send_value_signal.emit(str(new_val))

    @pyqtSlot(bool)
    def sendWaveform(self,checked):
        if self._bit < 0 or not self._isArray: return
        if self._bit >= self._count: return
        wave = self._value.copy()
        wave[self._bit] = 1 if checked else 0
        self.send_waveform_signal.emit(wave)

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        self.checkEnableState()

    @pyqtSlot(bool)
    def writeAccessChanged(self, write_access):
        self._write_access = write_access
        self.checkEnableState()

    def checkEnableState(self):
        self.setEnabled(self._write_access and self._connected)

    @pyqtProperty(str)
    def channel(self):
        return str(self._channel)
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = str(value)

    @pyqtProperty(int)
    def pvbit(self):
        return int(self._bit)
    @pvbit.setter
    def pvbit(self, bit):
        self._bit = -1
        if bit >= 0 :
            self._bit = int(bit)

    def channels(self):
        if self._channels is None:
            self._channels = [PyDMChannel(address=self.channel,
                                          connection_slot=self.connectionStateChanged,
                                          value_slot=self.receiveValue,
                                          waveform_slot=self.receiveWaveform,
                                          count_slot=self.receiveCount,
                                          write_access_slot=self.writeAccessChanged,
                                          value_signal=self.send_value_signal,
                                          waveform_signal=self.send_waveform_signal)]
        return self._channels
