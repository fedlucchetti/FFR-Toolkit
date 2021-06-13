

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import GraphicsScene, PlotWidget

import numpy as np
import pyqtgraph as pg







class SpectralWidget(object):

    def __init__(self,ffr,Form):
        super().__init__()
        self.Form = Form
        # self.initUI()

    def initUI(self):
        self.Form.setObjectName("Form")
        self.Form.resize(1411, 683)
        # self.PlotSpectralWidget = GraphicsScene(self)
        self.PlotSpectralWidget = PlotWidget(self.Form)
        self.PlotSpectralWidget.setGeometry(QtCore.QRect(130, 50, 1181, 591))
        self.PlotSpectralWidget.setObjectName("PlotSpectralWidget")
        self.add_spectrum()
        self.add_filter()
        self.retranslateUi(self.Form)
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    def add_spectrum(self):
        x2 = np.linspace(-100, 100, 1000)
        data2 = np.sin(x2) / x2
        plotitem = pg.PlotDataItem(x2,data2)
        self.PlotSpectralWidget.addItem(plotitem)

    def clear_plot(self):
        pass

    def add_filter(self):
        self.lr = pg.LinearRegionItem([400,700])
        # self.lr.sigRegionChanged()
        self.lr.setZValue(-10)
        self.PlotSpectralWidget.addItem(self.lr)
        pass

    def delete_filter():
        pass

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.Form.setWindowTitle(_translate("Form", "Form"))

    def test_print(self):
        print("yes")

    # def showPlot(self):
    #     self.win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
    #     self.win.resize(1000,600)
    #     self.win.setWindowTitle('pyqtgraph example: Plotting')
    #     x2 = np.linspace(-100, 100, 1000)
    #     data2 = np.sin(x2) / x2
    #     self.spectral.plot(data2, pen=(255,255,255,200))

        # lr = pg.LinearRegionItem([400,700])
        # lr.setZValue(-10)
        # self.spectral.addItem(lr)
        # lr.clicked.connect(self.on_click)





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = SpectralWidget(None)
    ex.initUI()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()
