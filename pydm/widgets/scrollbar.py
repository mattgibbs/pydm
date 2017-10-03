"""Define PyDM scrollbar widget."""
from pydm.PyQt.QtCore import Qt, pyqtSignal
from pydm.widgets.QDoubleScrollBar import QDoubleScrollBar
from .base import PyDMWritableWidget


class PyDMScrollBar(QDoubleScrollBar, PyDMWritableWidget):
    """
    A QDoubleScrollBar with support for Channels and more from PyDM.

    Parameters
    ----------
    parent : QWidget
        The parent widget for the scroll bar
    init_channel : str, optional
        The channel to be used by the widget.
    orientation : Qt.Horizontal, Qt.Vertical
        Orientation of the scroll bar
    precision : int
        Precision to be use. Used to calculate size of the scroll bar step
    """

    value_changed_signal = pyqtSignal([int], [float], [str])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, orientation=Qt.Horizontal,
                 init_channel=None, precision=2):
        QDoubleScrollBar.__init__(self, orientation, parent)
        PyDMWritableWidget.__init__(self, init_channel)

        self.setFocusPolicy(Qt.StrongFocus)
        # self.setEnabled(False)
        # self.setDecimals(precision)
        self.setInvertedControls(False)
        self._prec = precision
        self.setSingleStep(1/10**self._prec)
        self.setPageStep(10/10**self._prec)
        # else:
        #     self.setSingleStep(step)
        #     self.setPageStep(10 * step)

        self._update_tooltip()

        self.setTracking(True)
        self.actionTriggered.connect(self.send_value)

    def send_value(self):
        """Emit send_value_signal."""
        value = self.sliderPosition
        if self._connected and self.channeltype is not None:
            self.send_value_signal[self.channeltype].emit(
                self.channeltype(value))

    def ctrl_limit_changed(self, which, new_limit):
        """Call super and set new limits."""
        PyDMWritableWidget.ctrl_limit_changed(self, which, new_limit)

        if which == "UPPER":
            self.setMaximum(self._upper_ctrl_limit)
        else:
            self.setMinimum(self._lower_ctrl_limit)

        self._update_tooltip()

    def precision_changed(self, new_precision):
        """Call super and set new steps."""
        PyDMWritableWidget.precision_changed(self, new_precision)
        self.setDecimals(round(self._prec))
        self.setSingleStep(1/10**self._prec)
        self.setPageStep(10/10**self._prec)
        self._update_tooltip()

    def _update_tooltip(self):
        if self._lower_ctrl_limit is not None \
                and self._upper_ctrl_limit is not None:
            toltp = \
                str(self._lower_ctrl_limit) + "," + str(self._upper_ctrl_limit)
            self.setToolTip(toltp)
