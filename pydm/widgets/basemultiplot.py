from ..PyQt.QtGui import QColor, QBrush
from ..PyQt.QtCore import pyqtSlot, pyqtProperty, Q_ENUMS, Qt
# from pyqtgraph import GraphicsLayoutWidget, PlotItem, AxisItem, PlotDataItem, ViewBox
from pyqtgraph import PlotWidget, PlotItem, AxisItem, PlotDataItem, ViewBox, mkPen, LegendItem, ColorMap
import numpy as _np
from pydm.widgets.colormaps import jet as default_cm


TRACES_CONFIGS = '''
@pyqtSlot(bool)
def trace{0}setVisible(self,value):
    self.trace[{0}].setVisible(value)
    self._traceVisible[{0}] = value

@pyqtProperty(QColor)
def trace{0}Color(self):   return self._tracePen[{0}].color()
@trace{0}Color.setter
def trace{0}Color(self, color):
    if self._tracePen[{0}].color() != color:
        self._tracePen[{0}].setColor(color)
        self.trace[{0}].setPen(self._tracePen[{0}])

@pyqtProperty(lineStyleMap)
def trace{0}LineSytle(self):          return self.linestyledict[self._tracePen[{0}].style()]
@trace{0}LineSytle.setter
def trace{0}LineStyle(self,value):    self._tracePen[{0}].setStyle(self.linestyledict[value])

@pyqtProperty(symbolMap)
def trace{0}Symbol(self):        return self._traceSymbol[{0}]
@trace{0}Symbol.setter
def trace{0}Symbol(self,value):
    color = self._tracePen[{0}].color()
    self.trace[{0}].setSymbol(self.symboldict[value])
    self.trace[{0}].setSymbolPen(color)
    self.trace[{0}].setSymbolBrush(color)
    self.trace[{0}].setSymbolSize(8)
    self._traceSymbol[{0}] = value

@pyqtProperty(str)
def trace{0}Title(self):     return str(self._traceTitle[{0}])
@trace{0}Title.setter
def trace{0}Title(self, value):
    self.legendRemoveItem(self._legendEntry[{0}])
    self._traceTitle[{0}] = str(value)
    if value:
        self.legend.addItem(self.trace[{0}],str(value))
        self._legendEntry[{0}] = self.legendGetAddedItem()

@pyqtProperty(int)
def trace{0}YAxisIndex(self):       return self._traceYAxisIndex[{0}]
@trace{0}YAxisIndex.setter
def trace{0}YAxisIndex(self,new_axis):
    if new_axis in [1,2,3]:
        self._plotIndex[self._traceYAxisIndex[{0}]].removeItem(self.trace[{0}])
        self._plotIndex[new_axis].addItem(self.trace[{0}])
        self.trace[{0}].setVisible(self._traceVisible[{0}])
        self._traceYAxisIndex[{0}] = new_axis
'''

SYMBOLS = {'NoSymbol' : 0, 'Circle' : 1,   'Square' : 2,  'Triangle' : 3,
           'Star' : 4,     'Pentagon' : 5, 'Hexagon' : 6, 'X' : 7,
           'Cross' : 8,    'Diamond' : 9}
