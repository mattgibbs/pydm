from ..PyQt.QtCore import pyqtSlot, pyqtProperty, QTimer
from pyqtgraph import ViewBox, AxisItem, PlotItem
import numpy as _np
import time as _time
from .basemultiplot import BaseMultiPlot
from .channel import PyDMChannel

class PyDMMultiTimePlot(BaseMultiPlot):

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
        self._buffers_size = 100

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
    def Trace0InitializeBuffer(self):
        # print('here')
        self.trace0_points_accumulated = 0
        self.trace0_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace0_data_buffer = _np.roll(self.trace0_data_buffer,-1)
            self.trace0_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace0_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace0_points_accumulated < self._buffers_size:
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
    def Trace1InitializeBuffer(self):
        self.trace1_points_accumulated = 0
        self.trace1_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace1_data_buffer = _np.roll(self.trace1_data_buffer,-1)
            self.trace1_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace1_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace1_points_accumulated < self._buffers_size:
                self.trace1_points_accumulated = self.trace1_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace2InitializeBuffer(self):
        self.trace2_points_accumulated = 0
        self.trace2_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace2_data_buffer = _np.roll(self.trace2_data_buffer,-1)
            self.trace2_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace2_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace2_points_accumulated < self._buffers_size:
                self.trace2_points_accumulated = self.trace2_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace3InitializeBuffer(self):
        self.trace3_points_accumulated = 0
        self.trace3_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace3_data_buffer = _np.roll(self.trace3_data_buffer,-1)
            self.trace3_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace3_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace3_points_accumulated < self._buffers_size:
                self.trace3_points_accumulated = self.trace3_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace4InitializeBuffer(self):
        self.trace4_points_accumulated = 0
        self.trace4_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace4_data_buffer = _np.roll(self.trace4_data_buffer,-1)
            self.trace4_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace4_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace4_points_accumulated < self._buffers_size:
                self.trace4_points_accumulated = self.trace4_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace5InitializeBuffer(self):
        self.trace5_points_accumulated = 0
        self.trace5_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace5_data_buffer = _np.roll(self.trace5_data_buffer,-1)
            self.trace5_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace5_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace5_points_accumulated < self._buffers_size:
                self.trace5_points_accumulated = self.trace5_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace6InitializeBuffer(self):
        self.trace6_points_accumulated = 0
        self.trace6_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace6_data_buffer = _np.roll(self.trace6_data_buffer,-1)
            self.trace6_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace6_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace6_points_accumulated < self._buffers_size:
                self.trace6_points_accumulated = self.trace6_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace7InitializeBuffer(self):
        self.trace7_points_accumulated = 0
        self.trace7_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace7_data_buffer = _np.roll(self.trace7_data_buffer,-1)
            self.trace7_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace7_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace7_points_accumulated < self._buffers_size:
                self.trace7_points_accumulated = self.trace7_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace8InitializeBuffer(self):
        self.trace8_points_accumulated = 0
        self.trace8_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace8_data_buffer = _np.roll(self.trace8_data_buffer,-1)
            self.trace8_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace8_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace8_points_accumulated < self._buffers_size:
                self.trace8_points_accumulated = self.trace8_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace9InitializeBuffer(self):
        self.trace9_points_accumulated = 0
        self.trace9_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace9_data_buffer = _np.roll(self.trace9_data_buffer,-1)
            self.trace9_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace9_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace9_points_accumulated < self._buffers_size:
                self.trace9_points_accumulated = self.trace9_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace10InitializeBuffer(self):
        self.trace10_points_accumulated = 0
        self.trace10_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace10_data_buffer = _np.roll(self.trace10_data_buffer,-1)
            self.trace10_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace10_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace10_points_accumulated < self._buffers_size:
                self.trace10_points_accumulated = self.trace10_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace11InitializeBuffer(self):
        self.trace11_points_accumulated = 0
        self.trace11_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace11_data_buffer = _np.roll(self.trace11_data_buffer,-1)
            self.trace11_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace11_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace11_points_accumulated < self._buffers_size:
                self.trace11_points_accumulated = self.trace11_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace12InitializeBuffer(self):
        self.trace12_points_accumulated = 0
        self.trace12_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace12_data_buffer = _np.roll(self.trace12_data_buffer,-1)
            self.trace12_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace12_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace12_points_accumulated < self._buffers_size:
                self.trace12_points_accumulated = self.trace12_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace13InitializeBuffer(self):
        self.trace13_points_accumulated = 0
        self.trace13_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace13_data_buffer = _np.roll(self.trace13_data_buffer,-1)
            self.trace13_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace13_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace13_points_accumulated < self._buffers_size:
                self.trace13_points_accumulated = self.trace13_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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
    def Trace14InitializeBuffer(self):
        self.trace14_points_accumulated = 0
        self.trace14_data_buffer = _np.zeros((2,self._buffers_size), order='f',dtype=float)
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
        if self._update_mode == PyDMMultiTimePlot.SynchronousMode:
            self.trace14_data_buffer = _np.roll(self.trace14_data_buffer,-1)
            self.trace14_data_buffer[0,self._buffers_size - 1] = new_value
            self.trace14_data_buffer[1,self._buffers_size - 1] = _time.time()
            if self.trace14_points_accumulated < self._buffers_size:
                self.trace14_points_accumulated = self.trace14_points_accumulated + 1
        # elif self._update_mode == PyDMMultiTimePlot.AsynchronousMode:
        #     self.latest_value = new_value

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

    def getBuffersSize(self):
        return int(self._buffers_size)

    def setBuffersSize(self, value):
        if self._buffers_size != int(value):
            self._buffers_size = max(int(value),1)
            self.Trace0InitializeBuffer()
            self.Trace1InitializeBuffer()
            self.Trace2InitializeBuffer()
            self.Trace3InitializeBuffer()
            self.Trace4InitializeBuffer()
            self.Trace5InitializeBuffer()
            self.Trace6InitializeBuffer()
            self.Trace7InitializeBuffer()
            self.Trace8InitializeBuffer()
            self.Trace9InitializeBuffer()
            self.Trace10InitializeBuffer()
            self.Trace11InitializeBuffer()
            self.Trace12InitializeBuffer()
            self.Trace13InitializeBuffer()
            self.Trace14InitializeBuffer()

    def resetBuffersSize(self):
        if self._buffers_size != 100:
            self._buffers_size = 100
            self.Trace0InitializeBuffer()
            self.Trace1InitializeBuffer()
            self.Trace2InitializeBuffer()
            self.Trace3InitializeBuffer()
            self.Trace4InitializeBuffer()
            self.Trace5InitializeBuffer()
            self.Trace6InitializeBuffer()
            self.Trace7InitializeBuffer()
            self.Trace8InitializeBuffer()
            self.Trace9InitializeBuffer()
            self.Trace10InitializeBuffer()
            self.Trace11InitializeBuffer()
            self.Trace12InitializeBuffer()
            self.Trace13InitializeBuffer()
            self.Trace14InitializeBuffer()

    buffersSize = pyqtProperty("int", getBuffersSize, setBuffersSize, resetBuffersSize)

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
        minrange = max((maxrange - self._time_span), \
                      self.trace0_data_buffer[1, 0], \
                      self.trace1_data_buffer[1, 0], \
                      self.trace2_data_buffer[1, 0], \
                      self.trace3_data_buffer[1, 0], \
                      self.trace4_data_buffer[1, 0], \
                      self.trace5_data_buffer[1, 0], \
                      self.trace6_data_buffer[1, 0], \
                      self.trace7_data_buffer[1, 0], \
                      self.trace8_data_buffer[1, 0], \
                      self.trace9_data_buffer[1, 0], \
                      self.trace10_data_buffer[1, 0], \
                      self.trace11_data_buffer[1, 0], \
                      self.trace12_data_buffer[1, 0], \
                      self.trace13_data_buffer[1, 0], \
                      self.trace14_data_buffer[1, 0],)
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
