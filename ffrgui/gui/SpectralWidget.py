

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
        self.ffrutils = maingui.ffrutils
        self.workspace = maingui.workspace
        # self.win = pg.GraphicsLayoutWidget(show=False, title="FFR Spectral Analysis")
        # self.win.resize(1000,600)

        #
        # self.initUI()

    def __addItem(self,item):
        self.spectral.addItem(item)

    def initUI(self,arg=None):
        try:
            if self.win:self.win.clear()
        except: pass
        self.win = pg.GraphicsLayoutWidget(show=True, title="FFR Spectral Analysis")
        self.win.resize(1000,600)
        self.spectral = self.win.addPlot(title=self.maingui.current_sc)

        self.spectral.setXRange(0,4000)
        self.ymax=[]
        self.__add_clickable_background()
        self.update_plot()

        self.__add_clickable_background()
        try:
            if arg=='load':
                if -1 not in self.workspace.current_workspace[self.maingui.current_id]["Filters"]:
                    self.__load_roi_from_workspace()
        except:pass
        # self.win.show()

    def update_plot(self):
        if self.maingui.current_json != None:
            try:
                # print("Remove items")
                self.spectral.removeItem(self.signal_spectra)
                self.spectral.removeItem(self.noise_spectra)
            except:pass
            if len(self.workspace.get_filters())>0:flag='filtered'
            else:flag='original'
            sig_waveform, noise_waveform      = self.workspace.get_sc_spectral(flag)
            self.sig_waveform,signal_f        = self.ffrutils.smooth_plot(self.ffrutils.f,sig_waveform,window=91)
            self.noise_waveform,noise_f       = self.ffrutils.smooth_plot(self.ffrutils.f,noise_waveform,window=91)

            self.signal_spectra = pg.PlotDataItem(signal_f,self.sig_waveform,pen=pg.mkPen('r', width=2))

            if len(self.ymax)==0:self.ymax.append(self.sig_waveform.max())
            self.spectral.setLimits(xMin=0,yMin=0,yMax=self.ymax[0])

            print("Update items")
            self.__addItem(self.signal_spectra)
            self.noise_spectra = pg.PlotDataItem(noise_f,self.noise_waveform,fillLevel=0,brush=(255,0,0,80),fillOutline=False, width=0)
            self.__addItem(self.noise_spectra)
            self.spectral.update()
            # self.add_filter()


    def __add_clickable_background(self):
        roi = pg.RectROI(pos=[0,0], size=[self.ffrutils.fs/2, 10e12],centered=True, \
                   movable=False, resizable=False, removable=True ,\
                   pen=pg.mkPen((255, 0, 0,0)),hoverPen=pg.mkPen((0, 255, 0,0)),handlePen=pg.mkPen((0, 255, 0,0)))
        roi.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        roi.sigClicked.connect(self.__add_filter)
        self.__addItem(roi)

    def test_print(self):
        print("yes")

    def __clear_plot(self):
        pass

    def __construct_roi_filter(self,roi=None):
        if roi==None:
            _filter = pg.RectROI(pos=[np.random.randint(0,4000),0], size=[500, self.sig_waveform.max()],centered=True, \
                       movable=True, resizable=True, removable=True, maxBounds=QRectF(0,0,int(self.ffrutils.fs/2),self.sig_waveform.max()) ,\
                       pen=pg.mkPen((255, 0, 0,100), width=4),hoverPen=pg.mkPen((255, 0, 0,100), width=4),handlePen=pg.mkPen((255, 0, 0,100), width=4))
            type='stop'
        else:
            type=roi['type']
            if   type=='stop': color=pg.mkPen((255, 0, 0,100), width=4)
            elif type=='pass': color=pg.mkPen((0, 255, 0,100), width=4)
            _filter = pg.RectROI(pos=roi['state']['pos'], size=roi['state']['size'],centered=True, \
                       movable=True, resizable=True, removable=True, maxBounds=QRectF(0,0,int(self.ffrutils.fs/2),self.sig_waveform.max()) ,\
                       pen=color,hoverPen=color,handlePen=color)

        _filter.addScaleHandle(pos=[0,0.5],center=[0.5,0.5])
        _filter.addScaleHandle(pos=[1,0.5],center=[0.5,0.5])
        _filter.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        _filter.sigClicked.connect(self.__switch_filter_type)
        _filter.sigClicked.connect(self.__apply_filter)

        _filter.sigRegionChanged.connect(self.__update_roi_filter)
        _filter.sigRegionChanged.connect(self.__apply_filter)
        _filter.sigRemoveRequested.connect(self.__remove_roi_filter)
        self.__addItem(_filter)
        return _filter, type

    def __apply_filter(self):
        self.sig.filter_current_waveform()
        self.update_plot()
        self.__list_all()
        self.maingui.update_temporal_plot()

    def __add_filter(self):
        roi, type = self.__construct_roi_filter()
        new = {roi:{'state':roi.saveState(),'type':type}}
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)
        # self.__list_all()
        if -1 in self.workspace.current_workspace[self.maingui.current_id]["Filters"]:
            del self.workspace.current_workspace[self.maingui.current_id]["Filters"][-1]

    def __switch_filter_type(self,roi):
        color = roi.pen.color().getRgb()
        if color[0]==255:
            roi.pen       = pg.mkPen((0, 255, 0,100), width=4)
            roi.hoverPen  = pg.mkPen((0, 255, 0,100), width=4)
            roi.handlePen = pg.mkPen((0, 255, 0,100), width=4)
            type='pass'
        elif color[1]==255:
            roi.pen       = pg.mkPen((255, 0, 0,100), width=4)
            roi.hoverPen  = pg.mkPen((255, 0, 0,100), width=4)
            roi.handlePen = pg.mkPen((255, 0, 0,100), width=4)
            type='stop'
        new = {roi:{'state':roi.saveState(),'type':type}}
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)
        # self.__update_roi_filter(roi,type)

    def __update_roi_filter(self,roi):
        type = self.workspace.current_workspace[self.maingui.current_id]["Filters"][roi]['type']
        new = {roi:{'state':roi.saveState(),'type':type}}
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)

    def __list_all(self):
        rois=self.workspace.current_workspace[self.maingui.current_id]["Filters"]
        for id in rois:
            print(rois[id])

    def __count_filters(self):
        return len(self.workspace.current_workspace[self.maingui.current_id]["Filters"])

    def __remove_roi_filter(self,roi):
        self.spectral.removeItem(roi)
        del self.workspace.current_workspace[self.maingui.current_id]["Filters"][roi]

    def __load_roi_from_workspace(self):
        rois=self.workspace.current_workspace[self.maingui.current_id]["Filters"]
        for id in rois:
            self.__construct_roi_filter(rois[id])
        # roi.deleteLater()




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
