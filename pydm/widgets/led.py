from pydm.PyQt.QtCore import pyqtProperty
from pydm.widgets.QLed import QLed
from .base import PyDMWidget


class PyDMLed(QLed, PyDMWidget):
    """
    A QDoubleScrollBar with support for Channels and more from PyDM.

    Parameters
    ----------
    parent : QWidget
        The parent widget for the scroll bar
    init_channel : str, optional
        The channel to be used by the widget.
    bit : int
        Bit of the PV value to be used
    enum_map : int
        Mapping between enum_string and led colours
    """

    def __init__(self, parent=None, init_channel='', bit=-1, enum_map=None):
        QLed.__init__(self, parent)
        PyDMWidget.__init__(self, init_channel=init_channel)

        self.pvbit = bit

        self._enum_strings = None
        self._enum_map = enum_map
        self._count = None

        # self.setEnabled(False)

    @pyqtProperty(int)
    def pvbit(self): return self._bit
    @pvbit.setter
    def pvbit(self, bit):
        self._bit = -1
        self._mask = None
        if bit >= 0 :
            self._bit = int(bit)
            self._mask = 1 << bit

    # This property is not available to designer yet
    def enumMap(self):
        """
        Map the PV property :attr:`enum_strings` to led colours.
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

        If the PV is an enum type, the led has a colour for each enum. If the
        :attr:`enum_map` is set, it is used to map each enum value to a led
        colour.
        """
        PyDMWidget.value_changed(self, new_val)
        if new_val is None:
            return
        if self._enum_strings is None:  # PV of type integer or float
            value = int(new_val)
            if self._bit < 0:  # Led represents value of PV
                self.setValue(1 if value else 0)
            else:  # Led represents specific bit of PV
                bit_val = (value & self._mask) >> self._bit
                self.setValue(bit_val)
        else:  # PV of type ENUM
            self.setValue(1)
            if self._enum_map is None:
                self.setOnColour(new_val)
            else:
                if self._enum_strings is not None and isinstance(new_val, int):
                    enum_name = self._enum_strings[new_val]
                    color = self._enum_map[enum_name]
                    self.setOnColour(color)

    def enum_strings_changed(self, new_enum_strings):
        PyDMWidget.enum_strings_changed(self, new_enum_strings)
        if self.m_value is not None:
            self.receiveValue(self.m_value)
