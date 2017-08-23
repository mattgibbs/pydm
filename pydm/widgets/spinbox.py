from pydm.PyQt.QtGui import QDoubleSpinBox, QInputDialog
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from pydm.widgets.channel import PyDMChannel


class PyDMSpinBox(QDoubleSpinBox):

    value_changed_signal = pyqtSignal([int], [float], [str])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, init_channel=None, limits_from_pv=False,
                 alignment=Qt.AlignCenter, step=None, precision=2):
        super(PyDMSpinBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setAlignment(alignment)
        self.setDecimals(precision)
        if not step:
            self.setSingleStep(1/10**precision)
        else:
            self.setSingleStep(step)
        self.setEnabled(False)

        self._limits_from_pv = limits_from_pv
        self._connected = False
        self._channels = None
        self._channel = init_channel
        self._ch_typ = None
        self._value = self.value()
        self._update_tooltip()

        self.valueChanged.connect(self.value_changed)  # signal from spinbox
        self.setKeyboardTracking(False)
        self.setAccelerated(True)

    @pyqtSlot(bool)
    def dialogSingleStep(self, value):
        mini = 1/10**self.decimals()
        maxi = (self.maximum() - self.minimum())/10
        d, okP = QInputDialog.getDouble(self, "Single Step", "Single Step:",
                                        self.singleStep(), mini, maxi,
                                        self.decimals())
        if okP:
            self.setSingleStep(d)
            self._update_tooltip()

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        self.setEnabled(connected)
        if connected:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()
        self._update_tooltip()

    def contextMenuEvent(self, ev):
        menu = self.lineEdit().createStandardContextMenu()
        menu.addSeparator()
        ac = menu.addAction('Set Single Step')
        ac.triggered.connect(self.dialogSingleStep)
        menu.exec_(ev.globalPos())

    def keyPressEvent(self, event):
        singlestep = self.singleStep()
        if (event.key() == Qt.Key_Plus):
            self.setSingleStep(10*singlestep)
            self._update_tooltip()
        elif (event.key() == Qt.Key_Minus):
            self.setSingleStep(0.1*singlestep)
            self._update_tooltip()
        else:
            super().keyPressEvent(event)

    @pyqtSlot(str)
    @pyqtSlot(int)
    @pyqtSlot(float)
    def receiveValue(self, value):
        self._ch_typ = type(value)
        self._value = value
        self._valueBeingSet = True
        self.setValue(float(value))
        self._valueBeingSet = False

    @pyqtSlot(float)
    def value_changed(self, value):
        ''' Emits a value changed signal '''
        if self._connected and \
           self._ch_typ is not None and \
           not self._valueBeingSet:
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
        if self._limits_from_pv and value != self.decimals():
            self.setDecimals(round(value))
            self.setSingleStep(1/10**value)
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
