

import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon, QColor, QPen, QMouseEvent
from PyQt5.QtCore import pyqtSlot,QRectF
from PyQt5 import QtCore


from pyqtgraph.Qt import QtGui
# from PyQt5.QtGui import QColor, QPen, QMouseEvent

import numpy as np
import pyqtgraph as pg


win = pg.GraphicsLayoutWidget(show=True, title="FFR Spectral Analysis")
spectral = win.addPlot(title='draft')


x = np.random.randint(0,10,10)
y = np.random.randint(0,10,10)


signal_spectra = pg.PlotDataItem(x,y,pen=pg.mkPen('r', width=2))
spectral.addItem(signal_spectra)
