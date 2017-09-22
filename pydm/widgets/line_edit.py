"""PyDMLineEdit Module."""

from functools import partial
import numpy as _np
from ..PyQt.QtGui import QLineEdit, QMenu
from ..PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from .channel import PyDMChannel
from pydm import utilities


class PyDMLineEdit(QLineEdit):
    """Writeable text field to send and display channel values."""

    __pyqtSignals__ = ("no_alarm_signal()",
                       "minor_alarm_signal()",
                       "major_alarm_signal()",
                       "invalid_alarm_signal()"
                       )

    send_value_signal = pyqtSignal([int], [float], [str], [_np.ndarray])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, init_channel=None, unit=None, prec=None):
        """Initialize the instance."""
        super(PyDMLineEdit, self).__init__(parent)
        self._value = None
        self._display = None
        self._channeltype = None
        self._channel = init_channel

        if prec is None:
            self._prec_from_pv = True
            self._precformat = None
            self._prec = 0
        else:
            self._prec_from_pv = False
            self._precformat = '{{:.{:}f}}'.format(str(prec))
            self._prec = prec
        self._connected = False

        self._userformat = None

        self._scale = 1
        self._useunits = True  # Show units
        if unit is None:
            self._unit_from_pv = True
            self._units = None
            self._unitformat = None
        else:
            self.unit = unit

        self.setEnabled(False)

        self.returnPressed.connect(self.sendValue)

        # Create Context Menu upon Right Click
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.launchMenu)
        self.menu = QMenu(self)
        self.unitMenu = self.menu.addMenu('Convert Units')
        self.createUnitOptions()

    @pyqtProperty(str)
    def unit(self):
        """Unit set by the user. If unset will get from PV."""
        return self._units

    @unit.setter
    def unit(self, unit):
        if utilities.find_unit(unit) is None:
            raise AttributeError('Unit is not defined')
        else:
            self._unit_from_pv = False
            self._userunits = str(unit)
            self._unitformat = '{{:}} {:}'.format(unit)
            scale = utilities.convert(self._units, unit)
            if scale:
                self._scale = scale

    @pyqtProperty(int)
    def prec(self):
        """Number of decimal fields to be shown."""
        return self._prec

    @prec.setter
    def prec(self, value):
        if value >= 0:
            self._prec = value
            self._prec_from_pv = False
            self._precformat = '{{:.{:}f}}'.format(str(value))

    @pyqtProperty(str)
    def channel(self):
        """
        The channel address to attach the PyDMPushButton.

        The actual signal/slot attachment is done at the application level of
        the PyDM module.
        """
        return str(self._channel)

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = str(value)

    @pyqtProperty(bool)
    def usePrecision(self):
        """
        A choice whether or not to use the precision given by channel.

        If set to False, the value received will be displayed as is, with no
        modification to the number of displayed significant figures. However,
        if set to True, and the channel specifies a display precision, a float
        or integer channel value will be set to display the correct precision.
        When using an EPICS Channel, the precision value corresponds to the
        PV's PREC field.

        It is also important to note, that if the value of the channel is a
        String, the choice of True or False will have no affect on the display.
        """
        return self._prec_from_pv

    @usePrecision.setter
    def usePrecision(self, choice):
        if self._prec_from_pv != choice:
            self._prec_from_pv = choice

    @pyqtProperty(bool)
    def showUnits(self):
        """
        A choice whether or not to show the units given by the channel.

        If set to True, the units given in the channel will be displayed with
        the value. If using an EPICS channel, this will automatically be linked
        to the EGU field of the PV.
        """
        return self._useunits

    @showUnits.setter
    def showUnits(self, choice):
        if self._useunits != choice:
            self._useunits = choice

    @pyqtProperty(str)
    def userFormat(self):
        """
        A user defined format for the text display value.

        If you want the channel value to be displayed in a custom format, you
        can enter a format string into this attribute and it will automatically
        be applied to the channel value.

        It is important to watch how your custom format interacts with both the
        precision and unit formatting. If the :attr:`.usePrecision` property is
        set to True, the value given to the user format string will always be a
        string type. Therefore, if you wanted to enter a custom float or
        integer formatting command, you should not use the channel precision.
        Finally, if the :attr:`.showUnits` property is True, the current unit
        of the channel will be appended on to the end of the string.
        """
        return str(self._userformat)

    @userFormat.setter
    def userFormat(self, value):
        if self._userformat != str(value):
            self._userformat = str(value)

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    @pyqtSlot(_np.ndarray)
    def receiveValue(self, value):
        """
        Receive and update the PyDMLineEdit for a new channel value.

        The actual value of the input is saved as well as the type received.
        This also resets the PyDMLineEdit display text using
        :meth:`.setDisplay`

        :param value: The new value of the channel
        """
        self._value = value
        self._channeltype = type(value)
        self.setDisplay()

    @pyqtSlot()
    def sendValue(self):
        """
        Emit a :attr:`send_value_signal` to update channel value.

        The text is cleaned of all units, user-formatting and scale values
        before being sent back to the channel. This function is attached the
        ReturnPressed signal of the PyDMLineEdit
        """
        if self._channeltype is None:
            return
        send_value = str(self.text())

        if self._channeltype == _np.ndarray:
            send_value = _np.array([int(v) for v in send_value.split()])
            self.send_value_signal[_np.ndarray].emit(send_value)
            return

        # Clean text of all formatting
        if self._unitformat:
            send_value = send_value.strip(self._unitformat)

        if self._userformat:
            send_value = send_value.strip(self._userformat)
        # Remove scale factor
        if self._scale and self._channeltype != str:
            send_value = (self._channeltype(send_value)
                          / self._channeltype(self._scale))
        self.send_value_signal[self._channeltype]\
            .emit(self._channeltype(send_value))

    @pyqtSlot(bool)
    def connectionChanged(self, conn):
        """Change the PyDMLineEdit to read only if write access is denied."""
        self._connected = conn
        if conn:
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()
        self.setEnabled(conn)

    @pyqtSlot(bool)
    def writeAccessChanged(self, write_access):
        """Change the PyDMLineEdit to read only if write access is denied."""
        self.setReadOnly(not write_access)

    @pyqtSlot(int)
    def receivePrecision(self, value):
        """
        Accept a precision to display a channel's value.

        The value is saved in order to modify the number of significant figures
        to include after the decimal place for float and int channel values.
        Receiving a new value for the precision causes the display to reset.
        """
        if self._prec_from_pv and value >= 0:
            self._prec = value
            self._precformat = '{{:.{:}f}}'.format(str(value))
            self.setDisplay()

    @pyqtSlot(str)
    def receiveUnits(self, unit):
        """
        Accept a unit to display with a channel's value.

        The unit may or may not be displayed based on the :attr:`showUnits`
        attribute. Receiving a new value for the unit causes the display to
        reset.
        """
        if unit != self._units:
            self._units = str(unit)
            self.createUnitOptions()

            if self._unit_from_pv:
                self._scale = 1
                self._unitformat = '{{:}} {:}'.format(self._units)
            else:
                self._scale = utilities.convert(self._units, self._userunits)
            self.setDisplay()

    def createUnitOptions(self):
        """
        Create the menu for displaying possible unit values.

        The menu is filled with possible unit conversions based on the current
        PyDMLineEdit. If either the unit is not found in the by the
        :func:`utilities.find_unit_options` function, or, the
        :attr:`.showUnits` attribute is set to False, the menu will tell the
        user that there are no available conversions
        """
        self.unitMenu.clear()
        units = utilities.find_unit_options(self._units)
        if units and self._useunits:
            for choice in units:
                self.unitMenu.addAction(choice, partial(self.apply_conversion,
                                                        choice))
        else:
            self.unitMenu.addAction('No Unit Conversions found')

    def apply_conversion(self, unit):
        """
        Convert the current unit to a different one.

        This function will attempt to find a scalar to convert the current unit
        type to the desired one and reset the display with the new conversion.

        Parameters
        ----------
        unit : str
            String name of desired units
        """
        if not self._units:
            return None

        self.unit = unit
        self.clearFocus()
        self.setDisplay()

    def launchMenu(self, point):
        """Launch the context menu with the appropriate unit conversions."""
        return self.menu.exec_(self.mapToGlobal(point))

    def setDisplay(self):
        """
        Set the text display of the PyDMLineEdit.

        The original value given by the PV is converted to a text entry based
        on the current settings for scale value, precision, a user-defined
        format, and the current units. If the user is currently entering a
        value in the PyDMLineEdit the text will not be changed.
        """
        value = self._value
        if isinstance(value, _np.ndarray):
            self._display = ' '.join([str(v) for v in value])
            if not self.hasFocus():
                self.setText(self._display)
            return

        if not isinstance(value, str):
            if self._scale and value:
                value *= self._channeltype(self._scale)
            if self._prec > 0 and value is not None or self._prec_from_pv:
                value = self._precformat.format(value)
            else:
                value = str(value)

        if self._userformat:
            value = self._userformat.format(value)
        if self._units and self.showUnits:
            value = self._unitformat.format(value)
        self._display = str(value)
        if not self.hasFocus():
            self.setText(self._display)

    def focusOutEvent(self, event):
        """
        Unselect PyDMLineEdit in PyDMApplication.

        Overwrites the function called when a user leaves a PyDMLineEdit
        without pressing return.  Resets the value of the text field to the
        current channel value.
        """
        if self._display is not None:
            self.setText(self._display)
        super(PyDMLineEdit, self).focusOutEvent(event)

    def channels(self):
        """Method called by PyDMApplication to initialize the connections."""
        return [PyDMChannel(
                    address=self.channel,
                    value_slot=self.receiveValue,
                    value_signal=self.send_value_signal,
                    waveform_slot=self.receiveValue,
                    waveform_signal=self.send_value_signal[_np.ndarray],
                    connection_slot=self.connectionChanged,
                    prec_slot=self.receivePrecision,
                    unit_slot=self.receiveUnits,
                    write_access_slot=self.writeAccessChanged,
                    )]
