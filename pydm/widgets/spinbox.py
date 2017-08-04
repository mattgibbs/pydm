import time, math
from pydm.PyQt.QtGui import QDoubleSpinBox, QInputDialog
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from pydm.widgets.channel import PyDMChannel

class PyDMSpinBox(QDoubleSpinBox):

    value_changed_signal = pyqtSignal([int],[float],[str])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, init_channel=None,
                 alignment=Qt.AlignCenter, step=10, precision=2):
        super(PyDMSpinBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAlignment(alignment)
        self.setSingleStep(step)
        self.setDecimals(precision)
        self.setEnabled(False)

        self._limits_from_pv = False
        self._connected = False
        self._channels = None
        self._channel = init_channel
        self._channeltype = None
        self._value = self.value()

        self.valueChanged.connect(self.value_changed)  # signal from spinbox
        self.setKeyboardTracking(False)
        self.setAccelerated(True)

    @pyqtSlot()
    def changeStep(self):
        d, okPressed = QInputDialog.getDouble(self, "Get double","Value:", self.singleStep(), 0.1, 5, 1)
        if okPressed:
            self.setSingleStep(d)

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        self.setEnabled(connected)
        if connected:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()

    @pyqtSlot(str)
    @pyqtSlot(int)
    @pyqtSlot(float)
    def receiveValue(self, value):
        self._channeltype = type(value)
        if not self._isEqual(value):
            self._value = value
            self.setValue(float(value))

    @pyqtSlot(float)
    def value_changed(self,value):
        ''' Emits a value changed signal '''
        if self._connected and self._channeltype is not None and not self._isEqual(value):
            self.value_changed_signal[self._channeltype].emit(self._channeltype(value))

    def _isEqual(self,value):
        scale = 10**self.decimals()
        return True if int(self._value*scale) == int(value*scale) else False

    @pyqtSlot(float)
    @pyqtSlot(int)
    def receiveLowerLimit(self, value):
        if self._limits_from_pv: self.setMinimum(float(value))
    @pyqtSlot(float)
    @pyqtSlot(int)
    def receiveUpperLimit(self, value):
        if self._limits_from_pv: self.setMaximum(float(value))
    @pyqtSlot(int)
    def receivePrec(self, value):
        if self._limits_from_pv: self.setDecimals(int(value))

    #Designer Properties
    @pyqtProperty(str)
    def channel(self): return str(self._channel)
    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = str(value)

    @pyqtProperty(bool)
    def limitsFromPV(self): return bool(self._limits_from_pv)
    @limitsFromPV.setter
    def limitsFromPV(self, value):
        if self._limits_from_pv != value:
            self._limits_from_pv = bool(value)

    def channels(self):
        if self._channels is None:
            self._channels = [PyDMChannel(  address=self._channel,
                                            connection_slot=self.connectionStateChanged,
                                            value_slot=self.receiveValue,
                                            value_signal=self.value_changed_signal,
                                            lower_disp_limit_slot=self.receiveLowerLimit,
                                            upper_disp_limit_slot=self.receiveUpperLimit,
                                            prec_slot=self.receivePrec)]
        return self._channels
