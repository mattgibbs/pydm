from pydm.PyQt.QtGui import QColor
from pydm.PyQt.QtCore import pyqtProperty
from pydm.widgets.QLed import QLed
from .base import PyDMWidget


class PyDMLed(QLed, PyDMWidget):
    """
    A QLed with support for Channels and more from PyDM.

    Parameters
    ----------
    parent : QWidget
        The parent widget for the led.
    init_channel : str, optional
        The channel to be used by the widget.
    bit : int
        Bit of the PV value to be handled.
    enum_map : int
        Mapping between enum_string and led colors.
    """

    DarkGreen = QColor(20, 80, 10)
    LightGreen = QColor(0, 140, 0)
    Yellow = QColor(210, 205, 0)
    Red = QColor(207, 0, 0)

    def __init__(self, parent=None, init_channel='', bit=-1, enum_map=None):
        QLed.__init__(self, parent)
        PyDMWidget.__init__(self, init_channel=init_channel)

        self.pvbit = bit
        self.setEnumMap(enum_map)

    @pyqtProperty(int)
    def pvbit(self):
        """
        PV bit to be handled by the led.
        """
        return self._bit

    @pvbit.setter
    def pvbit(self, bit):
        if bit >= 0:
            self._bit = int(bit)
            self._mask = 1 << bit
        else:
            self._bit = -1
            self._mask = None

    # This property is not available to designer yet
    def enumMap(self):
        """
        Map the PV property :attr:`enum_strings` to led colors.
        """
        return self._enum_map

    def setEnumMap(self, enum_map):
        self._enum_map = enum_map

    def value_changed(self, new_val):
        """
        Receive new value and set led color accordingly.

        For int or float data type the standard led behaviour is to be red when
        the value is 0, and green otherwise.

        If a :attr:`bit` is set the value received will be treated as an int
        and the bit value is extracted using a mask. The led represents the
        value of the chosen bit.

        If the PV is an enum type, the led has a color for each enum. If the
        :attr:`enum_map` is set, it is used to map each enum value to a led
        color.
        """
        PyDMWidget.value_changed(self, new_val)
        if new_val is None:
            return
        if self.enum_strings is None:  # PV of type integer or float
            value = int(new_val)
            if self._bit < 0:  # Led represents value of PV
                self.setState(1 if value else 0)
            else:  # Led represents specific bit of PV
                bit_val = (value & self._mask) >> self._bit
                self.setState(bit_val)
        else:  # PV of type ENUM
            self.setState(1)
            if self._enum_map is None:
                enum_colorlist = [PyDMLed.DarkGreen,
                                  PyDMLed.LightGreen,
                                  PyDMLed.Yellow,
                                  PyDMLed.Red]
                self.setOnColor(enum_colorlist[new_val])
            else:
                if self.enum_strings is not None and isinstance(new_val, int):
                    enum_name = self.enum_strings[new_val]
                    color = self._enum_map[enum_name]
                    self.setOnColor(color)

    def enum_strings_changed(self, new_enum_strings):
        """
        Issue value_changed to set the led color according to the enum_strings.
        """
        PyDMWidget.enum_strings_changed(self, new_enum_strings)
        if self.value is not None:
            self.value_changed(self.value)
