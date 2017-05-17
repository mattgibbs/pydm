from pydm.PyQt.QtGui import QScrollBar, QWidget
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty, QState, QStateMachine, QPropertyAnimation, QByteArray
from pydm.widgets.channel import PyDMChannel
import time

class PyDMScrollBar(QScrollBar):

    value_changed_signal = pyqtSignal([int],[float],[str])
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self, parent=None, orientation=Qt.Horizontal, channel=''):
        super(PyDMScrollBar, self).__init__(orientation,parent)
        # self.setOrientation(Qt.Horizontal)
        self._connected = False
        self._channels = None
        self._channel = channel
        self._channeltype = None
        self.setMinimum(0)
        self.setMaximum(350)
        self.setMinimumWidth(90)

        self.valueChanged.connect(self.value_changed)

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        self._connected = connected
        if connected:
            print("Connected")
            self.connected_signal.emit()
        else:
            self.disconnected_signal.emit()

    @pyqtSlot(float)
    def receiveValue(self, value):
        print("Scroll Bar Received Value {}".format(value))
        self._channeltype = type(value)
        self.setValue(value)

    @pyqtSlot()
    def value_changed(self):
        ''' Emits a value changed signal '''
        print("Scroll Bar Emitting {}".format(self.value()))
        self.value_changed_signal[self._channeltype].emit(self._channeltype(self.value()))

    def getChannel(self):
        return str(self._channel)
    def setChannel(self, value):
        if self._channel != value:
            self._channel = str(value)
    def resetChannel(self):
        if self._channel != None:
            self._channel = None
    channel = pyqtProperty(str, getChannel, setChannel, resetChannel)

    def channels(self):
        if self._channels is None:
            self._channels = [PyDMChannel(  address=self._channel,
                                            connection_slot=self.connectionStateChanged,
                                            value_slot=self.receiveValue,
                                            value_signal=self.value_changed_signal)]
        return self._channels
