from ..PyQt.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QTimer
from pyqtgraph import ViewBox, AxisItem, PlotItem
import numpy as _np
import time as _time
from .basemultiplot import BaseMultiPlot
from .channel import PyDMChannel

TRACES_CONFIGS = '''
trace{0}_receive_value = pyqtSignal([float],[int])

# def getTrace{0}UpdatesAsynchronously(self):
#     return self._update_mode == self.AsynchronousMode
#
# def setTrace{0}UpdatesAsynchronously(self, value):
#     if value == True:
#         self._update_mode = self.AsynchronousMode
#     else:
#         self._update_mode = self.SynchronousMode
#     self.configure_timer()
#     self.initialize_buffer()
#
# def resetTrace{0}UpdatesAsynchronously(self):
#     self._update_mode = self.SynchronousMode
#     self.configure_timer()
#     self.initialize_buffer()
#
# trace{0}UpdateAsynchronously = pyqtProperty( "bool", getTrace{0}UpdatesAsynchronously,
#                                              setTrace{0}UpdatesAsynchronously,
#                                              resetTrace{0}UpdatesAsynchronously )

def getTrace{0}BufferSize(self):
    return self._trace_buffer_size[{0}]

@pyqtSlot(int)
@pyqtSlot(str)
def setTrace{0}BufferSize(self, value):
    if self._trace_buffer_size[{0}] != int(value):
        self.initializeBuffer({0},True,self._trace_buffer_size[{0}],int(value))
        self._trace_buffer_size[{0}] = max(int(value),1)

def resetTrace{0}BufferSize(self):
    if self._trace_buffer_size[{0}] != 100:
        self.initializeBuffer({0},True,self._trace_buffer_size[{0}],100)
        self._trace_buffer_size[{0}] = 100

trace{0}BufferSize = pyqtProperty("int", getTrace{0}BufferSize,
                                  setTrace{0}BufferSize,
                                  resetTrace{0}BufferSize)

#Trace {0} Channel
@pyqtSlot(bool)
def Trace{0}ConnectionStateChanged(self, connected):
    self._traces_connected[{0}] = connected
    if connected:
        if not self.redraw_timer.isActive():
            self.redraw_timer.start()
        # if self._update_mode == self.AsynchronousMode:
        #     self.update_timer.start()
    else:
        if self.redraw_timer.isActive() and not any(self._traces_connected):
            self.redraw_timer.stop()
        # self.update_timer.stop()

@pyqtSlot(float)
@pyqtSlot(int)
@pyqtSlot(str)
def Trace{0}ReceiveNewValue(self, new_value):
    self.trace{0}_receive_value.emit(new_value)
    if self._update_mode == self.SynchronousMode:
        self._trace_data_buffer[{0}] = _np.roll(self._trace_data_buffer[{0}],-1)
        self._trace_data_buffer[{0}][0,self._trace_buffer_size[{0}] - 1] = new_value
        self._trace_data_buffer[{0}][1,self._trace_buffer_size[{0}] - 1] = _time.time()
        if self._trace_points_accumulated[{0}] < self._trace_buffer_size[{0}]:
            self._trace_points_accumulated[{0}] = self._trace_points_accumulated[{0}] + 1
    # elif self._update_mode == self.AsynchronousMode:
    #     self.latest_value = new_value

def getTrace{0}Channel(self):
    return str(self._trace_channel[{0}])

def setTrace{0}Channel(self, value):
    if self._trace_channel[{0}] != value:
        self._trace_channel[{0}] = str(value)

def resetTrace{0}Channel(self):
    if self._trace_channel[{0}] != None:
        self._trace_channel[{0}] = None

trace{0}Channel = pyqtProperty(str, getTrace{0}Channel, setTrace{0}Channel, resetTrace{0}Channel)
'''

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
        self.redraw_timer.setInterval(20) #miliseconds
        self.redraw_timer.timeout.connect(self.redrawPlots)

        #Plot Configurations
        self._update_mode = PyDMMultiTimePlot.SynchronousMode
        self._time_span = 10.0           #This is in seconds
        # self.plotItem.disableAutoRange(ViewBox.XAxis)

        self._trace_buffer_size         = self.MAX_NUM_TRACES*[100]
        self._trace_channel             = self.MAX_NUM_TRACES*[None]
        self._trace_data_buffer         = self.MAX_NUM_TRACES*[None]
        self._traces_connected          = self.MAX_NUM_TRACES*[False]
        self._trace_points_accumulated  = self.MAX_NUM_TRACES*[0]
        for i in range(self.MAX_NUM_TRACES):
            self.initializeBuffer(i)

        self._traces_connected = self.MAX_NUM_TRACES * [False]
        self._trace0_channel = init_trace0_channel
        self._channels = None

        #AsynchronousMode Configurations
        # self.update_timer = QTimer(self)
        # self._update_interval = 100     #This is in miliseconds

    def initializeBuffer(self,ind,keep=False,oldsize=0,newsize=0):
        increase = (oldsize < newsize)
        if keep:
            if increase:
                for i in range(newsize-oldsize):
                    self._trace_data_buffer[ind] = _np.insert(self._trace_data_buffer[ind],0,0,axis=1)
            else:
                for i in range(oldsize-newsize):
                    self._trace_data_buffer[ind] = _np.delete(self._trace_data_buffer[ind],0,axis=1)
                if self._trace_points_accumulated[ind] > newsize:
                    self._trace_points_accumulated[ind] = newsize
        else:
            self._trace_points_accumulated[ind] = 0
            self._trace_data_buffer[ind] = _np.zeros((2,self._trace_buffer_size[ind]), order='f',dtype=float)
            self._trace_data_buffer[ind][1].fill(_time.time())

    def redrawPlot(self,ind):
        self.trace[ind].setData(y=self._trace_data_buffer[ind][0,-self._trace_points_accumulated[ind]:],
                                x=self._trace_data_buffer[ind][1,-self._trace_points_accumulated[ind]:]  )

    def redrawPlots(self):
        self.updateXAxis()
        for i in range(self._traceCount):
            if self._traces_connected[i]:
                self.redrawPlot(i)

    #Traces' properties
    for i in range(BaseMultiPlot.MAX_NUM_TRACES):
        exec(TRACES_CONFIGS.format(i))

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
        maxrange = _time.time()
        if self._update_mode == self.SynchronousMode:
            vals = [self._trace_data_buffer[i][1,-1] for i in range(self.MAX_NUM_TRACES)]
            maxrange = max(vals)
        minrange = (maxrange - self._time_span)
        self.plotItem.setXRange(minrange,maxrange,padding=0.0,update=update_immediately)

    def channels(self):
        if self._channels is None:
            self._channels = []
            for i in range(self.MAX_NUM_TRACES):
                chan      = getattr(self,'trace{0}Channel'.format(i))
                conn_slot = getattr(self,'Trace{0}ConnectionStateChanged'.format(i))
                val_slot  = getattr(self,'Trace{0}ReceiveNewValue'.format(i))
                self._channels.append( PyDMChannel(address=chan,
                                                   connection_slot=conn_slot,
                                                   value_slot=val_slot)  )
        return self._channels


class TimeAxisItem(AxisItem):
    def tickStrings(self, values, scale, spacing):
        strings = []
        for val in values:
            strings.append(_time.strftime("%H:%M:%S",_time.localtime(val)))
        return strings