LINESTYLES = {'NoLine':0, 'Solid':1,  'Dash':2,  'Dot':3, 'DashDot':4,  'DashDotDot':5}
class BaseMultiPlot(PlotWidget):
    MAX_NUM_TRACES = 15

    #symbolMap
    locals().update(**SYMBOLS)
    locals().update(**LINESTYLES)

    class lineStyleMap:
        locals().update(**LINESTYLES)

    class symbolMap:
        locals().update(**SYMBOLS)

    Q_ENUMS(symbolMap)
    Q_ENUMS(lineStyleMap)

    linestyledict = {NoLine:Qt.NoPen, Solid:Qt.SolidLine, Dash:Qt.DashLine, Dot:Qt.DotLine,
                     DashDot:Qt.DashDotLine, DashDotDot:Qt.DashDotDotLine}

    symboldict = { NoSymbol:None, Circle:'o',   Square:'s',  Triangle:'t',
                   Star:'star',   Pentagon:'p', Hexagon:'h', X:'x',
                   Cross:'+',     Diamond:'d'  }

    def __init__(self, parent=None, background='default',axisItems=None):

        self._yAxisCount = 1
        self._traceCount = 1

        #Main PlotItem
        if axisItems == None:
            self._XAxis1 = AxisItem("bottom")
            self._YAxis1 = AxisItem("left")
            self._YAxis2 = AxisItem("right")
        else:
            self._XAxis1 = axisItems['bottom']
            self._YAxis1 = axisItems['left']
            self._YAxis2 = axisItems['right']
        self._axisIndex = [self._XAxis1, self._YAxis1, self._YAxis2]
        self._axisItems = {'bottom': self._XAxis1, 'left': self._YAxis1, 'right': self._YAxis2}
        super(BaseMultiPlot, self).__init__(parent=parent, background=background, axisItems=self._axisItems)
        self.plotItem = self.getPlotItem()

        #Legend
        self.legend = LegendItem(size=None, offset=None)
        self.legend.setParentItem(self.plotItem.vb)
        self._showLegend = True

        #Another ViewBoxes to handle other traces
        #ViewBox2 associated to secondary Y Axis
        self.viewBox2 = ViewBox()
        self.plotItem.scene().addItem(self.viewBox2)
        self.viewBox2.setXLink(self.plotItem)
        #ViewBox3 associated to a new Y Axis
        self.viewBox3 = ViewBox()
        self.plotItem.scene().addItem(self.viewBox3)
        self.viewBox3.setXLink(self.plotItem)

        #Axis
        #Primary Axis (0 and 1)
        self._XAxis1Label = 'Primary X Axis (0)'
        self._XAxis1ShowLabel = False
        self._YAxis1Label = 'Primary Y Axis (1)'
        self._YAxis1ShowLabel = False
        self.plotItem.setLabels(bottom=self._XAxis1Label,left=self._YAxis1Label)
        self.setXAxis1ShowLabel(self._XAxis1ShowLabel)
        self.setYAxis1ShowLabel(self._YAxis1ShowLabel)
        #Secondary Y Axis (2)
        self._YAxis2Label = 'Secondary Y Axis (2)'
        self._YAxis2ShowLabel = False
        self.plotItem.getAxis('right').linkToView(self.viewBox2)
        self.plotItem.getAxis('right').setLabel(self._YAxis2Label)
        self.setYAxis2ShowLabel(self._YAxis2ShowLabel)
        self.plotItem.hideAxis('right')
        #Secondary Y Axis (3)
        self._YAxis3Label = 'Secondary Y AXis (3)'
        self._YAxis3ShowLabel = False
        self._YAxis3 = AxisItem('right')
        self._YAxis3.linkToView(self.viewBox3)
        self._YAxis3.setLabel(self._YAxis3Label)
        self.setYAxis3ShowLabel(self._YAxis3ShowLabel)
        self.plotItem.layout.addItem(self._YAxis3, 2, 3)
        self._YAxis3.setVisible(False)

        self.updateViews()
        self.plotItem.vb.sigResized.connect(self.updateViews)
        self._plotIndex = [None,self.plotItem,self.viewBox2,self.viewBox3]

        sz = default_cm.shape[0]
        pos = [i/(sz-1) for i in range(sz)]
        cm = ColorMap(pos, default_cm)
        colors = cm.mapToQColor(_np.linspace(0,1,self.MAX_NUM_TRACES))

        #Traces' Properties
        self.trace            = self.MAX_NUM_TRACES*[None]
        self._traceTitle      = self.MAX_NUM_TRACES*[None]
        self._tracePen        = self.MAX_NUM_TRACES*[None]
        self._traceYAxisIndex = self.MAX_NUM_TRACES*[1]
        self._traceSymbol     = self.MAX_NUM_TRACES*[0]
        self._traceVisible    = self.MAX_NUM_TRACES*[True]
        self._legendEntry     = self.MAX_NUM_TRACES*[None]
        for i in range(self.MAX_NUM_TRACES):
            self._traceTitle[i] = 'Trace '+ str(i)
            self._tracePen[i] = mkPen(colors[i],width=2)
            self.trace[i] =  PlotDataItem(pen=self._tracePen[i], symbol=None, name=self._traceTitle[i])

        #Initiate just trace0
        self.plotItem.addItem(self.trace[0])
        self.legend.addItem(self.trace[0],self._traceTitle[0])
        self._legendEntry[0] = self.legendGetAddedItem()

        self._title = None
        self._auto_range_XAxis = None
        self.setAutoRangeXAxis(True)
        self._auto_range_YAxis = None
        self.setAutoRangeYAxis(True)
        self._show_x_grid = None
        self.setShowXGrid(False)
        self._show_y_grid = None
        self.setShowYGrid(False)

    # Handle view resizing
    def updateViews(self):
        # view has resized; update auxiliary views to match
        self.viewBox2.setGeometry(self.plotItem.vb.sceneBoundingRect())
        self.viewBox3.setGeometry(self.plotItem.vb.sceneBoundingRect())

        # need to re-update linked axes since this was called incorrectly while views had different shapes.
        self.viewBox2.linkedViewChanged(self.plotItem.vb, self.viewBox2.XAxis)
        self.viewBox3.linkedViewChanged(self.plotItem.vb, self.viewBox3.XAxis)

    #count properties
    def getYAxisCount(self):
        return self._yAxisCount
    def setYAxisCount(self,value):
        if value >= 1 and value <= 4:
            if self._yAxisCount < 2 and value >= 2:
                self.plotItem.showAxis('right')
            if self._yAxisCount < 3 and value >= 3:
                self._YAxis3.setVisible(True)
                self._YAxis3._updateWidth()
                self._axisIndex.append(self._YAxis3)
            if self._yAxisCount >= 2 and value < 2:
                self.plotItem.hideAxis('right')
            if self._yAxisCount >= 3 and value < 3:
                self._YAxis3.setVisible(False)
                self._YAxis3.showLabel(False)
                self._axisIndex.remove(self._YAxis3)
            self._yAxisCount = value
            # print(value)
    def resetYAxisCount(self):
        self.setYAxisCount(1)
    yAxisCount = pyqtProperty(int,getYAxisCount,setYAxisCount,resetYAxisCount)

    #Plot properties
    def getAutoRangeXAxis(self):
        return self._auto_range_XAxis
    def setAutoRangeXAxis(self, value):
        self._auto_range_XAxis = value
        self.plotItem.enableAutoRange(ViewBox.XAxis,enable=self._auto_range_XAxis)
    def resetAutoRangeXAxis(self):
        self.setAutoRangeXAxis(True)
    autoRangeXAxis = pyqtProperty("bool", getAutoRangeXAxis, setAutoRangeXAxis, resetAutoRangeXAxis)

    def getAutoRangeYAxis(self):
        return self._auto_range_YAxis
    def setAutoRangeYAxis(self, value):
        self._auto_range_YAxis = value
        self.plotItem.enableAutoRange(ViewBox.YAxis,enable=self._auto_range_YAxis)
    def resetAutoRangeYAxis(self):
        self.setAutoRangeYAxis(True)
    autoRangeYAxis = pyqtProperty("bool", getAutoRangeYAxis, setAutoRangeYAxis, resetAutoRangeYAxis)

    def getShowXGrid(self):
        return self._show_x_grid
    def setShowXGrid(self, value):
        self._show_x_grid = value
        self.showGrid(x=self._show_x_grid)
    def resetShowXGrid(self):
        self.setShowXGrid(False)
    showXGrid = pyqtProperty("bool", getShowXGrid, setShowXGrid, resetShowXGrid)

    def getShowYGrid(self):
        return self._show_y_grid
    def setShowYGrid(self, value):
        self._show_y_grid = value
        self.showGrid(y=self._show_y_grid)
    def resetShowYGrid(self):
        self.setShowYGrid(False)
    showYGrid = pyqtProperty("bool", getShowYGrid, setShowYGrid, resetShowYGrid)

    def getBackgroundColor(self):
        return self.backgroundBrush().color()
    def setBackgroundColor(self, color):
        if self.backgroundBrush().color() != color:
                self.setBackgroundBrush(QBrush(color))
    backgroundColor = pyqtProperty(QColor, getBackgroundColor, setBackgroundColor)

    def getAxisColor(self):
        return self.getAxis('bottom')._pen.color()
    def setAxisColor(self, color):
        if self.getAxis('bottom')._pen.color() != color:
            self.getAxis('bottom').setPen(color)
            self.getAxis('left').setPen(color)
            self.getAxis('top').setPen(color)
            self.getAxis('right').setPen(color)
    axisColor = pyqtProperty(QColor, getAxisColor, setAxisColor)

    def getPlotTitle(self):
        return str(self._title)
    def setPlotTitle(self, value):
        self._title = str(value)
        self.setTitle(self._title)
    def resetPlotTitle(self):
        self._title = None
        self.setTitle(self._title)
    title = pyqtProperty(str, getPlotTitle, setPlotTitle, resetPlotTitle)

    def getShowLegend(self):
        return self._showLegend
    def setShowLegend(self, value):
        self._showLegend = value
        self.legend.setVisible(value)
    def resetShowLegend(self):
        self.setShowLegend(True)
    showLegend = pyqtProperty("bool", getShowLegend, setShowLegend, resetShowLegend)

    #Axis' properties
    def getXAxis1Label(self):
        return self._XAxis1Label
    def setXAxis1Label(self, label):
        self._XAxis1Label = label
        self.plotItem.getAxis('bottom').setLabel(self._XAxis1Label)
    XAxis1Label = pyqtProperty(str,getXAxis1Label,setXAxis1Label)

    def getXAxis1ShowLabel(self):
        return self._XAxis1ShowLabel
    def setXAxis1ShowLabel(self, showLabel):
        self._XAxis1ShowLabel = showLabel
        self.plotItem.getAxis('bottom').showLabel(showLabel)
    def resetXAxis1ShowLabel(self):
        self.plotItem.getAxis('bottom').showLabel(False)
    XAxis1ShowLabel = pyqtProperty(bool,getXAxis1ShowLabel,setXAxis1ShowLabel)

    def getYAxis1Label(self):
        return self._YAxis1Label
    def setYAxis1Label(self, label):
        self._YAxis1Label = label
        self.plotItem.getAxis('left').setLabel(self._YAxis1Label)
    YAxis1Label = pyqtProperty(str,getYAxis1Label,setYAxis1Label)

    def getYAxis1ShowLabel(self):
        return self._YAxis1ShowLabel
    def setYAxis1ShowLabel(self, showLabel):
        self._YAxis1ShowLabel = showLabel
        self.plotItem.getAxis('left').showLabel(showLabel)
    def resetYAxis1ShowLabel(self):
        self.plotItem.getAxis('left').showLabel(False)
    YAxis1ShowLabel = pyqtProperty(bool,getYAxis1ShowLabel,setYAxis1ShowLabel,resetYAxis1ShowLabel)

    def getYAxis2Label(self):
        return self._YAxis2Label
    def setYAxis2Label(self, label):
        self._YAxis2Label = label
        self.plotItem.getAxis('right').setLabel(self._YAxis2Label)
    YAxis2Label = pyqtProperty(str,getYAxis2Label,setYAxis2Label)

    def getYAxis2ShowLabel(self):
        return self._YAxis2ShowLabel
    def setYAxis2ShowLabel(self, showLabel):
        self._YAxis2ShowLabel = showLabel
        self.plotItem.getAxis('right').showLabel(showLabel)
    def resetYAxis2ShowLabel(self):
        self.plotItem.getAxis('right').showLabel(False)
    YAxis2ShowLabel = pyqtProperty(bool,getYAxis2ShowLabel,setYAxis2ShowLabel,resetYAxis2ShowLabel)

    def getYAxis3Label(self):
        return self._YAxis3Label
    def setYAxis3Label(self, label):
        self._YAxis3Label = label
        self._YAxis3.setLabel(self._YAxis3Label)
    YAxis3Label = pyqtProperty(str,getYAxis3Label,setYAxis3Label)

    def getYAxis3ShowLabel(self):
        return self._YAxis3ShowLabel
    def setYAxis3ShowLabel(self, showLabel):
        self._YAxis3ShowLabel = showLabel
        self._YAxis3.showLabel(showLabel)
    def resetYAxis3ShowLabel(self):
        self._YAxis3.showLabel(False)
    YAxis3ShowLabel = pyqtProperty(bool,getYAxis3ShowLabel,setYAxis3ShowLabel,resetYAxis3ShowLabel)

    ############################ TRACES PROPERTIES #################################
    @pyqtProperty(int)
    def tracesCount(self):     return self._traceCount
    @tracesCount.setter
    def tracesCount(self,value):
        value = min(max(value,1),self.MAX_NUM_TRACES)
        old_val = self._traceCount
        self._traceCount = value
        if old_val < value:
            for i in range(old_val,value):
                trYAxInd = self._traceYAxisIndex[i]
                tr   = self.trace[i]
                trTt = self._traceTitle[i]
                self._plotIndex[trYAxInd].addItem(tr)
                tr.setVisible(self._traceVisible[i])
                if trTt:
                    self.legend.addItem(tr,trTt)
                    self._legendEntry[i] = self.legendGetAddedItem()
        else:
            for i in range(value,old_val):
                trYAxInd = self._traceYAxisIndex[i]
                self._plotIndex[trYAxInd].removeItem(self.trace[i])
                if self._legendEntry[i]:
                    self.legendRemoveItem(self._legendEntry[i])

    ######## Individual Traces Properties ###########
    for i in range(MAX_NUM_TRACES):
        exec(TRACES_CONFIGS.format(i))

    #Legend complementary methods
    def legendGetAddedItem(self):
        """This function should be called shortly after adding a new item in the Legend,
        so that this item can be removed later"""
        return self.legend.items[-1][0]

    def legendRemoveItem(self, item):
        """Removes Item from Legend from the id returned by legendGetAddedItem method"""
        for sample, label in self.legend.items:
            if sample == item:  # hit
                self.legend.items.remove( (sample, label) )    # remove from itemlist
                self.legend.layout.removeItem(sample)          # remove from layout
                sample.close()                                 # remove from drawing
                self.legend.layout.removeItem(label)
                label.close()
                self.legendUpdateSize()                       # redraq box

    def legendUpdateSize(self):
        height = 0
        width = 0
        for sample, label in self.legend.items:
            height += max(sample.height(), label.height()) + 3
            width = max(width, sample.width()+min(label.width(),100))
        self.legend.setGeometry(0, 0, width, height)
