from ..PyQt.QtGui import QComboBox
from ..PyQt.QtCore import pyqtSignal, pyqtSlot, pyqtProperty
from .channel import PyDMChannel

class PyDMEnumComboBox(QComboBox):
  valueChanged = pyqtSignal(int)

  ALARM_NONE = 0
  ALARM_MINOR = 1
  ALARM_MAJOR = 2
  ALARM_INVALID = 3
  ALARM_DISCONNECTED = 4
  alarm_style_sheet_map = {
      ALARM_NONE: "color: black;",
      ALARM_MINOR: "color: yellow;",
      ALARM_MAJOR: "color: red;",
      ALARM_INVALID: "color: purple;",
      ALARM_DISCONNECTED: "color: white;"
  }

  def __init__(self, parent=None, init_channel=None):
    super(PyDMEnumComboBox, self).__init__(parent=parent)
    #Internal values for properties
    self._connected = False
    self._write_access = True
    self._has_enums = False
    self._channels = None
    self._channel = init_channel
    self._value = None
    self.setEnabled(False)
    self.activated[int].connect(self.internal_combo_box_activated_int)

  @property
  def connected(self):
    return self._connected

  @connected.setter
  def connected(self, connected):
    self._connected = connected
    self.update_enable_state()

  @property
  def write_access(self):
    return self._write_access

  @write_access.setter
  def write_access(self, write_access):
    self._write_access = write_access
    self.update_enable_state()

  @property
  def has_enums(self):
    return self._has_enums

  @has_enums.setter
  def has_enums(self, has_enums):
    self._has_enums = has_enums
    self.update_enable_state()

  #Internal methods

  def set_items(self, enums):
    self.clear()
    for enum in enums:
      self.addItem(enum)
    self.has_enums = True

  def update_enable_state(self):
    self.setEnabled(self.write_access and self.connected and self.has_enums)

  #PyDM widget slots

  @pyqtSlot(bool)
  def connectionStateChanged(self, connected):
    self.connected = connected

  @pyqtSlot(bool)
  def writeAccessChanged(self, write_access):
    self.write_access = write_access

  @pyqtSlot(tuple)
  def enumStringsChanged(self, enum_strings):
    self.set_items(enum_strings)

  @pyqtSlot(int)
  def alarmSeverityChanged(self, new_alarm_severity):
    if not self.connected:
      new_alarm_severity = self.ALARM_DISCONNECTED
    self.setStyleSheet(self.alarm_style_sheet_map[new_alarm_severity])

  @pyqtSlot(int)
  @pyqtSlot(float)
  @pyqtSlot(str)
  def receiveValue(self, new_val):
    if self._value != new_val:
      self._value = new_val
      self.setCurrentIndex(new_val)

  @pyqtSlot(int)
  def internal_combo_box_activated_int(self, index):
    if self._value != index:
      self.valueChanged.emit(index)

  #PyQt properties (the ones that show up in designer)
  @pyqtProperty(str)
  def channel(self):
    return str(self._channel) if self._channel else ''
  @channel.setter
  def channel(self, value):
    if self._channel != value:
      self._channel = str(value)

  #PyDM widget required methods
  def channels(self):
    if self._channels is None:
      self._channels = [PyDMChannel(address=self.channel,
                        connection_slot=self.connectionStateChanged,
                        value_slot=self.receiveValue,
                        severity_slot=self.alarmSeverityChanged,
                        write_access_slot=self.writeAccessChanged,
                        enum_strings_slot=self.enumStringsChanged,
                        value_signal=self.valueChanged)]
    return self._channels
