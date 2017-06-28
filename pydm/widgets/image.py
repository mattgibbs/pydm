from ..PyQt.QtGui import QLabel, QApplication, QColor, QActionGroup
from ..PyQt.QtCore import pyqtSignal, pyqtSlot, pyqtProperty, Q_ENUMS
from pyqtgraph import ImageView, ImageItem, ColorMap
import numpy as np
from .channel import PyDMChannel
from .colormaps import cmaps

READINGORDER = {'Fortranlike': 0, 'Clike': 1}
aux = 0
COLORMAP = {}
for cm in cmaps:
    COLORMAP[cm] = aux
    aux += 1

class PyDMImageView(ImageView):

    #Tell Designer what signals are available.
    __pyqtSignals__ = ("connected_signal()",
                     "disconnected_signal()")

    #Internal signals, used by the state machine
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    #enumMap for readingOrderMap
    locals().update(**READINGORDER)

    class readingOrderMap:
        locals().update(**READINGORDER)

    Q_ENUMS(readingOrderMap)

    #enumMap for colormapMap
    locals().update(**COLORMAP)

    class colormapMap:
        locals().update(**COLORMAP)

    Q_ENUMS(colormapMap)

    readingorderdict = {Fortranlike:    'F',
                        Clike:          'C'}
    colormapdict =     {magma:      cmaps['magma'],
                        inferno:    cmaps['inferno'],
                        plasma:     cmaps['plasma'],
                        viridis:    cmaps['viridis'],
                        jet:        cmaps['jet'],
                        monochrome: cmaps['monochrome'],
                        hot:        cmaps['hot']}

    def __init__(self, parent=None, init_image_channel=None, init_width_channel=None,
                 init_image_width=0, init_reading_order=0, init_colormap_index=0,
                 init_normalize_data=False):
        super(PyDMImageView, self).__init__(parent)
        self._imagechannel = init_image_channel
        self._widthchannel = init_width_channel
        self.image_waveform = np.zeros(0)
        self.image_width = init_image_width
        self._connected = False
        self._normalize_data = init_normalize_data

        #Hide some itens of the widget
        self.ui.histogram.hide()
        del self.ui.histogram
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

        #Set Color Map limits
        self.cm_min = 0.0
        self.cm_max = 255.0

        #Reading order of numpy array data
        self._readingOrder = init_reading_order
        self._needs_reshape = False

        #Default Color Map
        self._colormapindex = init_colormap_index
        self._cm_colors = self.colormapdict[self._colormapindex]
        self.setColorMap()

        #Menu to change Color Map
        cm_menu = self.getView().getMenu(None).addMenu("Color Map")
        cm_group = QActionGroup(self)
        for map_name in COLORMAP:
          action = cm_group.addAction(map_name)
          action.setCheckable(True)
          action.index = COLORMAP[map_name]
          cm_menu.addAction(action)
          if action.index == self._colormapindex:
            action.setChecked(True)
        cm_menu.triggered.connect(self.changeColorMap)

    def changeColorMap(self, action):
        self.colormap = action.index

    def setColorMap(self, new_colormap=None):
        if not new_colormap:
            if not self._cm_colors.any():
                return
            pos = np.linspace(0.0, 1.0, num=len(self._cm_colors))
            new_colormap = ColorMap(pos, self._cm_colors)
        self.getView().setBackgroundColor(new_colormap.map(0))
        lut = new_colormap.getLookupTable(0.0,1.0, alpha=False)
        self.getImageItem().setLookupTable(lut)
        self.getImageItem().setLevels([0.0,1.0])

    def setColorMapLimits(self, new_min, new_max):
        self.setColorMapMax(new_max)
        self.setColorMapMin(new_min)

    #PyDMSlots
    @pyqtSlot(np.ndarray)
    def receiveImageWaveform(self, new_waveform):
        if new_waveform is None:
            return
        if self.image_width == 0:
            if self._widthchannel is not None:
                self.image_waveform = new_waveform
                self._needs_reshape = True  #We'll wait to draw the image until we get the width from channel.
                return
            else:
                try:
                    self.image_width = new_waveform[0]
                    image = new_waveform[1:]
                    self.image_waveform = image.reshape((int(self.image_width),-1), order=self.readingorderdict[self._readingOrder])
                except:
                    raise Exception('Image width is not defined')
        else:
            if len(new_waveform.shape) == 1: # if widthchannel is not defined
                self.image_waveform = new_waveform.reshape((int(self.image_width),-1), order=self.readingorderdict[self._readingOrder])
            elif len(new_waveform.shape) == 2: # if widthchannel is defined
                self.image_waveform = new_waveform
        self.redrawImage()

    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    def receiveImageWidth(self, new_width):
        if new_width is None:
            return
        self.image_width = int(new_width)
        if self._needs_reshape:
            self.image_waveform = self.image_waveform.reshape((int(self.image_width),-1), order=self.readingorderdict[self._readingOrder])
            self._needs_reshape = False
        self.redrawImage()

    def redrawImage(self):
        if len(self.image_waveform) <=0 or self.image_width <= 0: return
        if self._normalize_data:
            mini = self.image_waveform.min()
            maxi = self.image_waveform.max()
        else:
            mini = self.cm_min
            maxi = self.cm_max
        image = (self.image_waveform - mini)/(maxi-mini)
        self.getImageItem().setImage(image, autoLevels=False)

    @pyqtSlot(int)
    def alarmStatusChanged(self, new_alarm_state):
        # -2 to +2, -2 is LOLO, -1 is LOW, 0 is OK, etc.
        pass

    @pyqtSlot(int)
    def alarmSeverityChanged(self, new_alarm_severity):
        #0 = NO_ALARM, 1 = MINOR, 2 = MAJOR, 3 = INVALID
        pass

    @pyqtSlot(bool)
    def connectionStateChanged(self, connected):
        #false = disconnected, true = connected
        self._connected = connected
        if connected:
          self.connected_signal.emit()
        else:
          self.disconnected_signal.emit()

    #PyQt properties (the ones that show up in designer)
    @pyqtProperty(int)
    def imageWidth(self):
        return self.image_width
    @imageWidth.setter
    def imageWidth(self,new_width):
        if self.image_width != new_width and self._widthchannel is None:
            self.image_width = new_width

    @pyqtProperty(colormapMap)
    def colormap(self):
        return self._colormapindex
    @colormap.setter
    def colormap(self, new_colormapindex):
        if self._colormapindex != new_colormapindex:
            self._colormapindex = new_colormapindex
            self._cm_colors = self.colormapdict[self._colormapindex]
            self.setColorMap()

    @pyqtProperty(bool)
    def normalizeData(self):
        return self._normalize_data
    @normalizeData.setter
    @pyqtSlot(bool)
    def normalizeData(self, new_norm):
        if self._normalize_data == new_norm: return
        self._normalize_data = new_norm
        self.redrawImage()

    @pyqtProperty(int)
    def colorMapMin(self):
        return self.cm_min
    @colorMapMin.setter
    @pyqtSlot(int)
    def colorMapMin(self, new_min):
        if self.cm_min == new_min or new_min > self.cm_max: return
        self.cm_min = new_min
        self.setColorMap()

    @pyqtProperty(int)
    def colorMapMax(self):
        return self.cm_max
    @colorMapMax.setter
    @pyqtSlot(int)
    def colorMapMax(self, new_max):
        if self.cm_max == new_max or new_max < self.cm_min: return
        self.cm_max = new_max
        self.setColorMap()

    @pyqtProperty(readingOrderMap)
    def readingOrder(self):
        return self._readingOrder
    @readingOrder.setter
    def readingOrder(self,new_order):
        if self._readingOrder != new_order:
            self._readingOrder = new_order

    @pyqtProperty(str)
    def imageChannel(self):
        return str(self._imagechannel)
    @imageChannel.setter
    def imageChannel(self, value):
        if self._imagechannel != value:
            self._imagechannel = str(value)

    @pyqtProperty(str)
    def widthChannel(self):
        return str(self._widthchannel)
    @widthChannel.setter
    def widthChannel(self, value):
        if self._widthchannel != value:
            self._widthchannel = str(value)

    def channels(self):
        return [PyDMChannel(address=self.imageChannel,
                            connection_slot=self.connectionStateChanged,
                            waveform_slot=self.receiveImageWaveform,
                            severity_slot=self.alarmSeverityChanged),
                PyDMChannel(address=self.widthChannel,
                            connection_slot=self.connectionStateChanged,
                            value_slot=self.receiveImageWidth,
                            severity_slot=self.alarmSeverityChanged)]
