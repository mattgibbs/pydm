from ..PyQt.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QTimer
from pyqtgraph import ViewBox, AxisItem, PlotItem
import numpy as _np
import time as _time
from .basemultiplot import BaseMultiPlot
from .channel import PyDMChannel

TRACES_CONFIGS = '''
trace{0}_receive_waveform = pyqtSignal(_np.ndarray)
trace{0}_receive_value    = pyqtSignal([float],[int],[str],[_np.ndarray])

def Trace{0}RedrawPlot(self):
    datax = self._x_data
    datay = self.trace{0}_data
    if datay is None: return
    if datax is None: datax = _np.arange(1,len(datay)+1)
    if len(datay)==1: datay = datay*_np.ones(len(datax))
    if self._allow_size_mismatch:
        min_  = min([len(datay),len(datax)])
        datay = datay[:min_]
        datax = datax[:min_]
    if len(datay) != len(datax): return
    self.trace{0}.setData(y=datay*self._trace{0}_scale, x=datax)

@pyqtSlot(_np.ndarray)
def setTrace{0}Waveform(self, new_value):
    self.trace{0}_receive_waveform.emit(new_value)
    self.trace{0}_data = new_value

@pyqtSlot(int)
@pyqtSlot(float)
@pyqtSlot(str)
@pyqtSlot(_np.ndarray)
def setTrace{0}Value(self, new_value):
    self.trace{0}_receive_value.emit(new_value)
    self.trace{0}_data = _np.array([float(new_value)])

@pyqtProperty(str)
def trace{0}Channel(self):
    return str(self._trace{0}_channel)
@trace{0}Channel.setter
def trace{0}Channel(self, value):
    if self._trace{0}_channel != value:
        self._trace{0}_channel = str(value)

@pyqtSlot(int)
@pyqtSlot(float)
@pyqtSlot(str)
def setTrace{0}Scale(self,new_value):
    self._trace{0}_scale = float(new_value)

@pyqtProperty(float)
def trace{0}Scale(self):
    return float(self._trace{0}_scale)
@trace{0}Scale.setter
def trace{0}Scale(self, value):
    if self._trace{0}_scale != float(value):
        self._trace{0}_scale = float(value)
'''

class PyDMMultiWaveformPlot(BaseMultiPlot):
    SynchronousMode = 1
    AsynchronousMode = 2

    def __init__(self, parent=None, init_trace0_channel=None, init_x_channel=None, background='default'):
        self._XAxis1 = AxisItem('bottom')
        self._YAxis1 = AxisItem('left')
        self._YAxis2 = AxisItem('right')
        self._axisItems = {'bottom': self._XAxis1, 'left': self._YAxis1, 'right': self._YAxis2}
        super(PyDMMultiWaveformPlot,self).__init__(parent=parent, background='default',axisItems=self._axisItems)

        #Redraw Configurations
        self.redraw_timer = QTimer(self)
        self.redraw_timer.setInterval(20) #miliseconds
        self.redraw_timer.timeout.connect(self.redrawPlot)

        self._channels = None
        self._allow_size_mismatch = True

        for i in range(self.MAX_NUM_TRACES):
            setattr(self, '_trace'+str(i)+'_channel',None)
            setattr(self, '_trace'+str(i)+'_data',None)
            setattr(self, '_trace'+str(i)+'_scale',1)
        self._trace0_channel = init_trace0_channel

        self._x_channel = None
        self._x_data    = None
        self._x_channel = init_x_channel

    @pyqtProperty(bool)
    def allowSizeMismatch(self):
        return bool(self._allow_size_mismatch)
    @allowSizeMismatch.setter
    def allowSizeMismatch(self, value):
        if self._allow_size_mismatch != value:
            self._allow_size_mismatch = bool(value)

    #YTraces' properties
    for i in range(BaseMultiPlot.MAX_NUM_TRACES):
        exec(TRACES_CONFIGS.format(i))

    x_receive_waveform = pyqtSignal(_np.ndarray)
    x_receive_value    = pyqtSignal([float],[int],[str],[_np.ndarray])

    @pyqtSlot(_np.ndarray)
    def setXWaveform(self, new_value):
        self.x_receive_waveform.emit(new_value)
        self._x_data = new_value

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    @pyqtSlot(_np.ndarray)
    def setXValue(self, new_value):
        self.x_receive_value.emit(new_value)
        self.x_data = _np.array([float(new_value)])

    @pyqtProperty(str)
    def XChannel(self):
        return str(self._x_channel)
    @XChannel.setter
    def XChannel(self, value):
        if self._x_channel != value:
            self._x_channel = str(value)

    def redrawPlot(self):
        for i in range(self._traceCount):
            attr_ = getattr('Trace{0}redrawPlot'.format(i))
            attr_()

    def channels(self):
        if self._channels is None:
            self._channels = [ PyDMChannel(address=self.XChannel,
                                           waveform_slot=self.setXWaveform,
                                           value_slot=self.setXValue)  ]
            for i in range(self.MAX_NUM_TRACES):
                chan      = getattr(self,'trace{0}Channel'.format(i))
                wave_slot = getattr(self,'setTrace{0}Waveform'.format(i))
                val_slot  = getattr(self,'setTrace{0}Value'.format(i))
                self._channels.append( PyDMChannel(address=chan,
                                                   waveform_slot=wave_slot,
                                                   value_slot=val_slot)  )
        return self._channels
