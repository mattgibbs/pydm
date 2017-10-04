from pydm.PyQt.QtCore import QObject, pyqtSlot, pyqtSignal
from pydm.widgets.channel import PyDMChannel
from pydm import Display
import numpy as np
from os import path
from pyqtgraph import PlotCurveItem, TextItem

class CorrelationFitter(Display):
    def __init__(self, parent=None, args=None):
        super(CorrelationFitter, self).__init__(parent=parent, args=args)
        
        #add a line to the plot to represent a fit to the data.
        self.fit_line = PlotCurveItem(pen='y')
        #self.ui.waveformPlot.addItem(self.fit_line)
        self.fit_text = TextItem(anchor=(0.5,1))
        #self.ui.waveformPlot.addItem(self.fit_text)
        self.fit_text.setPos(5500.0, 1.0)
        #intercept redraw signal to add a fit to the data.
        self.curve = self.ui.waveformPlot._curves[0]
        #self.curve.data_changed.disconnect()
        #self.curve.data_changed.connect(self.new_curve_data)
        
    def ui_filename(self):
        return 'demo_1.ui'
        
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
    
    @pyqtSlot()
    def new_curve_data(self):
        #Get the waveform data from the curve and fit a parabola to it.
        fit_coefs = np.polyfit(self.curve.x_waveform, self.curve.y_waveform, 2)
        fit_poly = np.poly1d(fit_coefs)
        
        #Update the data for our fit line.
        min_x = np.min(self.curve.x_waveform)
        max_x = np.max(self.curve.x_waveform)
        x_vals = np.linspace(min_x, max_x, len(self.curve.y_waveform))
        fit_data = fit_poly(x_vals)
        self.fit_line.setData(x_vals, fit_data)
        self.fit_text.setText("Peak at: {:.4}".format(fit_poly[1]/(2.0*fit_poly[0])))
        self.fit_text.setPos((min_x+max_x)/2.0, min(self.curve.y_waveform))
        #Now tell the plot to redraw itself
        self.ui.waveformPlot.redrawPlot()
        