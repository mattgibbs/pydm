from ..PyQt.QtGui import QColor, QBrush
from ..PyQt.QtCore import pyqtProperty
# from pyqtgraph import GraphicsLayoutWidget, PlotItem, AxisItem, PlotCurveItem, ViewBox
from pyqtgraph import PlotWidget, PlotItem, AxisItem, PlotCurveItem, ViewBox, mkPen, LegendItem

class BaseMultiPlot(PlotWidget):

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

        #Traces' Colors
        self.trace0Color = QColor(255,0,0)
        self.trace1Color = QColor(0,0,255)
        self.trace2Color = QColor(0,255,0)
        self.trace3Color = QColor(255,128,0)
        self.trace4Color = QColor(255,255,0)
        self.trace5Color = QColor(0,255,128)
        self.trace6Color = QColor(0,255,255)
        self.trace7Color = QColor(0,128,255)
        self.trace8Color = QColor(127,0,255)
        self.trace9Color = QColor(255,0,255)
        self.trace10Color = QColor(255,0,127)
        self.trace11Color = QColor(128,128,128)
        self.trace12Color = QColor(102,0,0)
        self.trace13Color = QColor(0,102,0)
        self.trace14Color = QColor(0,0,102)

        #Traces' Names
        self.trace0Title = 'Trace 0'
        self.trace1Title = 'Trace 1'
        self.trace2Title = 'Trace 2'
        self.trace3Title = 'Trace 3'
        self.trace4Title = 'Trace 4'
        self.trace5Title = 'Trace 5'
        self.trace6Title = 'Trace 6'
        self.trace7Title = 'Trace 7'
        self.trace8Title = 'Trace 8'
        self.trace9Title = 'Trace 9'
        self.trace10Title = 'Trace 10'
        self.trace11Title = 'Trace 11'
        self.trace12Title = 'Trace 12'
        self.trace13Title = 'Trace 13'
        self.trace14Title = 'Trace 14'

        #Possible traces
        self.trace0 = PlotCurveItem(pen=mkPen(self.trace0Color,width=2),name=self.trace0Title)
        self.plotItem.addItem(self.trace0)                              #Initiate just trace0
        self.legend.addItem(self.trace0,self.trace0Title)
        self._t0 = self.legendGetAddedItem()
        self.trace1 = PlotCurveItem(pen=mkPen(self.trace1Color,width=2),name=self.trace1Title)
        self.trace2 = PlotCurveItem(pen=mkPen(self.trace2Color,width=2),name=self.trace2Title)
        self.trace3 = PlotCurveItem(pen=mkPen(self.trace3Color,width=2),name=self.trace3Title)
        self.trace4 = PlotCurveItem(pen=mkPen(self.trace4Color,width=2),name=self.trace4Title)
        self.trace5 = PlotCurveItem(pen=mkPen(self.trace5Color,width=2),name=self.trace5Title)
        self.trace6 = PlotCurveItem(pen=mkPen(self.trace6Color,width=2),name=self.trace6Title)
        self.trace7 = PlotCurveItem(pen=mkPen(self.trace7Color,width=2),name=self.trace7Title)
        self.trace8 = PlotCurveItem(pen=mkPen(self.trace8Color,width=2),name=self.trace8Title)
        self.trace9 = PlotCurveItem(pen=mkPen(self.trace9Color,width=2),name=self.trace9Title)
        self.trace10 = PlotCurveItem(pen=mkPen(self.trace10Color,width=2),name=self.trace10Title)
        self.trace11 = PlotCurveItem(pen=mkPen(self.trace11Color,width=2),name=self.trace11Title)
        self.trace12 = PlotCurveItem(pen=mkPen(self.trace12Color,width=2),name=self.trace12Title)
        self.trace13 = PlotCurveItem(pen=mkPen(self.trace13Color,width=2),name=self.trace13Title)
        self.trace14 = PlotCurveItem(pen=mkPen(self.trace14Color,width=2),name=self.trace14Title)

        #Traces' Y Axis
        self.trace0YAxisIndex = 1
        self.trace1YAxisIndex = 1
        self.trace2YAxisIndex = 1
        self.trace3YAxisIndex = 1
        self.trace4YAxisIndex = 1
        self.trace5YAxisIndex = 1
        self.trace6YAxisIndex = 1
        self.trace7YAxisIndex = 1
        self.trace8YAxisIndex = 1
        self.trace9YAxisIndex = 1
        self.trace10YAxisIndex = 1
        self.trace11YAxisIndex = 1
        self.trace12YAxisIndex = 1
        self.trace13YAxisIndex = 1
        self.trace14YAxisIndex = 1

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
        if value >= 1 and value <= 15:
            if self._traceCount < 2 and value >= 2:
                self._plotIndex[self.trace1YAxisIndex].addItem(self.trace1)
                self.legend.addItem(self.trace1,self.trace1Title)
                self._t1 = self.legendGetAddedItem()
            if self._traceCount < 3 and value >= 3:
                self._plotIndex[self.trace2YAxisIndex].addItem(self.trace2)
                self.legend.addItem(self.trace2,self.trace2Title)
                self._t2 = self.legendGetAddedItem()
            if self._traceCount < 4 and value >= 4:
                self._plotIndex[self.trace3YAxisIndex].addItem(self.trace3)
                self.legend.addItem(self.trace3,self.trace3Title)
                self._t3 = self.legendGetAddedItem()
            if self._traceCount < 5 and value >= 5:
                self._plotIndex[self.trace4YAxisIndex].addItem(self.trace4)
                self.legend.addItem(self.trace4,self.trace4Title)
                self._t4 = self.legendGetAddedItem()
            if self._traceCount < 6 and value >= 6:
                self._plotIndex[self.trace5YAxisIndex].addItem(self.trace5)
                self.legend.addItem(self.trace5,self.trace5Title)
                self._t5 = self.legendGetAddedItem()
            if self._traceCount < 7 and value >= 7:
                self._plotIndex[self.trace6YAxisIndex].addItem(self.trace6)
                self.legend.addItem(self.trace6,self.trace6Title)
                self._t6 = self.legendGetAddedItem()
            if self._traceCount < 8 and value >= 8:
                self._plotIndex[self.trace7YAxisIndex].addItem(self.trace7)
                self.legend.addItem(self.trace7,self.trace7Title)
                self._t7 = self.legendGetAddedItem()
            if self._traceCount < 9 and value >= 9:
                self._plotIndex[self.trace8YAxisIndex].addItem(self.trace8)
                self.legend.addItem(self.trace8,self.trace8Title)
                self._t8 = self.legendGetAddedItem()
            if self._traceCount < 10 and value >= 10:
                self._plotIndex[self.trace9YAxisIndex].addItem(self.trace9)
                self.legend.addItem(self.trace9,self.trace9Title)
                self._t9 = self.legendGetAddedItem()
            if self._traceCount < 11 and value >= 11:
                self._plotIndex[self.trace10YAxisIndex].addItem(self.trace10)
                self.legend.addItem(self.trace10,self.trace10Title)
                self._t10 = self.legendGetAddedItem()
            if self._traceCount < 12 and value >= 12:
                self._plotIndex[self.trace11YAxisIndex].addItem(self.trace11)
                self.legend.addItem(self.trace11,self.trace11Title)
                self._t11 = self.legendGetAddedItem()
            if self._traceCount < 13 and value >= 13:
                self._plotIndex[self.trace12YAxisIndex].addItem(self.trace12)
                self.legend.addItem(self.trace12,self.trace12Title)
                self._t12 = self.legendGetAddedItem()
            if self._traceCount < 14 and value >= 14:
                self._plotIndex[self.trace13YAxisIndex].addItem(self.trace13)
                self.legend.addItem(self.trace13,self.trace13Title)
                self._t13 = self.legendGetAddedItem()
            if self._traceCount < 15 and value >= 15:
                self._plotIndex[self.trace14YAxisIndex].addItem(self.trace14)
                self.legend.addItem(self.trace14,self.trace14Title)
                self._t14 = self.legendGetAddedItem()

            if self._traceCount >= 2 and value < 2:
                self._plotIndex[self.trace1YAxisIndex].removeItem(self.trace1)
                self.legendRemoveItem(self._t1)
            if self._traceCount >= 3 and value < 3:
                self._plotIndex[self.trace2YAxisIndex].removeItem(self.trace2)
                self.legendRemoveItem(self._t2)
            if self._traceCount >= 4 and value < 4:
                self._plotIndex[self.trace3YAxisIndex].removeItem(self.trace3)
                self.legendRemoveItem(self._t3)
            if self._traceCount >= 5 and value < 5:
                self._plotIndex[self.trace4YAxisIndex].removeItem(self.trace4)
                self.legendRemoveItem(self._t4)
            if self._traceCount >= 6 and value < 6:
                self._plotIndex[self.trace5YAxisIndex].removeItem(self.trace5)
                self.legendRemoveItem(self._t5)
            if self._traceCount >= 7 and value < 7:
                self._plotIndex[self.trace6YAxisIndex].removeItem(self.trace6)
                self.legendRemoveItem(self._t6)
            if self._traceCount >= 8 and value < 8:
                self._plotIndex[self.trace7YAxisIndex].removeItem(self.trace7)
                self.legendRemoveItem(self._t7)
            if self._traceCount >= 9 and value < 9:
                self._plotIndex[self.trace8YAxisIndex].removeItem(self.trace8)
                self.legendRemoveItem(self._t8)
            if self._traceCount >= 10 and value < 10:
                self._plotIndex[self.trace9YAxisIndex].removeItem(self.trace9)
                self.legendRemoveItem(self._t9)
            if self._traceCount >= 11 and value < 11:
                self._plotIndex[self.trace10YAxisIndex].removeItem(self.trace10)
                self.legendRemoveItem(self._t10)
            if self._traceCount >= 12 and value < 12:
                self._plotIndex[self.trace11YAxisIndex].removeItem(self.trace11)
                self.legendRemoveItem(self._t11)
            if self._traceCount >= 13 and value < 13:
                self._plotIndex[self.trace12YAxisIndex].removeItem(self.trace12)
                self.legendRemoveItem(self._t12)
            if self._traceCount >= 14 and value < 14:
                self._plotIndex[self.trace13YAxisIndex].removeItem(self.trace13)
                self.legendRemoveItem(self._t13)
            if self._traceCount >= 15 and value < 15:
                self._plotIndex[self.trace14YAxisIndex].removeItem(self.trace14)
                self.legendRemoveItem(self._t14)
            self._traceCount = value
            # print(value)

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

    def getTrace0Color(self):
        return self.trace0Color

    def setTrace0Color(self, color):
        if self.trace0Color != color:
            self.trace0Color = color
            self.trace0.setPen(self.trace0Color)

    Trace0Colour = pyqtProperty(QColor,getTrace0Color,setTrace0Color)

    def getTrace0YAxisIndex(self):
        return self.trace0YAxisIndex

    def setTrace0YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace0YAxisIndex].removeItem(self.trace0)
            self._plotIndex[new_axis].addItem(self.trace0)
            self.trace0YAxisIndex = new_axis
            # print(new_axis)

    Trace0YAxisIndex = pyqtProperty(int,getTrace0YAxisIndex,setTrace0YAxisIndex)

    def getTrace0Title(self):
        return str(self.trace0Title)

    def setTrace0Title(self, value):
        self.legendRemoveItem(self._t0)
        self.trace0Title = str(value)
        self.legend.addItem(self.trace0,self.trace0Title)
        self._t0 = self.legendGetAddedItem()

    def resetTrace0Title(self):
        self.setTrace0Title('Trace 0')

    Trace0Title = pyqtProperty(str, getTrace0Title, setTrace0Title, resetTrace0Title)

    def getTrace1Color(self):
        # print(self.trace1Color)
        return self.trace1Color

    def setTrace1Color(self, color):
        if self.trace1Color != color:
            self.trace1Color = color
            self.trace1.setPen(self.trace1Color)

    Trace1Colour = pyqtProperty(QColor,getTrace1Color,setTrace1Color)

    def getTrace1YAxisIndex(self):
        return self.trace1YAxisIndex

    def setTrace1YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace1YAxisIndex].removeItem(self.trace1)
            self._plotIndex[new_axis].addItem(self.trace1)
            self.trace1YAxisIndex = new_axis
            # print(new_axis)

    Trace1YAxisIndex = pyqtProperty(int,getTrace1YAxisIndex,setTrace1YAxisIndex)

    def getTrace1Title(self):
        return str(self.trace1Title)

    def setTrace1Title(self, value):
        if self._traceCount > 1:
            self.legendRemoveItem(self._t1)
            self.trace1Title = str(value)
            self.legend.addItem(self.trace1,self.trace1Title)
            self._t1 = self.legendGetAddedItem()

    def resetTrace1Title(self):
        self.setTrace1Title('Trace 1')

    Trace1Title = pyqtProperty(str, getTrace1Title, setTrace1Title, resetTrace1Title)

    def getTrace2Color(self):
        return self.trace2Color

    def setTrace2Color(self, color):
        if self.trace2Color != color:
            self.trace2Color = color
            self.trace2.setPen(self.trace2Color)

    Trace2Colour = pyqtProperty(QColor,getTrace2Color,setTrace2Color)

    def getTrace2YAxisIndex(self):
        return self.trace2YAxisIndex

    def setTrace2YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace2YAxisIndex].removeItem(self.trace2)
            self._plotIndex[new_axis].addItem(self.trace2)
            self.trace2YAxisIndex = new_axis
            # print(new_axis)

    Trace2YAxisIndex = pyqtProperty(int,getTrace2YAxisIndex,setTrace2YAxisIndex)

    def getTrace2Title(self):
        return str(self.trace2Title)

    def setTrace2Title(self, value):
        if self._traceCount > 2:
            self.legendRemoveItem(self._t2)
            self.trace2Title = str(value)
            self.legend.addItem(self.trace2,self.trace2Title)
            self._t2 = self.legendGetAddedItem()

    def resetTrace2Title(self):
        self.setTrace2Title('Trace 2')

    Trace2Title = pyqtProperty(str, getTrace2Title, setTrace2Title, resetTrace2Title)

    def getTrace3Color(self):
        return self.trace3Color

    def setTrace3Color(self, color):
        if self.trace3Color != color:
            self.trace3Color = color
            self.trace3.setPen(self.trace3Color)

    Trace3Colour = pyqtProperty(QColor,getTrace3Color,setTrace3Color)

    def getTrace3YAxisIndex(self):
        return self.trace3YAxisIndex

    def setTrace3YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace3YAxisIndex].removeItem(self.trace3)
            self._plotIndex[new_axis].addItem(self.trace3)
            self.trace3YAxisIndex = new_axis
            # print(new_axis)

    Trace3YAxisIndex = pyqtProperty(int,getTrace3YAxisIndex,setTrace3YAxisIndex)

    def getTrace3Title(self):
        return str(self.trace3Title)

    def setTrace3Title(self, value):
        if self._traceCount > 3:
            self.legendRemoveItem(self._t3)
            self.trace3Title = str(value)
            self.legend.addItem(self.trace3,self.trace3Title)
            self._t3 = self.legendGetAddedItem()

    def resetTrace3Title(self):
        self.setTrace3Title('Trace 3')

    Trace3Title = pyqtProperty(str, getTrace3Title, setTrace3Title, resetTrace3Title)

    def getTrace4Color(self):
        return self.trace4Color

    def setTrace4Color(self, color):
        if self.trace4Color != color:
            self.trace4Color = color
            self.trace4.setPen(self.trace4Color)

    Trace4Colour = pyqtProperty(QColor,getTrace4Color,setTrace4Color)

    def getTrace4YAxisIndex(self):
        return self.trace4YAxisIndex

    def setTrace4YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace4YAxisIndex].removeItem(self.trace4)
            self._plotIndex[new_axis].addItem(self.trace4)
            self.trace4YAxisIndex = new_axis
            # print(new_axis)

    Trace4YAxisIndex = pyqtProperty(int,getTrace4YAxisIndex,setTrace4YAxisIndex)

    def getTrace4Title(self):
        return str(self.trace4Title)

    def setTrace4Title(self, value):
        if self._traceCount > 4:
            self.legendRemoveItem(self._t4)
            self.trace4Title = str(value)
            self.legend.addItem(self.trace4,self.trace4Title)
            self._t4 = self.legendGetAddedItem()

    def resetTrace4Title(self):
        self.setTrace1Title('Trace 4')

    Trace4Title = pyqtProperty(str, getTrace4Title, setTrace4Title, resetTrace4Title)

    def getTrace5Color(self):
        return self.trace5Color

    def setTrace5Color(self, color):
        if self.trace5Color != color:
            self.trace5Color = color
            self.trace5.setPen(self.trace5Color)

    Trace5Colour = pyqtProperty(QColor,getTrace5Color,setTrace5Color)

    def getTrace5YAxisIndex(self):
        return self.trace5YAxisIndex

    def setTrace5YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace5YAxisIndex].removeItem(self.trace5)
            self._plotIndex[new_axis].addItem(self.trace5)
            self.trace5YAxisIndex = new_axis
            # print(new_axis)

    Trace5YAxisIndex = pyqtProperty(int,getTrace5YAxisIndex,setTrace5YAxisIndex)

    def getTrace5Title(self):
        return str(self.trace5Title)

    def setTrace5Title(self, value):
        if self._traceCount > 5:
            self.legendRemoveItem(self._t5)
            self.trace5Title = str(value)
            self.legend.addItem(self.trace5,self.trace5Title)
            self._t5 = self.legendGetAddedItem()

    def resetTrace5Title(self):
        self.setTrace1Title('Trace 5')

    Trace5Title = pyqtProperty(str, getTrace5Title, setTrace5Title, resetTrace5Title)

    def getTrace6Color(self):
        return self.trace6Color

    def setTrace6Color(self, color):
        if self.trace6Color != color:
            self.trace6Color = color
            self.trace6.setPen(self.trace6Color)

    Trace6Colour = pyqtProperty(QColor,getTrace6Color,setTrace6Color)

    def getTrace6YAxisIndex(self):
        return self.trace6YAxisIndex

    def setTrace6YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace6YAxisIndex].removeItem(self.trace6)
            self._plotIndex[new_axis].addItem(self.trace6)
            self.trace6YAxisIndex = new_axis
            # print(new_axis)

    Trace6YAxisIndex = pyqtProperty(int,getTrace6YAxisIndex,setTrace6YAxisIndex)

    def getTrace6Title(self):
        return str(self.trace6Title)

    def setTrace6Title(self, value):
        if self._traceCount > 6:
            self.legendRemoveItem(self._t6)
            self.trace6Title = str(value)
            self.legend.addItem(self.trace6,self.trace6Title)
            self._t6 = self.legendGetAddedItem()

    def resetTrace6Title(self):
        self.setTrace6Title('Trace 6')

    Trace6Title = pyqtProperty(str, getTrace6Title, setTrace6Title, resetTrace6Title)

    def getTrace7Color(self):
        return self.trace7Color

    def setTrace7Color(self, color):
        if self.trace7Color != color:
            self.trace7Color = color
            self.trace7.setPen(self.trace7Color)

    Trace7Colour = pyqtProperty(QColor,getTrace7Color,setTrace7Color)

    def getTrace7YAxisIndex(self):
        return self.trace7YAxisIndex

    def setTrace7YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace7YAxisIndex].removeItem(self.trace7)
            self._plotIndex[new_axis].addItem(self.trace7)
            self.trace7YAxisIndex = new_axis
            # print(new_axis)

    Trace7YAxisIndex = pyqtProperty(int,getTrace7YAxisIndex,setTrace7YAxisIndex)

    def getTrace7Title(self):
        return str(self.trace7Title)

    def setTrace7Title(self, value):
        if self._traceCount > 7:
            self.legendRemoveItem(self._t7)
            self.trace7Title = str(value)
            self.legend.addItem(self.trace7,self.trace7Title)
            self._t7 = self.legendGetAddedItem()

    def resetTrace7Title(self):
        self.setTrace7Title('Trace 7')

    Trace7Title = pyqtProperty(str, getTrace7Title, setTrace7Title, resetTrace7Title)

    def getTrace8Color(self):
        return self.trace8Color

    def setTrace8Color(self, color):
        if self.trace8Color != color:
            self.trace8Color = color
            self.trace8.setPen(self.trace8Color)

    Trace8Colour = pyqtProperty(QColor,getTrace8Color,setTrace8Color)

    def getTrace8YAxisIndex(self):
        return self.trace8YAxisIndex

    def setTrace8YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace8YAxisIndex].removeItem(self.trace8)
            self._plotIndex[new_axis].addItem(self.trace8)
            self.trace8YAxisIndex = new_axis
            # print(new_axis)

    Trace8YAxisIndex = pyqtProperty(int,getTrace8YAxisIndex,setTrace8YAxisIndex)

    def getTrace8Title(self):
        return str(self.trace8Title)

    def setTrace8Title(self, value):
        if self._traceCount > 8:
            self.legendRemoveItem(self._t8)
            self.trace8Title = str(value)
            self.legend.addItem(self.trace8,self.trace8Title)
            self._t8 = self.legendGetAddedItem()

    def resetTrace8Title(self):
        self.setTrace8Title('Trace 8')

    Trace8Title = pyqtProperty(str, getTrace8Title, setTrace8Title, resetTrace8Title)

    def getTrace9Color(self):
        return self.trace9Color

    def setTrace9Color(self, color):
        if self.trace9Color != color:
            self.trace9Color = color
            self.trace9.setPen(self.trace9Color)

    Trace9Colour = pyqtProperty(QColor,getTrace9Color,setTrace9Color)

    def getTrace9YAxisIndex(self):
        return self.trace9YAxisIndex

    def setTrace9YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace9YAxisIndex].removeItem(self.trace9)
            self._plotIndex[new_axis].addItem(self.trace9)
            self.trace9YAxisIndex = new_axis
            # print(new_axis)

    Trace9YAxisIndex = pyqtProperty(int,getTrace9YAxisIndex,setTrace9YAxisIndex)

    def getTrace9Title(self):
        return str(self.trace9Title)

    def setTrace9Title(self, value):
        if self._traceCount > 9:
            self.legendRemoveItem(self._t9)
            self.trace9Title = str(value)
            self.legend.addItem(self.trace9,self.trace9Title)
            self._t9 = self.legendGetAddedItem()

    def resetTrace9Title(self):
        self.setTrace9Title('Trace 9')

    Trace9Title = pyqtProperty(str, getTrace9Title, setTrace9Title, resetTrace9Title)

    def getTrace10Color(self):
        return self.trace10Color

    def setTrace10Color(self, color):
        if self.trace10Color != color:
            self.trace10Color = color
            self.trace10.setPen(self.trace10Color)

    Trace10Colour = pyqtProperty(QColor,getTrace10Color,setTrace10Color)

    def getTrace10YAxisIndex(self):
        return self.trace10YAxisIndex

    def setTrace10YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace10YAxisIndex].removeItem(self.trace10)
            self._plotIndex[new_axis].addItem(self.trace10)
            self.trace10YAxisIndex = new_axis
            # print(new_axis)

    Trace10YAxisIndex = pyqtProperty(int,getTrace10YAxisIndex,setTrace10YAxisIndex)

    def getTrace10Title(self):
        return str(self.trace10Title)

    def setTrace10Title(self, value):
        if self._traceCount > 10:
            self.legendRemoveItem(self._t10)
            self.trace10Title = str(value)
            self.legend.addItem(self.trace10,self.trace10Title)
            self._t10 = self.legendGetAddedItem()

    def resetTrace10Title(self):
        self.setTrace10Title('Trace 10')

    Trace10Title = pyqtProperty(str, getTrace10Title, setTrace10Title, resetTrace10Title)

    def getTrace11Color(self):
        return self.trace11Color

    def setTrace11Color(self, color):
        if self.trace11Color != color:
            self.trace11Color = color
            self.trace11.setPen(self.trace11Color)

    Trace11Colour = pyqtProperty(QColor,getTrace11Color,setTrace11Color)

    def getTrace11YAxisIndex(self):
        return self.trace11YAxisIndex

    def setTrace11YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace11YAxisIndex].removeItem(self.trace11)
            self._plotIndex[new_axis].addItem(self.trace11)
            self.trace11YAxisIndex = new_axis
            # print(new_axis)

    Trace11YAxisIndex = pyqtProperty(int,getTrace11YAxisIndex,setTrace11YAxisIndex)

    def getTrace11Title(self):
        return str(self.trace11Title)

    def setTrace11Title(self, value):
        if self._traceCount > 11:
            self.legendRemoveItem(self._t11)
            self.trace11Title = str(value)
            self.legend.addItem(self.trace11,self.trace11Title)
            self._t11 = self.legendGetAddedItem()

    def resetTrace11Title(self):
        self.setTrace11Title('Trace 11')

    Trace11Title = pyqtProperty(str, getTrace11Title, setTrace11Title, resetTrace11Title)

    def getTrace12Color(self):
        return self.trace12Color

    def setTrace12Color(self, color):
        if self.trace12Color != color:
            self.trace12Color = color
            self.trace12.setPen(self.trace12Color)

    Trace12Colour = pyqtProperty(QColor,getTrace12Color,setTrace12Color)

    def getTrace12YAxisIndex(self):
        return self.trace12YAxisIndex

    def setTrace12YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace12YAxisIndex].removeItem(self.trace12)
            self._plotIndex[new_axis].addItem(self.trace12)
            self.trace12YAxisIndex = new_axis
            # print(new_axis)

    Trace12YAxisIndex = pyqtProperty(int,getTrace12YAxisIndex,setTrace12YAxisIndex)

    def getTrace12Title(self):
        return str(self.trace12Title)

    def setTrace12Title(self, value):
        if self._traceCount > 12:
            self.legendRemoveItem(self._t12)
            self.trace12Title = str(value)
            self.legend.addItem(self.trace12,self.trace12Title)
            self._t12 = self.legendGetAddedItem()

    def resetTrace12Title(self):
        self.setTrace12Title('Trace 12')

    Trace12Title = pyqtProperty(str, getTrace12Title, setTrace12Title, resetTrace12Title)

    def getTrace13Color(self):
        return self.trace13Color

    def setTrace13Color(self, color):
        if self.trace13Color != color:
            self.trace13Color = color
            self.trace13.setPen(self.trace13Color)

    Trace13Colour = pyqtProperty(QColor,getTrace13Color,setTrace13Color)

    def getTrace13YAxisIndex(self):
        return self.trace13YAxisIndex

    def setTrace13YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace13YAxisIndex].removeItem(self.trace13)
            self._plotIndex[new_axis].addItem(self.trace13)
            self.trace13YAxisIndex = new_axis
            # print(new_axis)

    Trace13YAxisIndex = pyqtProperty(int,getTrace13YAxisIndex,setTrace13YAxisIndex)

    def getTrace13Title(self):
        return str(self.trace13Title)

    def setTrace13Title(self, value):
        if self._traceCount > 13:
            self.legendRemoveItem(self._t13)
            self.trace13Title = str(value)
            self.legend.addItem(self.trace13,self.trace13Title)
            self._t13 = self.legendGetAddedItem()

    def resetTrace13Title(self):
        self.setTrace13Title('Trace 13')

    Trace13Title = pyqtProperty(str, getTrace13Title, setTrace13Title, resetTrace13Title)

    def getTrace14Color(self):
        return self.trace14Color

    def setTrace14Color(self, color):
        if self.trace14Color != color:
            self.trace14Color = color
            self.trace14.setPen(self.trace14Color)

    Trace14Colour = pyqtProperty(QColor,getTrace14Color,setTrace14Color)

    def getTrace14YAxisIndex(self):
        return self.trace14YAxisIndex

    def setTrace14YAxisIndex(self,new_axis):
        if new_axis in [1,2,3]:
            self._plotIndex[self.trace14YAxisIndex].removeItem(self.trace14)
            self._plotIndex[new_axis].addItem(self.trace14)
            self.trace14YAxisIndex = new_axis
            # print(new_axis)

    Trace14YAxisIndex = pyqtProperty(int,getTrace14YAxisIndex,setTrace14YAxisIndex)

    def getTrace14Title(self):
        return str(self.trace14Title)

    def setTrace14Title(self, value):
        if self._traceCount > 14:
            self.legendRemoveItem(self._t14)
            self.trace14Title = str(value)
            self.legend.addItem(self.trace14,self.trace14Title)
            self._t14 = self.legendGetAddedItem()

    def resetTrace14Title(self):
        self.setTrace14Title('Trace 14')

    Trace14Title = pyqtProperty(str, getTrace14Title, setTrace14Title, resetTrace14Title)

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
