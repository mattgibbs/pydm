from ..PyQt.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QTimer
from pyqtgraph import ViewBox, AxisItem, PlotItem
import numpy as _np
import time as _time
from .basemultiplot import BaseMultiPlot
from .channel import PyDMChannel

class PyDMMultiTimePlot(BaseMultiPlot):

    #Tell Designer what signals are available.
    __pyqtSignals__ = ( "trace0_receive_value([float],[int])", \
                        "trace1_receive_value([float],[int])", \
                        "trace2_receive_value([float],[int])", \
                        "trace3_receive_value([float],[int])", \
                        "trace4_receive_value([float],[int])", \
                        "trace5_receive_value([float],[int])", \
                        "trace6_receive_value([float],[int])", \
                        "trace7_receive_value([float],[int])", \
                        "trace8_receive_value([float],[int])", \
                        "trace9_receive_value([float],[int])", \
                        "trace10_receive_value([float],[int])", \
                        "trace11_receive_value([float],[int])", \
                        "trace12_receive_value([float],[int])", \
                        "trace13_receive_value([float],[int])", \
                        "trace14_receive_value([float],[int])",)

    #Internal signals, used by the state machine
    trace0_receive_value = pyqtSignal([float],[int])
    trace1_receive_value = pyqtSignal([float],[int])
    trace2_receive_value = pyqtSignal([float],[int])
    trace3_receive_value = pyqtSignal([float],[int])
    trace4_receive_value = pyqtSignal([float],[int])
    trace5_receive_value = pyqtSignal([float],[int])
    trace6_receive_value = pyqtSignal([float],[int])
    trace7_receive_value = pyqtSignal([float],[int])
    trace8_receive_value = pyqtSignal([float],[int])
    trace9_receive_value = pyqtSignal([float],[int])
    trace10_receive_value = pyqtSignal([float],[int])
    trace11_receive_value = pyqtSignal([float],[int])
    trace12_receive_value = pyqtSignal([float],[int])
    trace13_receive_value = pyqtSignal([float],[int])
    trace14_receive_value = pyqtSignal([float],[int])

    SynchronousMode = 1
    AsynchronousMode = 2

    def __init__(self, parent=None, init_trace0_channel=None, background='default'):

        self._XAxis1 = TimeAxisItem('bottom')
        self._YAxis1 = AxisItem('left')
        self._YAxis2 = AxisItem('right')
        self._axisItems = {'bottom': self._XAxis1, 'left': self._YAxis1, 'right': self._YAxis2}
        super(PyDMMultiTimePlot,self).__init__(parent=parent, background='default',axisItems=self._axisItems)

        #Redraw Configurations
        self.redraw_timer = QTimer(self)
        self.redraw_timer.setInterval(20)
        self.redraw_timer.timeout.connect(self.redrawPlot)

        #Plot Configurations
        self._update_mode = PyDMMultiTimePlot.SynchronousMode
        self._time_span = 10.0           #This is in seconds
        # self.plotItem.disableAutoRange(ViewBox.XAxis)
        self._trace0_buffer_size = 100
        self._trace1_buffer_size = 100
        self._trace2_buffer_size = 100
        self._trace3_buffer_size = 100
        self._trace4_buffer_size = 100
        self._trace5_buffer_size = 100
        self._trace6_buffer_size = 100
        self._trace7_buffer_size = 100
        self._trace8_buffer_size = 100
        self._trace9_buffer_size = 100
        self._trace10_buffer_size = 100
        self._trace11_buffer_size = 100
        self._trace12_buffer_size = 100
        self._trace13_buffer_size = 100
        self._trace14_buffer_size = 100

        #Traces Configurations
        self._trace0_channel = init_trace0_channel
        self.Trace0InitializeBuffer()
        self._trace0_connected = False
        self._trace1_channel = None
        self.Trace1InitializeBuffer()
        self._trace1_connected = False
        self._trace2_channel = None
        self.Trace2InitializeBuffer()
        self._trace2_connected = False
        self._trace3_channel = None
        self.Trace3InitializeBuffer()
        self._trace3_connected = False
        self._trace4_channel = None
        self.Trace4InitializeBuffer()
        self._trace4_connected = False
        self._trace5_channel = None
        self.Trace5InitializeBuffer()
        self._trace5_connected = False
        self._trace6_channel = None
        self.Trace6InitializeBuffer()
        self._trace6_connected = False
        self._trace7_channel = None
        self.Trace7InitializeBuffer()
        self._trace7_connected = False
        self._trace8_channel = None
        self.Trace8InitializeBuffer()
        self._trace8_connected = False
        self._trace9_channel = None
        self.Trace9InitializeBuffer()
        self._trace9_connected = False
        self._trace10_channel = None
        self.Trace10InitializeBuffer()
        self._trace10_connected = False
        self._trace11_channel = None
        self.Trace11InitializeBuffer()
        self._trace11_connected = False
        self._trace12_channel = None
        self.Trace12InitializeBuffer()
        self._trace12_connected = False
        self._trace13_channel = None
        self.Trace13InitializeBuffer()
        self._trace13_connected = False
        self._trace14_channel = None
        self.Trace14InitializeBuffer()
        self._trace14_connected = False

        #AsynchronousMode Configurations
        # self.update_timer = QTimer(self)
        # self._update_interval = 100     #This is in miliseconds

    #Trace 0 Configurations
    def Trace0InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace0_data_buffer = _np.insert(self.trace0_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace0_data_buffer = _np.delete(self.trace0_data_buffer,0,axis=1)
                if self.trace0_points_accumulated > newsize:
                    self.trace0_points_accumulated = newsize
        else:
            self.trace0_points_accumulated = 0
            self.trace0_data_buffer = _np.zeros((2,self._trace0_buffer_size), order='f',dtype=float)
            self.trace0_data_buffer[1].fill(_time.time())

    def Trace0RedrawPlot(self):
        self.trace0.setData(y=self.trace0_data_buffer[0,-self.trace0_points_accumulated:],x=self.trace0_data_buffer[1,-self.trace0_points_accumulated:])

    # def getTrace0UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace0UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace0UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace0UpdateAsynchronously = pyqtProperty("bool", getTrace0UpdatesAsynchronously, setTrace0UpdatesAsynchronously, resetTrace0UpdatesAsynchronously)

    def getTrace0BufferSize(self):
        return self._trace0_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace0BufferSize(self, value):
        if self._trace0_buffer_size != int(value):
            self.Trace0InitializeBuffer(True,self._trace0_buffer_size,int(value))
            self._trace0_buffer_size = max(int(value),1)

    def resetTrace0BufferSize(self):
        if self._trace0_buffer_size != 100:
            self.Trace0InitializeBuffer(True,self._trace0_buffer_size,100)
            self._trace0_buffer_size = 100

    trace0BufferSize = pyqtProperty("int", getTrace0BufferSize, setTrace0BufferSize, resetTrace0BufferSize)

    #Trace 0 Channel
    @pyqtSlot(bool)
    def Trace0ConnectionStateChanged(self, connected):
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace0_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace0ReceiveNewValue(self, new_value):
        self.trace0_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace0_data_buffer = _np.roll(self.trace0_data_buffer,-1)
            self.trace0_data_buffer[0,self._trace0_buffer_size - 1] = new_value
            self.trace0_data_buffer[1,self._trace0_buffer_size - 1] = _time.time()
            if self.trace0_points_accumulated < self._trace0_buffer_size:
                self.trace0_points_accumulated = self.trace0_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace0Channel(self):
        return str(self._trace0_channel)

    def setTrace0Channel(self, value):
        if self._trace0_channel != value:
            self._trace0_channel = str(value)

    def resetTrace0Channel(self):
        if self._trace0_channel != None:
            self._trace0_channel = None

    trace0Channel = pyqtProperty(str, getTrace0Channel, setTrace0Channel, resetTrace0Channel)

    #Trace 1 Configurations
    def Trace1InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace1_data_buffer = _np.insert(self.trace1_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace1_data_buffer = _np.delete(self.trace1_data_buffer,0,axis=1)
                if self.trace1_points_accumulated > newsize:
                    self.trace1_points_accumulated = newsize
        else:
            self.trace1_points_accumulated = 0
            self.trace1_data_buffer = _np.zeros((2,self._trace1_buffer_size), order='f',dtype=float)
            self.trace1_data_buffer[1].fill(_time.time())

    def Trace1RedrawPlot(self):
        self.trace1.setData(y=self.trace1_data_buffer[0,-self.trace1_points_accumulated:],x=self.trace1_data_buffer[1,-self.trace1_points_accumulated:])

    # def getTrace1UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace1UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace1UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace1UpdateAsynchronously = pyqtProperty("bool", getTrace1UpdatesAsynchronously, setTrace1UpdatesAsynchronously, resetTrace1UpdatesAsynchronously)

    #Trace 1 Channel
    @pyqtSlot(bool)
    def Trace1ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace1_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace1ReceiveNewValue(self, new_value):
        self.trace1_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace1_data_buffer = _np.roll(self.trace1_data_buffer,-1)
            self.trace1_data_buffer[0,self._trace1_buffer_size - 1] = new_value
            self.trace1_data_buffer[1,self._trace1_buffer_size - 1] = _time.time()
            if self.trace1_points_accumulated < self._trace1_buffer_size:
                self.trace1_points_accumulated = self.trace1_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace1BufferSize(self):
        return self._trace1_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace1BufferSize(self, value):
        if self._trace1_buffer_size != int(value):
            self.Trace1InitializeBuffer(True,self._trace1_buffer_size,int(value))
            self._trace1_buffer_size = max(int(value),1)

    def resetTrace1BufferSize(self):
        if self._trace1_buffer_size != 100:
            self.Trace1InitializeBuffer(True,self._trace1_buffer_size,100)
            self._trace1_buffer_size = 100

    trace1BufferSize = pyqtProperty("int", getTrace1BufferSize, setTrace1BufferSize, resetTrace1BufferSize)

    def getTrace1Channel(self):
        return str(self._trace1_channel)

    def setTrace1Channel(self, value):
        if self._trace1_channel != value:
            self._trace1_channel = str(value)

    def resetTrace1Channel(self):
        if self._trace1_channel != None:
            self._trace1_channel = None

    trace1Channel = pyqtProperty(str, getTrace1Channel, setTrace1Channel, resetTrace1Channel)

    #Trace 2 Configurations
    def Trace2InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace2_data_buffer = _np.insert(self.trace2_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace2_data_buffer = _np.delete(self.trace2_data_buffer,0,axis=1)
                if self.trace2_points_accumulated > newsize:
                    self.trace2_points_accumulated = newsize
        else:
            self.trace2_points_accumulated = 0
            self.trace2_data_buffer = _np.zeros((2,self._trace2_buffer_size), order='f',dtype=float)
            self.trace2_data_buffer[1].fill(_time.time())

    def Trace2RedrawPlot(self):
        self.trace2.setData(y=self.trace2_data_buffer[0,-self.trace2_points_accumulated:],x=self.trace2_data_buffer[1,-self.trace2_points_accumulated:])

    # def getTrace2UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace2UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace2UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace2UpdateAsynchronously = pyqtProperty("bool", getTrace2UpdatesAsynchronously, setTrace2UpdatesAsynchronously, resetTrace2UpdatesAsynchronously)

    #Trace 2 Channel
    @pyqtSlot(bool)
    def Trace2ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace2_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace2ReceiveNewValue(self, new_value):
        self.trace2_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace2_data_buffer = _np.roll(self.trace2_data_buffer,-1)
            self.trace2_data_buffer[0,self._trace2_buffer_size - 1] = new_value
            self.trace2_data_buffer[1,self._trace2_buffer_size - 1] = _time.time()
            if self.trace2_points_accumulated < self._trace2_buffer_size:
                self.trace2_points_accumulated = self.trace2_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace2BufferSize(self):
        return self._trace2_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace2BufferSize(self, value):
        if self._trace2_buffer_size != int(value):
            self.Trace2InitializeBuffer(True,self._trace2_buffer_size,int(value))
            self._trace2_buffer_size = max(int(value),1)

    def resetTrace2BufferSize(self):
        if self._trace2_buffer_size != 100:
            self.Trace2InitializeBuffer(True,self._trace2_buffer_size,100)
            self._trace2_buffer_size = 100

    trace2BufferSize = pyqtProperty("int", getTrace2BufferSize, setTrace2BufferSize, resetTrace2BufferSize)

    def getTrace2Channel(self):
        return str(self._trace2_channel)

    def setTrace2Channel(self, value):
        if self._trace2_channel != value:
            self._trace2_channel = str(value)

    def resetTrace2Channel(self):
        if self._trace2_channel != None:
            self._trace2_channel = None

    trace2Channel = pyqtProperty(str, getTrace2Channel, setTrace2Channel, resetTrace2Channel)

    #Trace 3 Configurations
    def Trace3InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace3_data_buffer = _np.insert(self.trace3_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace3_data_buffer = _np.delete(self.trace3_data_buffer,0,axis=1)
                if self.trace3_points_accumulated > newsize:
                    self.trace3_points_accumulated = newsize
        else:
            self.trace3_points_accumulated = 0
            self.trace3_data_buffer = _np.zeros((2,self._trace3_buffer_size), order='f',dtype=float)
            self.trace3_data_buffer[1].fill(_time.time())

    def Trace3RedrawPlot(self):
        self.trace3.setData(y=self.trace3_data_buffer[0,-self.trace3_points_accumulated:],x=self.trace3_data_buffer[1,-self.trace3_points_accumulated:])

    # def getTrace3UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace3UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace3UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace3UpdateAsynchronously = pyqtProperty("bool", getTrace3UpdatesAsynchronously, setTrace3UpdatesAsynchronously, resetTrace3UpdatesAsynchronously)

    #Trace 3 Channel
    @pyqtSlot(bool)
    def Trace3ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace3_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace3ReceiveNewValue(self, new_value):
        self.trace3_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace3_data_buffer = _np.roll(self.trace3_data_buffer,-1)
            self.trace3_data_buffer[0,self._trace3_buffer_size - 1] = new_value
            self.trace3_data_buffer[1,self._trace3_buffer_size - 1] = _time.time()
            if self.trace3_points_accumulated < self._trace3_buffer_size:
                self.trace3_points_accumulated = self.trace3_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace3BufferSize(self):
        return self._trace3_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace3BufferSize(self, value):
        if self._trace3_buffer_size != int(value):
            self.Trace3InitializeBuffer(True,self._trace3_buffer_size,int(value))
            self._trace3_buffer_size = max(int(value),1)

    def resetTrace3BufferSize(self):
        if self._trace3_buffer_size != 100:
            self.Trace3InitializeBuffer(True,self._trace3_buffer_size,100)
            self._trace3_buffer_size = 100

    trace3BufferSize = pyqtProperty("int", getTrace3BufferSize, setTrace3BufferSize, resetTrace3BufferSize)

    def getTrace3Channel(self):
        return str(self._trace3_channel)

    def setTrace3Channel(self, value):
        if self._trace3_channel != value:
            self._trace3_channel = str(value)

    def resetTrace3Channel(self):
        if self._trace3_channel != None:
            self._trace3_channel = None

    trace3Channel = pyqtProperty(str, getTrace3Channel, setTrace3Channel, resetTrace3Channel)

    #Trace 4 Configurations
    def Trace4InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace4_data_buffer = _np.insert(self.trace4_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace4_data_buffer = _np.delete(self.trace4_data_buffer,0,axis=1)
                if self.trace4_points_accumulated > newsize:
                    self.trace4_points_accumulated = newsize
        else:
            self.trace4_points_accumulated = 0
            self.trace4_data_buffer = _np.zeros((2,self._trace4_buffer_size), order='f',dtype=float)
            self.trace4_data_buffer[1].fill(_time.time())

    def Trace4RedrawPlot(self):
        self.trace4.setData(y=self.trace4_data_buffer[0,-self.trace4_points_accumulated:],x=self.trace4_data_buffer[1,-self.trace4_points_accumulated:])

    # def getTrace4UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace4UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace4UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace4UpdateAsynchronously = pyqtProperty("bool", getTrace4UpdatesAsynchronously, setTrace4UpdatesAsynchronously, resetTrace4UpdatesAsynchronously)

    #Trace 4 Channel
    @pyqtSlot(bool)
    def Trace4ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace4_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace4ReceiveNewValue(self, new_value):
        self.trace4_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace4_data_buffer = _np.roll(self.trace4_data_buffer,-1)
            self.trace4_data_buffer[0,self._trace4_buffer_size - 1] = new_value
            self.trace4_data_buffer[1,self._trace4_buffer_size - 1] = _time.time()
            if self.trace4_points_accumulated < self._trace4_buffer_size:
                self.trace4_points_accumulated = self.trace4_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace4BufferSize(self):
        return self._trace4_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace4BufferSize(self, value):
        if self._trace4_buffer_size != int(value):
            self.Trace4InitializeBuffer(True,self._trace4_buffer_size,int(value))
            self._trace4_buffer_size = max(int(value),1)

    def resetTrace4BufferSize(self):
        if self._trace4_buffer_size != 100:
            self.Trace4InitializeBuffer(True,self._trace4_buffer_size,100)
            self._trace4_buffer_size = 100

    trace4BufferSize = pyqtProperty("int", getTrace4BufferSize, setTrace4BufferSize, resetTrace4BufferSize)

    def getTrace4Channel(self):
        return str(self._trace4_channel)

    def setTrace4Channel(self, value):
        if self._trace4_channel != value:
            self._trace4_channel = str(value)

    def resetTrace4Channel(self):
        if self._trace4_channel != None:
            self._trace4_channel = None

    trace4Channel = pyqtProperty(str, getTrace4Channel, setTrace4Channel, resetTrace4Channel)

    #Trace 5 Configurations
    def Trace5InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace5_data_buffer = _np.insert(self.trace5_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace5_data_buffer = _np.delete(self.trace5_data_buffer,0,axis=1)
                if self.trace5_points_accumulated > newsize:
                    self.trace5_points_accumulated = newsize
        else:
            self.trace5_points_accumulated = 0
            self.trace5_data_buffer = _np.zeros((2,self._trace5_buffer_size), order='f',dtype=float)
            self.trace5_data_buffer[1].fill(_time.time())

    def Trace5RedrawPlot(self):
        self.trace5.setData(y=self.trace5_data_buffer[0,-self.trace5_points_accumulated:],x=self.trace5_data_buffer[1,-self.trace5_points_accumulated:])

    # def getTrace5UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace5UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace5UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace5UpdateAsynchronously = pyqtProperty("bool", getTrace5UpdatesAsynchronously, setTrace5UpdatesAsynchronously, resetTrace5UpdatesAsynchronously)

    #Trace 5 Channel
    @pyqtSlot(bool)
    def Trace5ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace5_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace5ReceiveNewValue(self, new_value):
        self.trace5_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace5_data_buffer = _np.roll(self.trace5_data_buffer,-1)
            self.trace5_data_buffer[0,self._trace5_buffer_size - 1] = new_value
            self.trace5_data_buffer[1,self._trace5_buffer_size - 1] = _time.time()
            if self.trace5_points_accumulated < self._trace5_buffer_size:
                self.trace5_points_accumulated = self.trace5_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace5BufferSize(self):
        return self._trace5_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace5BufferSize(self, value):
        if self._trace5_buffer_size != int(value):
            self.Trace5InitializeBuffer(True,self._trace5_buffer_size,int(value))
            self._trace5_buffer_size = max(int(value),1)

    def resetTrace5BufferSize(self):
        if self._trace5_buffer_size != 100:
            self.Trace5InitializeBuffer(True,self._trace5_buffer_size,100)
            self._trace5_buffer_size = 100

    trace5BufferSize = pyqtProperty("int", getTrace5BufferSize, setTrace5BufferSize, resetTrace5BufferSize)

    def getTrace5Channel(self):
        return str(self._trace5_channel)

    def setTrace5Channel(self, value):
        if self._trace5_channel != value:
            self._trace5_channel = str(value)

    def resetTrace5Channel(self):
        if self._trace5_channel != None:
            self._trace5_channel = None

    trace5Channel = pyqtProperty(str, getTrace5Channel, setTrace5Channel, resetTrace5Channel)

    #Trace 6 Configurations
    def Trace6InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace6_data_buffer = _np.insert(self.trace6_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace6_data_buffer = _np.delete(self.trace6_data_buffer,0,axis=1)
                if self.trace6_points_accumulated > newsize:
                    self.trace6_points_accumulated = newsize
        else:
            self.trace6_points_accumulated = 0
            self.trace6_data_buffer = _np.zeros((2,self._trace6_buffer_size), order='f',dtype=float)
            self.trace6_data_buffer[1].fill(_time.time())

    def Trace6RedrawPlot(self):
        self.trace6.setData(y=self.trace6_data_buffer[0,-self.trace6_points_accumulated:],x=self.trace6_data_buffer[1,-self.trace6_points_accumulated:])

    # def getTrace6UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace6UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace6UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace6UpdateAsynchronously = pyqtProperty("bool", getTrace6UpdatesAsynchronously, setTrace6UpdatesAsynchronously, resetTrace6UpdatesAsynchronously)

    #Trace 6 Channel
    @pyqtSlot(bool)
    def Trace6ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace6_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace6ReceiveNewValue(self, new_value):
        self.trace6_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace6_data_buffer = _np.roll(self.trace6_data_buffer,-1)
            self.trace6_data_buffer[0,self._trace6_buffer_size - 1] = new_value
            self.trace6_data_buffer[1,self._trace6_buffer_size - 1] = _time.time()
            if self.trace6_points_accumulated < self._trace6_buffer_size:
                self.trace6_points_accumulated = self.trace6_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace6BufferSize(self):
        return self._trace6_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace6BufferSize(self, value):
        if self._trace6_buffer_size != int(value):
            self.Trace6InitializeBuffer(True,self._trace6_buffer_size,int(value))
            self._trace6_buffer_size = max(int(value),1)

    def resetTrace6BufferSize(self):
        if self._trace6_buffer_size != 100:
            self.Trace6InitializeBuffer(True,self._trace6_buffer_size,100)
            self._trace6_buffer_size = 100

    trace6BufferSize = pyqtProperty("int", getTrace6BufferSize, setTrace6BufferSize, resetTrace6BufferSize)

    def getTrace6Channel(self):
        return str(self._trace6_channel)

    def setTrace6Channel(self, value):
        if self._trace6_channel != value:
            self._trace6_channel = str(value)

    def resetTrace6Channel(self):
        if self._trace6_channel != None:
            self._trace6_channel = None

    trace6Channel = pyqtProperty(str, getTrace6Channel, setTrace6Channel, resetTrace6Channel)

    #Trace 7 Configurations
    def Trace7InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace7_data_buffer = _np.insert(self.trace7_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace7_data_buffer = _np.delete(self.trace7_data_buffer,0,axis=1)
                if self.trace7_points_accumulated > newsize:
                    self.trace7_points_accumulated = newsize
        else:
            self.trace7_points_accumulated = 0
            self.trace7_data_buffer = _np.zeros((2,self._trace7_buffer_size), order='f',dtype=float)
            self.trace7_data_buffer[1].fill(_time.time())

    def Trace7RedrawPlot(self):
        self.trace7.setData(y=self.trace7_data_buffer[0,-self.trace7_points_accumulated:],x=self.trace7_data_buffer[1,-self.trace7_points_accumulated:])

    # def getTrace7UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace7UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace7UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace7UpdateAsynchronously = pyqtProperty("bool", getTrace7UpdatesAsynchronously, setTrace7UpdatesAsynchronously, resetTrace7UpdatesAsynchronously)

    #Trace 7 Channel
    @pyqtSlot(bool)
    def Trace7ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace7_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace7ReceiveNewValue(self, new_value):
        self.trace7_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace7_data_buffer = _np.roll(self.trace7_data_buffer,-1)
            self.trace7_data_buffer[0,self._trace7_buffer_size - 1] = new_value
            self.trace7_data_buffer[1,self._trace7_buffer_size - 1] = _time.time()
            if self.trace7_points_accumulated < self._trace7_buffer_size:
                self.trace7_points_accumulated = self.trace7_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace7BufferSize(self):
        return self._trace7_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace7BufferSize(self, value):
        if self._trace7_buffer_size != int(value):
            self.Trace7InitializeBuffer(True,self._trace7_buffer_size,int(value))
            self._trace7_buffer_size = max(int(value),1)

    def resetTrace7BufferSize(self):
        if self._trace7_buffer_size != 100:
            self.Trace7InitializeBuffer(True,self._trace7_buffer_size,100)
            self._trace7_buffer_size = 100

    trace7BufferSize = pyqtProperty("int", getTrace7BufferSize, setTrace7BufferSize, resetTrace7BufferSize)

    def getTrace7Channel(self):
        return str(self._trace7_channel)

    def setTrace7Channel(self, value):
        if self._trace7_channel != value:
            self._trace7_channel = str(value)

    def resetTrace7Channel(self):
        if self._trace7_channel != None:
            self._trace7_channel = None

    trace7Channel = pyqtProperty(str, getTrace7Channel, setTrace7Channel, resetTrace7Channel)

    #Trace 8 Configurations
    def Trace8InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace8_data_buffer = _np.insert(self.trace8_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace8_data_buffer = _np.delete(self.trace8_data_buffer,0,axis=1)
                if self.trace8_points_accumulated > newsize:
                    self.trace8_points_accumulated = newsize
        else:
            self.trace8_points_accumulated = 0
            self.trace8_data_buffer = _np.zeros((2,self._trace8_buffer_size), order='f',dtype=float)
            self.trace8_data_buffer[1].fill(_time.time())

    def Trace8RedrawPlot(self):
        self.trace8.setData(y=self.trace8_data_buffer[0,-self.trace8_points_accumulated:],x=self.trace8_data_buffer[1,-self.trace8_points_accumulated:])

    # def getTrace8UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace8UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace8UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace8UpdateAsynchronously = pyqtProperty("bool", getTrace8UpdatesAsynchronously, setTrace8UpdatesAsynchronously, resetTrace8UpdatesAsynchronously)

    #Trace 8 Channel
    @pyqtSlot(bool)
    def Trace8ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace8_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace8ReceiveNewValue(self, new_value):
        self.trace8_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace8_data_buffer = _np.roll(self.trace8_data_buffer,-1)
            self.trace8_data_buffer[0,self._trace8_buffer_size - 1] = new_value
            self.trace8_data_buffer[1,self._trace8_buffer_size - 1] = _time.time()
            if self.trace8_points_accumulated < self._trace8_buffer_size:
                self.trace8_points_accumulated = self.trace8_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace8BufferSize(self):
        return self._trace8_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace8BufferSize(self, value):
        if self._trace8_buffer_size != int(value):
            self.Trace8InitializeBuffer(True,self._trace8_buffer_size,int(value))
            self._trace8_buffer_size = max(int(value),1)

    def resetTrace8BufferSize(self):
        if self._trace8_buffer_size != 100:
            self.Trace8InitializeBuffer(True,self._trace8_buffer_size,100)
            self._trace8_buffer_size = 100

    trace8BufferSize = pyqtProperty("int", getTrace8BufferSize, setTrace8BufferSize, resetTrace8BufferSize)

    def getTrace8Channel(self):
        return str(self._trace8_channel)

    def setTrace8Channel(self, value):
        if self._trace8_channel != value:
            self._trace8_channel = str(value)

    def resetTrace8Channel(self):
        if self._trace8_channel != None:
            self._trace8_channel = None

    trace8Channel = pyqtProperty(str, getTrace8Channel, setTrace8Channel, resetTrace8Channel)

    #Trace 9 Configurations
    def Trace9InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace9_data_buffer = _np.insert(self.trace9_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace9_data_buffer = _np.delete(self.trace9_data_buffer,0,axis=1)
                if self.trace9_points_accumulated > newsize:
                    self.trace9_points_accumulated = newsize
        else:
            self.trace9_points_accumulated = 0
            self.trace9_data_buffer = _np.zeros((2,self._trace9_buffer_size), order='f',dtype=float)
            self.trace9_data_buffer[1].fill(_time.time())

    def Trace9RedrawPlot(self):
        self.trace9.setData(y=self.trace9_data_buffer[0,-self.trace9_points_accumulated:],x=self.trace9_data_buffer[1,-self.trace9_points_accumulated:])

    # def getTrace9UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace9UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace9UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace9UpdateAsynchronously = pyqtProperty("bool", getTrace9UpdatesAsynchronously, setTrace9UpdatesAsynchronously, resetTrace9UpdatesAsynchronously)

    #Trace 9 Channel
    @pyqtSlot(bool)
    def Trace9ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace9_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace9ReceiveNewValue(self, new_value):
        self.trace9_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace9_data_buffer = _np.roll(self.trace9_data_buffer,-1)
            self.trace9_data_buffer[0,self._trace9_buffer_size - 1] = new_value
            self.trace9_data_buffer[1,self._trace9_buffer_size - 1] = _time.time()
            if self.trace9_points_accumulated < self._trace9_buffer_size:
                self.trace9_points_accumulated = self.trace9_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace9BufferSize(self):
        return self._trace9_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace9BufferSize(self, value):
        if self._trace9_buffer_size != int(value):
            self.Trace9InitializeBuffer(True,self._trace9_buffer_size,int(value))
            self._trace9_buffer_size = max(int(value),1)

    def resetTrace9BufferSize(self):
        if self._trace9_buffer_size != 100:
            self.Trace9InitializeBuffer(True,self._trace9_buffer_size,100)
            self._trace9_buffer_size = 100

    trace9BufferSize = pyqtProperty("int", getTrace9BufferSize, setTrace9BufferSize, resetTrace9BufferSize)

    def getTrace9Channel(self):
        return str(self._trace9_channel)

    def setTrace9Channel(self, value):
        if self._trace9_channel != value:
            self._trace9_channel = str(value)

    def resetTrace9Channel(self):
        if self._trace9_channel != None:
            self._trace9_channel = None

    trace9Channel = pyqtProperty(str, getTrace9Channel, setTrace9Channel, resetTrace9Channel)

    #Trace 10 Configurations
    def Trace10InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace10_data_buffer = _np.insert(self.trace10_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace10_data_buffer = _np.delete(self.trace10_data_buffer,0,axis=1)
                if self.trace10_points_accumulated > newsize:
                    self.trace10_points_accumulated = newsize
        else:
            self.trace10_points_accumulated = 0
            self.trace10_data_buffer = _np.zeros((2,self._trace10_buffer_size), order='f',dtype=float)
            self.trace10_data_buffer[1].fill(_time.time())

    def Trace10RedrawPlot(self):
        self.trace10.setData(y=self.trace10_data_buffer[0,-self.trace10_points_accumulated:],x=self.trace10_data_buffer[1,-self.trace10_points_accumulated:])

    # def getTrace10UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace10UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace10UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace10UpdateAsynchronously = pyqtProperty("bool", getTrace10UpdatesAsynchronously, setTrace10UpdatesAsynchronously, resetTrace10UpdatesAsynchronously)

    #Trace 10 Channel
    @pyqtSlot(bool)
    def Trace10ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace10_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace10ReceiveNewValue(self, new_value):
        self.trace10_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace10_data_buffer = _np.roll(self.trace10_data_buffer,-1)
            self.trace10_data_buffer[0,self._trace10_buffer_size - 1] = new_value
            self.trace10_data_buffer[1,self._trace10_buffer_size - 1] = _time.time()
            if self.trace10_points_accumulated < self._trace10_buffer_size:
                self.trace10_points_accumulated = self.trace10_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace10BufferSize(self):
        return self._trace10_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace10BufferSize(self, value):
        if self._trace10_buffer_size != int(value):
            self.Trace10InitializeBuffer(True,self._trace10_buffer_size,int(value))
            self._trace10_buffer_size = max(int(value),1)

    def resetTrace10BufferSize(self):
        if self._trace10_buffer_size != 100:
            self.Trace10InitializeBuffer(True,self._trace10_buffer_size,100)
            self._trace10_buffer_size = 100

    trace10BufferSize = pyqtProperty("int", getTrace10BufferSize, setTrace10BufferSize, resetTrace10BufferSize)

    def getTrace10Channel(self):
        return str(self._trace10_channel)

    def setTrace10Channel(self, value):
        if self._trace10_channel != value:
            self._trace10_channel = str(value)

    def resetTrace10Channel(self):
        if self._trace10_channel != None:
            self._trace10_channel = None

    trace10Channel = pyqtProperty(str, getTrace10Channel, setTrace10Channel, resetTrace10Channel)

    #Trace 11 Configurations
    def Trace11InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace11_data_buffer = _np.insert(self.trace11_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace11_data_buffer = _np.delete(self.trace11_data_buffer,0,axis=1)
                if self.trace11_points_accumulated > newsize:
                    self.trace11_points_accumulated = newsize
        else:
            self.trace11_points_accumulated = 0
            self.trace11_data_buffer = _np.zeros((2,self._trace11_buffer_size), order='f',dtype=float)
            self.trace11_data_buffer[1].fill(_time.time())

    def Trace11RedrawPlot(self):
        self.trace11.setData(y=self.trace11_data_buffer[0,-self.trace11_points_accumulated:],x=self.trace11_data_buffer[1,-self.trace11_points_accumulated:])

    # def getTrace11UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace11UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace11UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace11UpdateAsynchronously = pyqtProperty("bool", getTrace11UpdatesAsynchronously, setTrace11UpdatesAsynchronously, resetTrace11UpdatesAsynchronously)

    #Trace 11 Channel
    @pyqtSlot(bool)
    def Trace11ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace12_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace11_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace11ReceiveNewValue(self, new_value):
        self.trace11_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace11_data_buffer = _np.roll(self.trace11_data_buffer,-1)
            self.trace11_data_buffer[0,self._trace11_buffer_size - 1] = new_value
            self.trace11_data_buffer[1,self._trace11_buffer_size - 1] = _time.time()
            if self.trace11_points_accumulated < self._trace11_buffer_size:
                self.trace11_points_accumulated = self.trace11_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace11BufferSize(self):
        return self._trace11_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace11BufferSize(self, value):
        if self._trace11_buffer_size != int(value):
            self.Trace11InitializeBuffer(True,self._trace11_buffer_size,int(value))
            self._trace11_buffer_size = max(int(value),1)

    def resetTrace11BufferSize(self):
        if self._trace11_buffer_size != 100:
            self.Trace11InitializeBuffer(True,self._trace11_buffer_size,100)
            self._trace11_buffer_size = 100

    trace11BufferSize = pyqtProperty("int", getTrace11BufferSize, setTrace11BufferSize, resetTrace11BufferSize)

    def getTrace11Channel(self):
        return str(self._trace11_channel)

    def setTrace11Channel(self, value):
        if self._trace11_channel != value:
            self._trace11_channel = str(value)

    def resetTrace11Channel(self):
        if self._trace11_channel != None:
            self._trace11_channel = None

    trace11Channel = pyqtProperty(str, getTrace11Channel, setTrace11Channel, resetTrace11Channel)

    #Trace 12 Configurations
    def Trace12InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace12_data_buffer = _np.insert(self.trace12_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace12_data_buffer = _np.delete(self.trace12_data_buffer,0,axis=1)
                if self.trace12_points_accumulated > newsize:
                    self.trace12_points_accumulated = newsize
        else:
            self.trace12_points_accumulated = 0
            self.trace12_data_buffer = _np.zeros((2,self._trace12_buffer_size), order='f',dtype=float)
            self.trace12_data_buffer[1].fill(_time.time())

    def Trace12RedrawPlot(self):
        self.trace12.setData(y=self.trace12_data_buffer[0,-self.trace12_points_accumulated:],x=self.trace12_data_buffer[1,-self.trace12_points_accumulated:])

    # def getTrace12UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace12UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace12UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace12UpdateAsynchronously = pyqtProperty("bool", getTrace12UpdatesAsynchronously, setTrace12UpdatesAsynchronously, resetTrace12UpdatesAsynchronously)

    #Trace 12 Channel
    @pyqtSlot(bool)
    def Trace12ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace13_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace12_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace12ReceiveNewValue(self, new_value):
        self.trace12_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace12_data_buffer = _np.roll(self.trace12_data_buffer,-1)
            self.trace12_data_buffer[0,self._trace12_buffer_size - 1] = new_value
            self.trace12_data_buffer[1,self._trace12_buffer_size - 1] = _time.time()
            if self.trace12_points_accumulated < self._trace12_buffer_size:
                self.trace12_points_accumulated = self.trace12_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace12BufferSize(self):
        return self._trace12_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace12BufferSize(self, value):
        if self._trace12_buffer_size != int(value):
            self.Trace12InitializeBuffer(True,self._trace12_buffer_size,int(value))
            self._trace12_buffer_size = max(int(value),1)

    def resetTrace12BufferSize(self):
        if self._trace12_buffer_size != 100:
            self.Trace12InitializeBuffer(True,self._trace12_buffer_size,100)
            self._trace12_buffer_size = 100

    trace12BufferSize = pyqtProperty("int", getTrace12BufferSize, setTrace12BufferSize, resetTrace12BufferSize)

    def getTrace12Channel(self):
        return str(self._trace12_channel)

    def setTrace12Channel(self, value):
        if self._trace12_channel != value:
            self._trace12_channel = str(value)

    def resetTrace12Channel(self):
        if self._trace12_channel != None:
            self._trace12_channel = None

    trace12Channel = pyqtProperty(str, getTrace12Channel, setTrace12Channel, resetTrace12Channel)

    #Trace 13 Configurations
    def Trace13InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace13_data_buffer = _np.insert(self.trace13_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace13_data_buffer = _np.delete(self.trace13_data_buffer,0,axis=1)
                if self.trace13_points_accumulated > newsize:
                    self.trace13_points_accumulated = newsize
        else:
            self.trace13_points_accumulated = 0
            self.trace13_data_buffer = _np.zeros((2,self._trace13_buffer_size), order='f',dtype=float)
            self.trace13_data_buffer[1].fill(_time.time())

    def Trace13RedrawPlot(self):
        self.trace13.setData(y=self.trace13_data_buffer[0,-self.trace13_points_accumulated:],x=self.trace13_data_buffer[1,-self.trace13_points_accumulated:])

    # def getTrace13UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace13UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace13UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace13UpdateAsynchronously = pyqtProperty("bool", getTrace13UpdatesAsynchronously, setTrace13UpdatesAsynchronously, resetTrace13UpdatesAsynchronously)

    #Trace 13 Channel
    @pyqtSlot(bool)
    def Trace13ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace14_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace13_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace13ReceiveNewValue(self, new_value):
        self.trace13_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace13_data_buffer = _np.roll(self.trace13_data_buffer,-1)
            self.trace13_data_buffer[0,self._trace13_buffer_size - 1] = new_value
            self.trace13_data_buffer[1,self._trace13_buffer_size - 1] = _time.time()
            if self.trace13_points_accumulated < self._trace13_buffer_size:
                self.trace13_points_accumulated = self.trace13_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace13BufferSize(self):
        return self._trace13_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace13BufferSize(self, value):
        if self._trace13_buffer_size != int(value):
            self.Trace13InitializeBuffer(True,self._trace13_buffer_size,int(value))
            self._trace13_buffer_size = max(int(value),1)

    def resetTrace13BufferSize(self):
        if self._trace13_buffer_size != 100:
            self.Trace13InitializeBuffer(True,self._trace13_buffer_size,100)
            self._trace13_buffer_size = 100

    trace13BufferSize = pyqtProperty("int", getTrace13BufferSize, setTrace13BufferSize, resetTrace13BufferSize)

    def getTrace13Channel(self):
        return str(self._trace13_channel)

    def setTrace13Channel(self, value):
        if self._trace13_channel != value:
            self._trace13_channel = str(value)

    def resetTrace13Channel(self):
        if self._trace13_channel != None:
            self._trace13_channel = None

    trace13Channel = pyqtProperty(str, getTrace13Channel, setTrace13Channel, resetTrace13Channel)

    #Trace 14 Configurations
    def Trace14InitializeBuffer(self,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self.trace14_data_buffer = _np.insert(self.trace14_data_buffer,0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self.trace14_data_buffer = _np.delete(self.trace14_data_buffer,0,axis=1)
                if self.trace14_points_accumulated > newsize:
                    self.trace14_points_accumulated = newsize
        else:
            self.trace14_points_accumulated = 0
            self.trace14_data_buffer = _np.zeros((2,self._trace14_buffer_size), order='f',dtype=float)
            self.trace14_data_buffer[1].fill(_time.time())

    def Trace14RedrawPlot(self):
        self.trace14.setData(y=self.trace14_data_buffer[0,-self.trace14_points_accumulated:],x=self.trace14_data_buffer[1,-self.trace14_points_accumulated:])

    # def getTrace14UpdatesAsynchronously(self):
    #     return self._update_mode==PyDMMultiTimePlot.AsynchronousMode
    #
    # def setTrace14UpdatesAsynchronously(self, value):
    #     if value == True:
    #         self._update_mode = PyDMMultiTimePlot.AsynchronousMode
    #     else:
    #         self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # def resetTrace14UpdatesAsynchronously(self):
    #     self._update_mode = PyDMMultiTimePlot.SynchronousMode
    #     self.configure_timer()
    #     self.initialize_buffer()
    #
    # trace14UpdateAsynchronously = pyqtProperty("bool", getTrace14UpdatesAsynchronously, setTrace14UpdatesAsynchronously, resetTrace14UpdatesAsynchronously)

    #Trace 14 Channel
    @pyqtSlot(bool)
    def Trace14ConnectionStateChanged(self, connected):
        # not implemented
        if connected:
            if self.redraw_timer.isActive() == False:
                self.redraw_timer.start()
            # if self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
            #     self.update_timer.start()
        else:
            if self.redraw_timer.isActive == True and all(self._trace0_connected,self._trace1_connected,self._trace2_connected,self._trace3_connected,self._trace4_connected,self._trace5_connected,self._trace6_connected,self._trace7_connected,self._trace8_connected,self._trace9_connected,self._trace10_connected,self._trace11_connected,self._trace12_connected,self._trace13_connected,) == False:
                self.redraw_timer.stop()
            # self.update_timer.stop()
        self._trace14_connected = connected

    @pyqtSlot(float)
    @pyqtSlot(int)
    @pyqtSlot(str)
    def Trace14ReceiveNewValue(self, new_value):
        self.trace14_receive_value.emit(new_value)
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace14_data_buffer = _np.roll(self.trace14_data_buffer,-1)
            self.trace14_data_buffer[0,self._trace14_buffer_size - 1] = new_value
            self.trace14_data_buffer[1,self._trace14_buffer_size - 1] = _time.time()
            if self.trace14_points_accumulated < self._trace14_buffer_size:
                self.trace14_points_accumulated = self.trace14_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

    def getTrace14BufferSize(self):
        return self._trace14_buffer_size

    @pyqtSlot(int)
    @pyqtSlot(str)
    def setTrace14BufferSize(self, value):
        if self._trace14_buffer_size != int(value):
            self.Trace14InitializeBuffer(True,self._trace14_buffer_size,int(value))
            self._trace14_buffer_size = max(int(value),1)

    def resetTrace14BufferSize(self):
        if self._trace14_buffer_size != 100:
            self.Trace14InitializeBuffer(True,self._trace14_buffer_size,100)
            self._trace14_buffer_size = 100

    trace14BufferSize = pyqtProperty("int", getTrace14BufferSize, setTrace14BufferSize, resetTrace14BufferSize)

    def getTrace14Channel(self):
        return str(self._trace14_channel)

    def setTrace14Channel(self, value):
        if self._trace14_channel != value:
            self._trace14_channel = str(value)

    def resetTrace14Channel(self):
        if self._trace14_channel != None:
            self._trace14_channel = None

    trace14Channel = pyqtProperty(str, getTrace14Channel, setTrace14Channel, resetTrace14Channel)


    #Asynchronous Mode Configurations
    # def getUpdateInterval(self):
    #     return float(self._update_interval)/1000.0
    #
    # def setUpdateInterval(self, value):
    #     value = abs(int(1000.0*value))
    #     if self._update_interval != value:
    #         self._update_interval = value
    #         self.update_timer.setInterval(self._update_interval)
    #         if self.getUpdatesAsynchronously():
    #             self.setBufferSize(int(self._time_span*1000.0/self._update_interval))
    #
    # def resetUpdateInterval(self):
    #     if self._update_interval != 100:
    #         self._update_interval = 100
    #         self.update_timer.setInterval(self._update_interval)
    #         if self.getUpdatesAsynchronously():
    #             self.setBufferSize(int(self._time_span*1000.0/self._update_interval))
    #
    # updateInterval = pyqtProperty(float, getUpdateInterval, setUpdateInterval, resetUpdateInterval)


    #Plot Configurations
    def getTimeSpan(self):
        return float(self._time_span)

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    def setTimeSpan(self, value):
        value = float(value)
        if self._time_span != value:
            self._time_span = value
            # if self.getUpdatesAsynchronously():
            #     self.setBufferSize(int(self._time_span*1000.0/self._update_interval))
            self.updateXAxis(update_immediately=True)

    def resetTimeSpan(self):
        if self._time_span != 5.0:
            self._time_span = 5.0
            # if self.getUpdatesAsynchronously():
            #     self.setBufferSize(int(self._time_span*1000.0/self._update_interval))
            self.updateXAxis(update_immediately=True)

    timeSpan = pyqtProperty(float, getTimeSpan, setTimeSpan, resetTimeSpan)

    def updateXAxis(self, update_immediately=False):
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            maxrange = max(self.trace0_data_buffer[1, -1], \
                           self.trace1_data_buffer[1, -1], \
                           self.trace2_data_buffer[1, -1], \
                           self.trace3_data_buffer[1, -1], \
                           self.trace4_data_buffer[1, -1], \
                           self.trace5_data_buffer[1, -1], \
                           self.trace6_data_buffer[1, -1], \
                           self.trace7_data_buffer[1, -1], \
                           self.trace8_data_buffer[1, -1], \
                           self.trace9_data_buffer[1, -1], \
                           self.trace10_data_buffer[1, -1], \
                           self.trace11_data_buffer[1, -1], \
                           self.trace12_data_buffer[1, -1], \
                           self.trace13_data_buffer[1, -1], \
                           self.trace14_data_buffer[1, -1],)
        # else:
        #     maxrange = _time.time()
        minrange = (maxrange - self._time_span)
        self.plotItem.setXRange(minrange,maxrange,padding=0.0,update=update_immediately)

    def redrawPlot(self):
        self.updateXAxis()
        if self._trace0_connected:
            self.Trace0RedrawPlot()
        if self._traceCount >= 1 and self._trace1_connected:
            self.Trace1RedrawPlot()
        if self._traceCount >= 2 and self._trace2_connected:
            self.Trace2RedrawPlot()
        if self._traceCount >= 3 and self._trace3_connected:
            self.Trace3RedrawPlot()
        if self._traceCount >= 4 and self._trace4_connected:
            self.Trace4RedrawPlot()
        if self._traceCount >= 5 and self._trace5_connected:
            self.Trace5RedrawPlot()
        if self._traceCount >= 6 and self._trace6_connected:
            self.Trace6RedrawPlot()
        if self._traceCount >= 7 and self._trace7_connected:
            self.Trace7RedrawPlot()
        if self._traceCount >= 8 and self._trace8_connected:
            self.Trace8RedrawPlot()
        if self._traceCount >= 9 and self._trace9_connected:
            self.Trace9RedrawPlot()
        if self._traceCount >= 10 and self._trace10_connected:
            self.Trace10RedrawPlot()
        if self._traceCount >= 11 and self._trace11_connected:
            self.Trace11RedrawPlot()
        if self._traceCount >= 12 and self._trace12_connected:
            self.Trace12RedrawPlot()
        if self._traceCount >= 13 and self._trace13_connected:
            self.Trace13RedrawPlot()
        if self._traceCount >= 14 and self._trace14_connected:
            self.Trace14RedrawPlot()

    def channels(self):
      return [PyDMChannel(address=self.trace0Channel, connection_slot=self.Trace0ConnectionStateChanged, value_slot=self.Trace0ReceiveNewValue), \
              PyDMChannel(address=self.trace1Channel, connection_slot=self.Trace1ConnectionStateChanged, value_slot=self.Trace1ReceiveNewValue), \
              PyDMChannel(address=self.trace2Channel, connection_slot=self.Trace2ConnectionStateChanged, value_slot=self.Trace2ReceiveNewValue), \
              PyDMChannel(address=self.trace3Channel, connection_slot=self.Trace3ConnectionStateChanged, value_slot=self.Trace3ReceiveNewValue), \
              PyDMChannel(address=self.trace4Channel, connection_slot=self.Trace4ConnectionStateChanged, value_slot=self.Trace4ReceiveNewValue), \
              PyDMChannel(address=self.trace5Channel, connection_slot=self.Trace5ConnectionStateChanged, value_slot=self.Trace5ReceiveNewValue), \
              PyDMChannel(address=self.trace6Channel, connection_slot=self.Trace6ConnectionStateChanged, value_slot=self.Trace6ReceiveNewValue), \
              PyDMChannel(address=self.trace7Channel, connection_slot=self.Trace7ConnectionStateChanged, value_slot=self.Trace7ReceiveNewValue), \
              PyDMChannel(address=self.trace8Channel, connection_slot=self.Trace8ConnectionStateChanged, value_slot=self.Trace8ReceiveNewValue), \
              PyDMChannel(address=self.trace9Channel, connection_slot=self.Trace9ConnectionStateChanged, value_slot=self.Trace9ReceiveNewValue), \
              PyDMChannel(address=self.trace10Channel, connection_slot=self.Trace10ConnectionStateChanged, value_slot=self.Trace10ReceiveNewValue), \
              PyDMChannel(address=self.trace11Channel, connection_slot=self.Trace11ConnectionStateChanged, value_slot=self.Trace11ReceiveNewValue), \
              PyDMChannel(address=self.trace12Channel, connection_slot=self.Trace12ConnectionStateChanged, value_slot=self.Trace12ReceiveNewValue), \
              PyDMChannel(address=self.trace13Channel, connection_slot=self.Trace13ConnectionStateChanged, value_slot=self.Trace13ReceiveNewValue), \
              PyDMChannel(address=self.trace14Channel, connection_slot=self.Trace14ConnectionStateChanged, value_slot=self.Trace14ReceiveNewValue),]


class TimeAxisItem(AxisItem):
    def tickStrings(self, values, scale, spacing):
        strings = []
        for val in values:
            strings.append(_time.strftime("%H:%M:%S",_time.localtime(val)))
        return strings
