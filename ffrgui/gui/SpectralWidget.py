

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon, QColor, QPen, QMouseEvent
from PyQt5.QtCore import pyqtSlot,QRectF
from PyQt5 import QtCore


from pyqtgraph.Qt import QtGui
# from PyQt5.QtGui import QColor, QPen, QMouseEvent

import numpy as np
import pyqtgraph as pg


class SpectralWidget():

    def __init__(self,maingui):
        super().__init__()
        self.maingui = maingui
        self.sig = maingui.sig
        self.ffrjson = maingui.ffr
        # self.win = pg.GraphicsLayoutWidget(show=False, title="FFR Spectral Analysis")
        # self.win.resize(1000,600)

        self.filter_list={-1:{"type":None,"state":None}}
        #
        # self.initUI()

    def __addItem(self,item):
        self.spectral.addItem(item)

    def initUI(self):
        try:
            if win:self.win.clear()
        except: pass
        self.win = pg.GraphicsLayoutWidget(show=True, title="FFR Spectral Analysis")
        self.win.resize(1000,600)
        self.spectral = self.win.addPlot(title=self.maingui.current_sc)
        if self.maingui.current_json != None:
            self.add_spectrum()
        self.spectral.setXRange(0,4000)
        self.__add_clickable_background()
        # self.win.show()

    def __add_clickable_background(self):
        roi = pg.RectROI(pos=[0,0], size=[self.ffrjson.fs/2, 10e12],centered=True, \
                   movable=False, resizable=False, removable=True ,\
                   pen=pg.mkPen((255, 0, 0,0)),hoverPen=pg.mkPen((0, 255, 0,0)),handlePen=pg.mkPen((0, 255, 0,0)))
        roi.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        roi.sigClicked.connect(self.__add_filter)
        self.__addItem(roi)

    def test_print(self):
        print("yes")

    def add_spectrum(self):
        sig_waveform, noise_waveform      = self.sig.get_sc_spectral()
        self.sig_waveform,signal_f        = self.ffrjson.smooth_plot(self.ffrjson.f,sig_waveform,window=91)
        self.noise_waveform,noise_f       = self.ffrjson.smooth_plot(self.ffrjson.f,noise_waveform,window=91)

        signal_spectra = pg.PlotDataItem(signal_f,self.sig_waveform,pen=pg.mkPen('r', width=2))
        self.spectral.setLimits(xMin=0,yMin=0,yMax=self.sig_waveform.max())


        self.__addItem(signal_spectra)
        noise_spectra = pg.PlotDataItem(noise_f,self.noise_waveform,fillLevel=0,brush=(255,0,0,80),fillOutline=False, width=0)
        self.__addItem(noise_spectra)
        # self.add_filter()
        self.__add_clickable_background()

    def __clear_plot(self):
        pass

    def __switch_filter_type(self,roi):
        color = roi.pen.color().getRgb()
        if color[0]==255:
            roi.pen       = pg.mkPen((0, 255, 0,100), width=4)
            roi.hoverPen  = pg.mkPen((0, 255, 0,100), width=4)
            roi.handlePen = pg.mkPen((0, 255, 0,100), width=4)
            print("set to bandpass")
        elif color[1]==255:
            roi.pen       = pg.mkPen((255, 0, 0,100), width=4)
            roi.hoverPen  = pg.mkPen((255, 0, 0,100), width=4)
            roi.handlePen = pg.mkPen((255, 0, 0,100), width=4)
            print("set to bandstop")
        self.filter_list.update({roi:roi})

    def __update_roi_filter(self,roi):
        self.filter_list.update({roi:roi})

    def __remove_roi_filter(self,roi):
        roi.deleteLater()

    def __construct_roi_filter(self):
        _filter = pg.RectROI(pos=[np.random.randint(0,4000),0], size=[500, self.sig_waveform.max()],centered=True, \
                   movable=True, resizable=True, removable=True, maxBounds=QRectF(0,0,int(self.ffrjson.fs/2),self.sig_waveform.max()) ,\
                   pen=pg.mkPen((255, 0, 0,100), width=4),hoverPen=pg.mkPen((255, 0, 0,50), width=4),handlePen=pg.mkPen((255, 0, 0,100), width=4))
        _filter.addScaleHandle(pos=[0,0.5],center=[0.5,0.5])
        _filter.addScaleHandle(pos=[1,0.5],center=[0.5,0.5])
        _filter.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        _filter.sigClicked.connect(self.__switch_filter_type)

        _filter.sigRegionChangeFinished.connect(self.__update_roi_filter)
        _filter.sigRegionChanged.connect(self.__update_roi_filter)

        _filter.sigRemoveRequested.connect(self.__remove_roi_filter)
        # _filter.saveState()
        self.__addItem(_filter)

    def __add_filter(self):
        _filter = self.__construct_roi_filter()
        if _filter in self.filter_list:
            self.filter_list[_filter]=_filter
        else:
            self.filter_list.update({_filter:_filter})
        print("_add filter: number of fitlers",len(self.filter_list))
        if -1 in self.filter_list:
            del self.filter_list[-1]




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = SpectralWidget()
    ex.initUI()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()
