from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from pydm.widgets.channel import PyDMChannel
from pydm.widgets.QDoubleScrollBar import QDoubleScrollBar


class PyDMScrollBar(QDoubleScrollBar):

    value_changed_signal = pyqtSignal([int], [float], [str])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, orientation=Qt.Horizontal,
                 init_channel=None, step=None, precision=2):
        super(PyDMScrollBar, self).__init__(orientation, parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setDecimals(precision)
        self.setEnabled(False)
        self.setInvertedControls(False)
        if not step:
            self.setSingleStep(1/10**precision)
            self.setPageStep(10/10**precision)
        else:
            self.setSingleStep(step)
            self.setPageStep(10 * step)

        self._limits_from_pv = False
        self._connected = False
        self._channels = None
        self._channel = init_channel
        self._ch_typ = None
        self._value = self.value
        self._update_tooltip()

        self.setTracking(True)
        self.actionTriggered.connect(self.value_changed)

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        self.setEnabled(connected)
        if connected:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()
        self._update_tooltip()

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def receiveValue(self, value):
        self._ch_typ = type(value)
        self._value = value
        self.setValue(float(value))

    @pyqtSlot(int)
    @pyqtSlot(float)
    def value_changed(self, value):
        ''' Emits a value changed signal '''
        value = self.sliderPosition
        if self._connected and self._ch_typ is not None:
            self.value_changed_signal[self._ch_typ].emit(self._ch_typ(value))

    @pyqtSlot(float)
    @pyqtSlot(int)
    def receiveLowerLimit(self, value):
        if self._limits_from_pv:
            self.setMinimum(float(value))
            self._update_tooltip()

    @pyqtSlot(float)
    @pyqtSlot(int)
    def receiveUpperLimit(self, value):
        if self._limits_from_pv:
            self.setMaximum(float(value))
            self._update_tooltip()

    @pyqtSlot(int)
    def receivePrec(self, value):
        if self._limits_from_pv and value != self.getDecimals():
            self.setDecimals(round(value))
            self.setSingleStep(1/10**value)
            self.setPageStep(10/10**value)
            self._update_tooltip()

    # Designer Properties
    @pyqtProperty(str)
    def channel(self):
        return str(self._channel)

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = str(value)
            self._update_tooltip()

    @pyqtProperty(bool)
    def limitsFromPV(self):
        return bool(self._limits_from_pv)

    @limitsFromPV.setter
    def limitsFromPV(self, value):
        if self._limits_from_pv != value:
            self._limits_from_pv = bool(value)

    def channels(self):
        if self._channels is None:
            self._channels = [PyDMChannel(
                address=self._channel,
                connection_slot=self.connectionStateChanged,
                value_slot=self.receiveValue,
                value_signal=self.value_changed_signal,
                lower_disp_limit_slot=self.receiveLowerLimit,
                upper_disp_limit_slot=self.receiveUpperLimit,
                prec_slot=self.receivePrec)]
        return self._channels

    def _update_tooltip(self):
        fmt = '{0:.' + '{0:d}'.format(self.decimals()) + 'f}'
        toltp = (self._channel or '') + '\n'
        if self.isEnabled():
            toltp += 'min: ' + fmt.format(self.minimum()) + '\n'
            toltp += 'max: ' + fmt.format(self.maximum()) + '\n'
            toltp += 'step: ' + fmt.format(self.singleStep()) + '\n'
        self.setToolTip(toltp)
