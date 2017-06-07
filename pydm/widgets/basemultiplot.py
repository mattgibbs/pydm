from ..PyQt.QtGui import QColor, QBrush
from ..PyQt.QtCore import pyqtSlot, pyqtProperty, Q_ENUMS
# from pyqtgraph import GraphicsLayoutWidget, PlotItem, AxisItem, PlotDataItem, ViewBox
from pyqtgraph import PlotWidget, PlotItem, AxisItem, PlotDataItem, ViewBox, mkPen, mkBrush, LegendItem

TRACES_PROPERTIES = '''
@pyqtSlot(bool)
def trace{0}setVisible(self,value):
    if value:
        self.trace{0}.setPen(self.trace{0}Color,width=2)
        self.trace{0}.setSymbol(self.symboldict[self.trace{0}Symbol])
        self.trace{0}.setSymbolPen(self.trace{0}Color)
        self.trace{0}.setSymbolBrush(self.trace{0}Color)
        self.trace{0}.setSymbolSize(8)
    else:
        self.trace{0}.setPen(None)
        self.trace{0}.setSymbol(None)
    self.trace{0}Visible = value

@pyqtSlot(bool)
def trace{0}toggle_line_scatter(self,value):
    if self.trace{0}Visible:
        if value:
            self.trace{0}.setPen(self.trace{0}Color,width=2)
            self.trace{0}.setSymbol(None)
        else:
            self.trace{0}.setPen(None)
            self.trace{0}.setSymbol(self.symboldict[1])
            self.trace{0}.setSymbolPen(self.trace{0}Color)
            self.trace{0}.setSymbolBrush(self.trace{0}Color)
            self.trace{0}.setSymbolSize(8)

def getTrace{0}Interpolate(self):
    return self.trace{0}Interpolate

def setTrace{0}Interpolate(self,value):
    if value:
        self.trace{0}.setPen(self.trace{0}Color,width=2)
    else:
        self.trace{0}.setPen(None)
    self.trace{0}Interpolate = value

def resetTrace{0}Interpolate(self):
    self.setTrace{0}Interpolate(True)

Trace{0}Interpolate = pyqtProperty(bool,getTrace{0}Interpolate,setTrace{0}Interpolate,resetTrace{0}Interpolate)

def getTrace{0}Symbol(self):
    return self.trace{0}Symbol

def setTrace{0}Symbol(self,value):
    self.trace{0}.setSymbol(self.symboldict[value])
    self.trace{0}.setSymbolPen(self.trace{0}Color)
    self.trace{0}.setSymbolBrush(self.trace{0}Color)
    self.trace{0}.setSymbolSize(8)
    self.trace{0}Symbol = value

def resetTrace{0}Symbol(self):
    self.setTrace{0}Symbol(0)

Trace{0}Symbol = pyqtProperty(symbolMap,getTrace{0}Symbol,setTrace{0}Symbol,resetTrace{0}Symbol)

def getTrace{0}Color(self):
    return self.trace{0}Color

def setTrace{0}Color(self, color):
    if self.trace{0}Color != color:
        self.trace{0}Color = color
        self.trace{0}.setPen(self.trace{0}Color,width=2)

Trace{0}Color = pyqtProperty(QColor,getTrace{0}Color,setTrace{0}Color)

def getTrace{0}YAxisIndex(self):
    return self.trace{0}YAxisIndex

def setTrace{0}YAxisIndex(self,new_axis):
    if new_axis in [1,2,3]:
        self._plotIndex[self.trace{0}YAxisIndex].removeItem(self.trace{0})
        self._plotIndex[new_axis].addItem(self.trace{0})
        self.trace{0}YAxisIndex = new_axis
        # print(new_axis)

Trace{0}YAxisIndex = pyqtProperty(int,getTrace{0}YAxisIndex,setTrace{0}YAxisIndex)

def getTrace{0}Title(self):
    return str(self.trace{0}Title)

def setTrace{0}Title(self, value):
    self.legendRemoveItem(self._t{0})
    self.trace{0}Title = str(value)
    self.legend.addItem(self.trace{0},self.trace{0}Title)
    self._t{0} = self.legendGetAddedItem()

def resetTrace{0}Title(self):
    self.setTrace{0}Title('Trace {0}')

Trace{0}Title = pyqtProperty(str, getTrace{0}Title, setTrace{0}Title, resetTrace{0}Title)
'''


SYMBOLS = {'NoSymbol' : 0, 'Circle' : 1,   'Square' : 2,  'Triangle' : 3,
           'Star' : 4,     'Pentagon' : 5, 'Hexagon' : 6, 'X' : 7,
           'Cross' : 8,    'Diamond' : 9}

class BaseMultiPlot(PlotWidget):
    MAX_NUM_TRACES = 15

    #symbolMap
    locals().update(**SYMBOLS)

    class symbolMap:
        locals().update(**SYMBOLS)

    Q_ENUMS(symbolMap)

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

        colors = [ QColor(255,0,0),   QColor(0,0,255),   QColor(0,255,0),   QColor(255,128,0),
                   QColor(255,255,0), QColor(0,255,128), QColor(0,255,255), QColor(0,128,255),
                   QColor(127,0,255), QColor(255,0,255), QColor(255,0,127), QColor(128,128,128),
                   QColor(102,0,0),   QColor(0,102,0),   QColor(0,0,102) ]

        #Traces' Properties
        for i in range(self.MAX_NUM_TRACES):
            tr = 'trace'+str(i)
            setattr(self,tr + 'Color', colors[i])
            setattr(self,tr + 'Title', 'Trace '+ str(i))
            setattr(self,tr, PlotDataItem(pen=mkPen(colors[i],width=2), symbol=None, name='Trace'+str(i)))
            setattr(self,tr + 'YAxisIndex', 1)
            setattr(self,tr + 'Interpolate', True)
            setattr(self,tr + 'Symbol', 0)
            setattr(self,tr + 'Visible', True)

        #Initiate just trace0
        self.plotItem.addItem(self.trace0)
        self.legend.addItem(self.trace0,self.trace0Title)
        self._t0 = self.legendGetAddedItem()


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

    def getTracesCount(self):
        return self._traceCount

    def setTracesCount(self,value):
        ## proposed code
        if not (1 <= value <= self.MAX_NUM_TRACES): return
        old_val = self._traceCount
        self._traceCount = value
        if old_val < value:
            for i in range(old_val,value):
                v = str(i)
                attr_trYAxInd = getattr(self,'trace'+v+'YAxisIndex')
                attr_tr = getattr(self,'trace'+v)
                attr_trTt = getattr(self,'trace'+v+'Title')
                self._plotIndex[attr_trYAxInd].addItem(attr_tr)
                self.legend.addItem(attr_tr,attr_trTt)
                setattr(self,'_t'+v, self.legendAddedItem())
        else:
            for i in range(value,old_val):
                v = str(i)
                attr_trYAxInd = getattr(self,'trace'+v+'YAxisIndex')
                attr_tr = getattr(self,'trace'+v)
                attr_ti = getattr(self,'_t'+v)
                self._plotIndex[attr_trYAxInd].removeItem(attr_tr)
                self.legendRemoveItem(attr_ti)

    def resetTracesCount(self):
        self.setTracesCount(1)

    tracesCount = pyqtProperty(int,getTracesCount,setTracesCount,resetTracesCount)

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

    #Traces' properties
    for i in range(MAX_NUM_TRACES):
        exec(TRACES_PROPERTIES.format(i))

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
