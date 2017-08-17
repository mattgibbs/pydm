"""Module that defines PyDMScrollBar."""
from pydm.widgets.channel import PyDMChannel
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from pydm.PyQt.QtGui import QScrollBar


class PyDMScrollBar(QScrollBar):
    """Again."""

    value_changed_signal = pyqtSignal([int],[float],[str])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self,
                 parent=None,
                 orientation=Qt.Horizontal,
                 init_channel=None,
                 precision=6):
        """Constructor."""
        super().__init__(orientation, parent)
        self.setFocusPolicy(Qt.StrongFocus)

        self._channel = init_channel
        self._channels = None
        self._display_value = 0.0

        self._precision = precision

        self._received_value = False
        self.actionTriggered.connect(self.value_changed)
        self.sliderReleased.connect(self._emit_slider_value)

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        """Slot called when connection state of pv changes."""
        self._connected = connected
        self.setEnabled(connected)
        if connected:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def receiveValue(self, value):
        """Slot called when the value of pv changes."""
        if type(value) == str or type(value) == int:
            raise NotImplementedError("Error")

        # if value > self._upper_limit:
        #     value = self._upper_limit
        # if value < self._lower_limit:
        #     value = self._lower_limit

        self._channeltype = type(value)
        self._received_value = True
        self._value = value
        # Check if it is not too big
        self._display_value = value*(10**self._precision)
        self.setValue(self._display_value)

    @pyqtSlot(int)
    def value_changed(self, action):
        """Emit a signal when the value changes."""
        if not self._connected or self._channeltype is None:
            return
        step = 0

        if action not in (QScrollBar.SliderSingleStepAdd,
                          QScrollBar.SliderSingleStepSub,
                          QScrollBar.SliderPageStepAdd,
                          QScrollBar.SliderPageStepSub):
            return

        if action == QScrollBar.SliderSingleStepAdd:
            step = self.singleStep()
        elif action == QScrollBar.SliderSingleStepSub:
            step = -self.singleStep()
        elif action == QScrollBar.SliderPageStepAdd:
            step = self.pageStep()
        elif action == QScrollBar.SliderPageStepSub:
            step = -self.pageStep()

        new_value = self._display_value + step
        if new_value > self.maximum():
            new_value = self.maximum()
        if new_value < self.minimum():
            new_value = self.minimum()

        self._emit_value(new_value)
        # if self._received_value:
        #     self._received_value = False
        #     return

    def _emit_value(self, value):
        descaled_value = value/(10**self._precision)
        self.value_changed_signal[self._channeltype].emit(
            self._channeltype(descaled_value))

    def _emit_slider_value(self):
        self._emit_value(self.value())

    @pyqtSlot(float)
    @pyqtSlot(int)
    def receiveLowerLimit(self, value):
        self._lower_limit = value
        self.setMinimum(value*(10**self._precision))

    @pyqtSlot(float)
    @pyqtSlot(int)
    def receiveUpperLimit(self, value):
        self._upper_limit = value
        self.setMaximum(value*(10**self._precision))
        self.setToolTip("Min: {1}\nMax: {0}".format(
            self.maximum()/(10**self._precision),
            self.minimum()/(10**self._precision)))

    @pyqtProperty(bool)
    def limitsFromPV(self):
        pass

    @limitsFromPV.setter
    def limitsFromPV(self, value):
        pass

    @pyqtSlot(int)
    def receivePrec(self, value):
        self._precision = value

    def channels(self):
        """Return epics channels and its mapping to slots."""
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
