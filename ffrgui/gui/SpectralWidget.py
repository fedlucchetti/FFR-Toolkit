

import sys, copy
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon, QColor, QPen, QMouseEvent, QFont
from PyQt5.QtCore import pyqtSlot,QRectF
from PyQt5 import QtCore



from pyqtgraph.Qt import QtGui

import numpy as np
import pyqtgraph as pg


font=QtGui.QFont()
font.setPixelSize(30)

class SpectralWidget():

    def __init__(self,maingui):
        super().__init__()
        self.maingui = maingui
        self.sig = maingui.sig
        self.ffrutils = maingui.ffrutils
        self.const = maingui.const
        self.workspace = maingui.workspace
        self.plot_style = pg.mkPen((255, 100, 0,255) ,width=2)




    def initUI(self,flag='new'):
        try:
            if self.win:self.win.clear()
        except: pass
        self.win = pg.GraphicsLayoutWidget(show=True, title=self.maingui.current_sc)
        self.win.resize(1000,600)
        self.spectral = self.win.addPlot(title='')

        self.spectral.setXRange(0,4000)

        try:
            self.ymax=self.workspace.current_workspace[self.maingui.current_id]["Data"]["original"]["gui"]["ymax"]
        except:self.ymax=0
        self.update_plot()
        self.roifilters=[]
        if flag=='load':
            self.__load_roi_from_workspace()
        try:
            self.add_iirfilter_button()
            self.add_deepfilter_button('Apply DeepFilter')
        except Exception as e:
            print('SpectralWidget initUI:', e)
            raise
        # self.win.show()

    def add_iirfilter_button(self):
        _font = QtGui.QFont()
        _font.setPointSize(18)
        _font.setBold(True)
        _font.setWeight(75)
        proxy = QtGui.QGraphicsProxyWidget()
        button = QtGui.QPushButton('Add IIR Filter')
        button.clicked.connect(lambda: self.__add_iirfilter())
        button.setFont(_font)
        proxy.setWidget(button)
        self.win.addItem(proxy,row=1,col=0)

    def add_deepfilter_button(self,label):
        _font = QtGui.QFont()
        _font.setPointSize(18)
        _font.setBold(True)
        _font.setWeight(75)
        self.proxy = QtGui.QGraphicsProxyWidget()
        self.deepfilterbutton = QtGui.QPushButton(label)
        self.deepfilterbutton.setCheckable(True)
        # self.deepfilterbutton.toggle()

        self.deepfilterbutton.clicked.connect(self.btnstate)
        self.deepfilterbutton.setFont(_font)
        self.proxy.setWidget(self.deepfilterbutton)
        try:
            self.win.addItem(self.proxy,row=2,col=0)
        except:pass
            # raise

    def btnstate(self):
        print('btnstate: ',self.deepfilterbutton.isChecked())
        if self.deepfilterbutton.isChecked():
            self.__add_deepfilter()
        else:
            self.__remove_deepfilter()


    def update_plot(self):

        if self.maingui.current_json != None:
            try:
                self.spectral.removeItem(self.cursor)
                self.spectral.removeItem(self.signal_spectra)
                self.spectral.removeItem(self.noise_spectra)
                self.spectral.removeItem(self.proxy)
            except:pass

            # try:
            #     for item in self.roifilters:
            #         self.specopyctral.removeItem(item)
            # except:pass
            # try:
            #     self.__load_roi_from_workspace()
            # except:pass
            self.__add_cursor()
            if len(self.workspace.get_filters())>0:flag='filtered'
            else:flag='original'

            sig_waveform, noise_waveform      = self.workspace.get_sc_spectral(flag)
            self.sig_waveform,signal_f        = self.ffrutils.smooth_plot(self.const.f,sig_waveform,window=91)
            self.noise_waveform,noise_f       = self.ffrutils.smooth_plot(self.const.f,noise_waveform,window=91)


            self.signal_spectra = pg.PlotDataItem(signal_f,self.sig_waveform,pen=self.plot_style)
            self.spectral.showGrid(x=True, y=True)
            self.spectral.setLabel('left', "FFT Amplitude [nV]")
            self.spectral.setLabel('bottom', "Frequency [Hz]",fontsize=20)

            font=QtGui.QFont()
            font.setPixelSize(100)
            self.spectral.getAxis("left").tickFont = font
            # self.spectral.getAxis("left").setStyle(tickTextOffset = 20)
            self.spectral.getAxis("bottom").tickFont = font
            # self.spectral.getAxis("bottom").setStyle(tickTextOffset = 20)

            self.spectral.setLimits(xMin=0,yMin=0,yMax=self.ymax*1.1)

            self.__addItem(self.signal_spectra)
            self.noise_spectra = pg.PlotDataItem(noise_f,self.noise_waveform,fillLevel=0,brush=(255,0,0,80),fillOutline=False, width=0)
            self.__addItem(self.noise_spectra)
            self.spectral.update()



            # self.add_filter()

    def __add_cursor(self):
        try:
            if self.cursor_xpos:pass
            else:self.cursor_xpos=500
        except:self.cursor_xpos=500
        self.cursor = pg.InfiniteLine(pos=self.cursor_xpos,pen=pg.mkPen('y', width=4),\
                                markers = '<|>',label=str(self.cursor_xpos) )
        self.cursor.setMovable(True)
        self.cursor.setBounds([0,self.const.fs])
        self.cursor.label.setMovable(True)
        self.cursor.label.setMovable(True)
        self.cursor.label.setY(0)
        self.cursor.label.setColor(pg.mkColor((255, 200, 0,150)))
        self.cursor.label.setFont(QFont("Times", 20, QFont.Bold))
        self.cursor.sigDragged.connect(self.__cursor_moved)
        self.spectral.addItem(self.cursor)


    def __cursor_moved(self,cursor):
        self.cursor_xpos=self.cursor.value()
        self.cursor.label.setText("{:.0f}".format(self.cursor_xpos))

    def __addItem(self,item):
        self.spectral.addItem(item)


    def __clear_plot(self):
        pass

    def __construct_roi_filter(self,flag):
        hovercolor = pg.mkPen((255, 255, 0,255) ,width=4)
        if flag=='new':
            _roi = pg.RectROI(pos=[np.random.randint(0,4000),0], size=[500, self.ymax],centered=True, \
                       movable=True, resizable=True, removable=True, maxBounds=QRectF(0,0,int(self.const.fs/2),self.ymax) ,\
                       pen=pg.mkPen((255, 0, 0,100), width=4),hoverPen=hovercolor,handlePen=pg.mkPen((255, 0, 0,100), width=4))
            type='stop'
            self.__action(_roi)
            return _roi, type

        elif flag=='load':
            copydict=copy.deepcopy(self.workspace.current_workspace[self.maingui.current_id]["Filters"])
            for key in copydict.keys():
                if key==-1: continue
                value=copydict[key]
                # print('__construct_roi_filter', key, value)
                type=value['type']
                if   type=='stop': color=pg.mkPen((255, 0, 0,100), width=4)
                elif type=='pass': color=pg.mkPen((0, 255, 0,100), width=4)
                elif key =='42':
                    if value['enable']==1:
                        self.add_deepfilter_button('Disable DeepFilter')
                        # self.deepfilterbutton.setText('Disable DeepFilter')
                        self.plot_style = pg.mkPen((0, 100, 220,255) ,width=2)
                    elif value['enable']==0:
                        self.add_deepfilter_button('Apply DeepFilter')
                        # self.deepfilterbutton.setText('Apply DeepFilter')
                        self.plot_style = pg.mkPen((255, 100, 0,255) ,width=2)
                    continue


                x,y = value['state']['pos']
                wx,wy = value['state']['size'][0], value['state']['size'][1]
                _roi = pg.RectROI(pos=(x,y), size=(wx,wy, self.ymax),centered=True, \
                           movable=True, resizable=True, removable=True, maxBounds=QRectF(0,0,int(self.const.fs/2),self.ymax) ,\
                           pen=color,hoverPen=hovercolor,handlePen=color)

                del self.workspace.current_workspace[self.maingui.current_id]["Filters"][key]
                new = {str(_roi):{'state':_roi.saveState(),'type':type}}
                self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)
                self.__action(_roi)




    def __action(self,roi):
        roi.addScaleHandle(pos=[0,0.5],center=[0.5,0.5])
        roi.addScaleHandle(pos=[1,0.5],center=[0.5,0.5])
        roi.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        # _roi.setAcceptedMouseButtons(QtCore.Qt.RightButton)

        roi.sigClicked.connect(self.__switch_filter_type)
        roi.sigClicked.connect(self.__apply_filter)

        roi.sigRegionChanged.connect(self.__update_roi_filter)
        roi.sigRegionChanged.connect(self.__apply_filter)
        roi.sigRemoveRequested.connect(self.__remove_roi_filter)

        # _roi.sigClicked.connect(self.mouseRightClickEvent)

        self.roifilters.append(roi)
        self.__addItem(roi)

    def __apply_filter(self):
        self.sig.filter_current_waveform()
        self.update_plot()
        self.__list_all()
        self.maingui.update_temporal_plot()

    def __add_iirfilter(self):
        roi, type = self.__construct_roi_filter('new')
        new = {str(roi):{'state':roi.saveState(),'type':type}}
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)
        # self.__list_all()
        try:
            if -1 in self.workspace.current_workspace[self.maingui.current_id]["Filters"]:
                del self.workspace.current_workspace[self.maingui.current_id]["Filters"][-1]
        except: pass

    def __add_deepfilter(self):
        # roi, type = self.__construct_roi_filter('new')
        print('checked')
        new = {'42':{'state':{'pos':(0.0,0.0),'size':(0.0,0.0),'angle':(0.0)},'type':'autoencoder','enable':1}}
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)
        self.plot_style = pg.mkPen((0, 80, 220,255) ,width=2)
        self.update_plot()
        self.deepfilterbutton.setText('Disable DeepFilter')
        self.__apply_filter()

    def __remove_deepfilter(self):
        print('unchecked')
        new = {'42':{'state':{'pos':(0.0,0.0),'size':(0.0,0.0),'angle':(0.0)},'type':'autoencoder','enable':0}}
        self.deepfilterbutton.setText('Apply DeepFilter')
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)
        self.plot_style = pg.mkPen((255, 100, 0,255) ,width=2)
        self.__apply_filter()
        self.update_plot()


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
        n = len(self.maingui.workspace.get_filters())
        new = {str(roi):{'state':roi.saveState(),'type':type}}
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)

    def __update_roi_filter(self,roi):
        type = self.workspace.current_workspace[self.maingui.current_id]["Filters"][str(roi)]['type']
        new = {str(roi):{'state':roi.saveState(),'type':type}}
        self.workspace.current_workspace[self.maingui.current_id]["Filters"].update(new)

    def __list_all(self):
        rois=self.workspace.current_workspace[self.maingui.current_id]["Filters"]
        for id,roi in enumerate(rois):
            # print('filter # ',id, str(roi), rois[str(roi)])
            pass
    def __count_filters(self):
        return len(self.workspace.current_workspace[self.maingui.current_id]["Filters"])

    def __remove_roi_filter(self,roi):
        del self.workspace.current_workspace[self.maingui.current_id]["Filters"][str(roi)]
        self.spectral.removeItem(roi)
        self.update_plot()


    def __load_roi_from_workspace(self):
        self.__construct_roi_filter('load')








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
