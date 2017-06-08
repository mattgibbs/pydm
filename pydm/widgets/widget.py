import numpy as _np
from pydm.PyQt.QtGui import QWidget
from pydm.PyQt.QtCore import pyqtSignal, pyqtSlot, pyqtProperty


class PyDMWidget(QWidget):
    _send_value_to_pv_signal = pyqtSignal([int],[float],[str],[_np.ndarray])
    value_signal = pyqtSignal([int],[float],[str],[_np.ndarray])
    enum_strings_signal = pyqtSignal(tuple)
    alarm_severity_signal = pyqtSignal(int)
    connected_signal = pyqtSignal(bool)
    write_access_signal = pyqtSignal(bool)
    unit_signal = pyqtSignal(str)
    precision_signal = pyqtSignal(int)
    count_signal = pyqtSignal(int)

    ALARM_NONE = 0
    ALARM_MINOR = 1
    ALARM_MAJOR = 2
    ALARM_INVALID = 3
    ALARM_DISCONNECTED = 4

    def __init__(self,parent=None,init_channel=None):
        super(PyDMWidget,self).__init__(parent)
        self._channel = init_channel
        self._channels = None
        self._connected = False

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    @pyqtSlot(_np.ndarray)
    def receiveValue(self, new_value):
        type_ = type(new_value)
        self.value_signal[type_].emit(new_value)

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    @pyqtSlot(_np.ndarray)
    def sendValue(self, new_value):
        type_ = type(new_value)
        self._send_value_signal_to_pv[type_].emit(new_value)

    @pyqtSlot(bool)
    def receiveConnectionState(self, connected):
        self._connected = connected
        self.connected_signal.emit(connected)

    @pyqtSlot(bool)
    def receiveWriteAccess(self, write_access):
        self.write_access_signal.emit(write_access)

    @pyqtSlot(str)
    def receiveUnit(self, unit):
        self.unit_signal.emit(unit)

    @pyqtSlot(int)
    def receivePrec(self, prec):
        self.precision_signal.emit(prec)

    @pyqtSlot(int)
    def receivePrec(self, count):
        self.count_signal.emit(count)

    @pyqtSlot(int)
    def receiveAlarmSeverity(self, new_alarm_severity):
        if not self._connected:
            new_alarm_severity = self.ALARM_DISCONNECTED
        self.alarm_severity_signal.emit(new_alarm_severity)

    @pyqtSlot(tuple)
    def receiveEnumStrings(self, enum_strings):
        self.enum_strings_signal.emit(enum_strings)

    @pyqtProperty(str)
    def channel(self): return str(self._channel)
    @channel.setter
    def channel(self,value): self._channel = str(value)

    def channels(self):
        if self._channels is None:
            self._channels = [PyDMChannel(address=self.channel,
                                          connection_slot=self.receiveConnectionState,
                                          value_slot=self.receiveValue,
                                          waveform_slot=self.receiveValue,
                                          severity_slot=self.receiveAlarmSeverity,
                                          write_access_slot=self.receiveWriteAccess,
                                          enum_strings_slot=self.receiveEnumStrings,
                                          unit_slot=self.receiveUnit,
                                          prec_slot=self.receivePrec,
                                          count_slot=self.receiveCount,
                                          value_signal=self._send_value_to_pv_signal,
                                          waveform_signal=self._send_value_to_pv_signal ) ]
        return self._channels
