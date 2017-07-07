from pydm.PyQt.QtGui import QScrollBar
from pydm.PyQt.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty

class QDoubleScrollBar(QScrollBar):
    rangeChanged = pyqtSignal(float,float)
    sliderMoved = pyqtSignal(float)
    valueChanged = pyqtSignal(float)

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        self._decimals = 0
        self._scale = 1
        super(QDoubleScrollBar,self).__init__(orientation,parent)
        super().rangeChanged.connect(self._intercept_rangeChanged)
        super().sliderMoved.connect(self._intercept_sliderMoved)
        super().valueChanged.connect(self._intercept_valueChanged)

    def getDecimals(self):
        return self._decimals
    def setDecimals(self,value):
        mini   = self.minimum
        maxi   = self.maximum
        sgstep = self.singleStep
        pgstep = self.pageStep
        val    = self.value
        slpos  = self.sliderPosition

        self._decimals = value
        self._scale = float(10**value)
        self.minimum        = mini
        self.maximum        = maxi
        self.singleStep     = sgstep
        self.pageStep       = pgstep
        self.value          = val
        self.sliderPosition = slpos
    decimals = pyqtProperty(float,getDecimals,setDecimals)

    def getMinimum(self):
        return super().minimum()/self._scale
    def setMinimum(self,value):
        super().setMinimum(int(value*self._scale))
    minimum = pyqtProperty(float,getMinimum,setMinimum)

    def getMaximum(self):
        return super().maximum()/self._scale
    def setMaximum(self,value):
        super().setMaximum(int(value*self._scale))
    maximum = pyqtProperty(float,getMaximum,setMaximum)

    def getSingleStep(self):
        # return super().singleStep()/self._scale
        return super().singleStep()
    def setSingleStep(self,value):
        # super().setSingleStep(int(value*self._scale))
        super().setSingleStep(int(value))
    singleStep = pyqtProperty(float,getSingleStep,setSingleStep)

    def getPageStep(self):
        # return super().pageStep()/self._scale
        return super().pageStep()
    def setPageStep(self,value):
        # super().setPageStep(int(value*self._scale))
        super().setPageStep(int(value))
    pageStep = pyqtProperty(float,getPageStep,setPageStep)

    def getValue(self):
        return super().value()/self._scale
    @pyqtSlot(float)
    def setValue(self,value):
        super().setValue(int(value*self._scale))
    value = pyqtProperty(float,getValue,setValue)

    def getSliderPosition(self):
        return super().sliderPosition()/self._scale
    def setSliderPosition(self,value):
        super().setSliderPosition(int(value*self._scale))
    sliderPosition = pyqtProperty(float,getSliderPosition,setSliderPosition)

    @pyqtSlot(float,float)
    def setRange(self,mini,maxi):
        super().setRange(int(mini/self._scale), int(maxi*self._scale))

    @pyqtSlot(int,int)
    def _intercept_rangeChanged(self,mini,maxi):
        self.rangeChanged.emit(mini/self._scale, maxi/self._scale)

    @pyqtSlot(int)
    def _intercept_sliderMoved(self,value):
        self.sliderMoved.emit(value/self._scale)

    @pyqtSlot(int)
    def _intercept_valueChanged(self,value):
        self.valueChanged.emit(value/self._scale)
