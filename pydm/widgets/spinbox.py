import time, math
from pydm.PyQt.QtGui import QDoubleSpinBox, QInputDialog
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from pydm.widgets.channel import PyDMChannel

class PyDMSpinBox(QDoubleSpinBox):

    value_changed_signal = pyqtSignal([int],[float],[str])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, init_channel=None, alignment=Qt.AlignCenter,step=None, precision=2):
        super(PyDMSpinBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAlignment(alignment)
        self.setSingleStep(step or 10)
        self.setDecimals(precision)
        self.setEnabled(False)

        self._limits_from_pv = False
        self._connected = False
        self._channels = None
        self._channel = init_channel
        self._channeltype = None

        self.valueChanged.connect(self.value_changed) # signal from spinbox

    @pyqtSlot()
    def changeStep(self):
        d, okPressed = QInputDialog.getDouble(self, "Get double","Value:", self.singleStep(), 0.1, 5, 1)
        if okPressed:
            self.setSingleStep(d)

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        if connected:
            self.setEnabled(True)
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()
            self.setEnabled(False)

    @pyqtSlot(float)
    @pyqtSlot(int)
    def receiveValue(self, value):
        self._channeltype = type(value)
        self.value = self._channeltype(value)

    @pyqtSlot()
    def value_changed(self):
        ''' Emits a value changed signal '''
        if self._connected:
            if self.value() <= self.minimum():
                self.value_changed_signal[self._channeltype].emit(self._channeltype(self.minimum()))
            elif self.value() >= self.maximum():
                self.value_changed_signal[self._channeltype].emit(self._channeltype(self.maximum()))
            else:
                self.value_changed_signal[self._channeltype].emit(self._channeltype(self.value))

    @pyqtSlot(float)
    def receiveLowerLimit(self, value):
        if self._limits_from_pv: self.setMinimum(value)
    @pyqtSlot(float)
    def receiveUpperLimit(self, value):
        if self._limits_from_pv: self.setMaximum(value)
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
