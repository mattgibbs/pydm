from ..PyQt.QtGui import QLabel, QApplication, QColor, QActionGroup
from ..PyQt.QtCore import pyqtSignal, pyqtSlot, pyqtProperty, Q_ENUMS
from pyqtgraph import ImageView, ImageItem, ColorMap
import numpy as np
from .channel import PyDMChannel
from .colormaps import cmaps

class PyDMImageView(ImageView):

    #enumMap for readingOrderMap
    Fortranlike = 0
    Clike =  1
    #enumMap for colormapMap
    magma = 0
    inferno = 1
    plasma = 2
    viridis = 3
    jet = 4
    monochrome = 5
    hot = 6

    class readingOrderMap:
        Fortranlike = 0
        Clike =  1

    class colormapMap:
        magma = 0
        inferno = 1
        plasma = 2
        viridis = 3
        jet = 4
        monochrome = 5
        hot = 6

    Q_ENUMS(readingOrderMap)
    Q_ENUMS(colormapMap)

    readingorderdict = {readingOrderMap.Fortranlike:    'F',
                        readingOrderMap.Clike:          'C'}
    colormapdict =     {colormapMap.magma:      cmaps['magma'],
                        colormapMap.inferno:    cmaps['inferno'],
                        colormapMap.plasma:     cmaps['plasma'],
                        colormapMap.viridis:    cmaps['viridis'],
                        colormapMap.jet:        cmaps['jet'],
                        colormapMap.monochrome: cmaps['monochrome'],
                        colormapMap.hot:        cmaps['hot']}

    def __init__(self, parent=None, init_image_channel=None, init_width_channel=None, init_image_width=0, init_reading_order=0, init_colormap_index=0):
        super(PyDMImageView, self).__init__(parent)
        self._imagechannel = init_image_channel
        self._widthchannel = init_width_channel
        self.image_waveform = np.zeros(0)
        self.image_width = init_image_width

        #Hide some itens of the widget
        self.ui.histogram.hide()
        del self.ui.histogram
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

        #Set Color Map limits
        self.cm_min = 0.0
        self.cm_max = 255.0
        self.data_max_int = 255 #This is the max value for the image waveform's data type.  It gets set when the waveform updates.

        #Reading order of numpy array data
        self._readingOrder = init_reading_order
        self._needs_reshape = False

        #Default Color Map
        self._colormapindex = init_colormap_index
        self._cm_colors = self.colormapdict[self._colormapindex]

        #Menu to change Color Map
        cm_menu = self.getView().getMenu(None).addMenu("Color Map")
        cm_group = QActionGroup(self)
        index = 0
        for map_name in cmaps:
          action = cm_group.addAction(map_name)
          action.setCheckable(True)
          action.index = index
          index += 1
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
            pos = np.linspace(self.cm_min/float(self.data_max_int), self.cm_max/float(self.data_max_int), num=len(self._cm_colors))
            new_colormap = ColorMap(pos, self._cm_colors)
        self.getView().setBackgroundColor(new_colormap.map(0))
        lut = new_colormap.getLookupTable(0.0,1.0,self.data_max_int, alpha=False)
        self.getImageItem().setLookupTable(lut)
        self.getImageItem().setLevels([self.cm_min/float(self.data_max_int),float(self.data_max_int)])

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
        self.data_max_int = self.image_waveform.max() #np.iinfo(self.image_waveform.dtype.type).max
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
        if len(self.image_waveform) > 0 and self.image_width > 0:
            self.getImageItem().setImage(self.image_waveform, autoLevels=False)

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
        pass

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

    @pyqtProperty(int)
    def colorMapMin(self):
        return self.cm_min
    @colorMapMin.setter
    @pyqtSlot(int)
    def colorMapMin(self, new_min):
        if self.cm_min != new_min:
            self.cm_min = new_min
            if self.cm_min > self.cm_max:
                self.cm_max = self.cm_min
            self.setColorMap()

    @pyqtProperty(int)
    def colorMapMax(self):
        return self.cm_max
    @colorMapMax.setter
    @pyqtSlot(int)
    def colorMapMax(self, new_max):
        if self.cm_max != new_max:
            if new_max >= self.data_max_int:
                self.cm_max = self.data_max_int
            if self.cm_max < self.cm_min:
                self.cm_min = self.cm_max
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
