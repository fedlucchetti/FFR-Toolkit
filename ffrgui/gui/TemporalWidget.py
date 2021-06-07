import sys, copy
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor, QPen, QMouseEvent, QFont


from pyqtgraph import PlotWidget
from pyqtgraph.Qt import QtGui

import pyqtgraph as pg



font=QtGui.QFont()
font.setPixelSize(30)

class TemporalWidget():

    def __init__(self,maingui):
        super().__init__()
        self.maingui = maingui
        self.sig = maingui.sig
        self.const = maingui.const
        self.workspace = maingui.workspace
        self.plot_style = pg.mkPen((255, 100, 0,255) ,width=2)




    def initUI(self):
        self.PlotTemporalWidget = PlotWidget(self.maingui.TemporalWidgetContainer)
        self.PlotTemporalWidget.setGeometry(QtCore.QRect(10, 10, 1451, 800))
        self.PlotTemporalWidget.setObjectName("PlotTemporalWidget")

    def update(self,arg=None):
        waveforms, self.sc_list = self.workspace.load_AVGs()

        # self.PlotTemporalWidget.clear()
        try:
            for item in self.plotitem:
                self.PlotTemporalWidget.removeItem(item)
        except:pass
        try:
            for item in self.labellist:
                self.PlotTemporalWidget.removeItem(item)
        except:pass
        try:
            for item in self.roisdict:
                self.PlotTemporalWidget.removeItem(item)
        except Exception as e:print(e)
        self.plotitem = []
        self.labellist = []
        waveforms, scale_factor = self.sig.normalize_waveforms(waveforms)
        # waveforms               = self.sig.order_waveforms(waveforms,self.initSClist)
        self.waveforms       = self.sig.offset_waveforms(waveforms)


        for id, sc in enumerate(self.sc_list):
            if sc=="Stimulus":c='g'
            elif sc[0]=="R ": c='r'
            elif sc[0]=="C ": c='b'
            elif self.maingui.current_sc!=None and self.maingui.current_id==id: c = 'r'
            else: c='w'
            self.plotitem.append(pg.PlotDataItem(self.const.t*1000,self.waveforms[:,id],pen=pg.mkPen(c, width=1)))
            self.PlotTemporalWidget.addItem(self.plotitem[id])
            label = pg.TextItem(sc, color="r", anchor=(0, 0))
            label.setPos(np.amax(self.const.t*1000),self.waveforms[:,id].mean() )
            self.labellist.append(label)
            # label.setTextWidth(10)
            self.PlotTemporalWidget.addItem(self.labellist[id])


        self.PlotTemporalWidget.setLimits(xMin=0,yMin=self.waveforms[:,-1].min(),yMax=2,xMax=1.1*self.const.t.max()*1000)
        self.PlotTemporalWidget.setXRange(0, 1.1*self.const.t.max()*1000, padding=0)
        self.PlotTemporalWidget.setYRange(self.waveforms[:,-1].min(), 2, padding=0)

        self.PlotTemporalWidget.showGrid(x=True, y=False,alpha=1)
        self.PlotTemporalWidget.setLabel('left', "Amplitude",fontsize=100,color='white')
        self.PlotTemporalWidget.setLabel('bottom', "Time [ms]",fontsize=100,color='white')

        self.update_rois()
        self.__add_clickable_background()


    def update_rois(self):
        try:
            for item in self.roisdict:
                self.PlotTemporalWidget.removeItem(item)
        except:pass
        # self.roisdict = {'initROI':pg.RectROI([0,1], [1, 1],pen=QPen(QColor(255, 0, 0,0)))}
        self.roisdict=[]
        roi_width = 10*1000
        # for id,sc in self.waveforms.keys():
        for id, sc in enumerate(self.sc_list):
            roi_y_pos  = np.min(self.waveforms[:,id])
            roi_height = np.abs(np.max(self.waveforms[:,id])-np.min(self.waveforms[:,id]))
            _rectroi   = pg.RectROI(pos=[np.max(self.const.t*1000),roi_y_pos], size=[roi_width, roi_height], \
                       movable=True, resizable=False, removable=True, \
                       maxBounds=QRectF(0,20*roi_y_pos,roi_width,20*roi_height) ,\
                       pen=pg.mkPen((255, 0, 0,255), width=2),\
                       hoverPen=pg.mkPen((0, 255, 0,255), width=2),\
                       handlePen=pg.mkPen((255, 0, 0,255), width=2))

            # _roi       = {id:_rectroi}
            self.roisdict.append(_rectroi)
            self.PlotTemporalWidget.addItem(self.roisdict[id])
            self.roisdict[id].setAcceptedMouseButtons(QtCore.Qt.LeftButton)

            self.roisdict[id].sigClicked.connect(self.select_waveform)
            self.roisdict[id].sigClicked.connect(self.update)

            # self.roisdict[id].sigHoverEvent.connect(self.update_temporal_plot)
            # self.roisdict[id].sigHoverEvent.connect(self.select_waveform)

            self.roisdict[id].sigRegionChangeFinished.connect(self.move_waveform)
            self.roisdict[id].sigRegionChanged.connect(self.move_waveform)
        # del self.roisdict['initROI']

    def select_waveform(self,roi):
        x,y = roi.pos()
        w,h = roi.size()
        y   = y + 0.5*h
        for id, sc in enumerate(self.sc_list):
            if y<=np.max(self.waveforms[:,id]) and y>=np.min(self.waveforms[:,id]):
                break
            else: pass
        print("select_waveform:  id:sc", id, sc)
        self.current_sc       = sc
        self.maingui.current_id       = id
        self.current_waveform,_ = self.workspace.get_waveform(id)
        return sc


    def move_waveform(self,roi):
        pass


    def __add_clickable_background(self):
        roi = pg.RectROI(pos=[0,0], size=[max(self.const.t)*1000, 20],centered=True, \
                   movable=False, resizable=False, removable=True ,\
                   pen=pg.mkPen((255, 0, 0,0)),hoverPen=pg.mkPen((0, 255, 0,0)),handlePen=pg.mkPen((0, 255, 0,0)))
        roi.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        roi.sigClicked.connect(self.__add_cursor)
        self.PlotTemporalWidget.addItem(roi)


    def __add_cursor(self):
        xpos=np.random.randint(0,max(self.const.t)*1000)
        cursor = pg.InfiniteLine(pos=xpos,pen=pg.mkPen('y', width=4),\
                                markers = '<|>',label=str(xpos) )
        cursor.setMovable(True)
        cursor.setBounds([0,max(self.const.t)*1000])
        cursor.label.setMovable(True)
        cursor.label.setY(1.5)
        cursor.label.setColor(pg.mkColor((255, 200, 0,255)))
        cursor.label.setFont(QFont("Times", 20, QFont.Bold))
        cursor.sigDragged.connect(self.__cursor_moved)
        # cursor.sigClicked.connect(self.test_print)
        self.PlotTemporalWidget.addItem(cursor)

        cursorbutton = pg.RectROI(pos=[cursor.value(),1], size=[2.5, 0.5],centered=True,
                          movable=True, resizable=True, removable=True,
                          pen=pg.mkPen((255, 0, 0,100), width=4),
                          hoverPen=pg.mkPen((255, 255, 0,100), width=4),
                          handlePen=pg.mkPen((255, 0, 0,100), width=4))
        cursorbutton.sigClicked.connect(self.test_print)
        self.PlotTemporalWidget.addItem(cursorbutton)



    def __remove_cursor(self):
        self.PlotTemporalWidget.removeItem(roi)

    # def __add_target_label(self,cursor):
    #     label = pg.TargetItem(pos=(cursor.value(),0),size=20,label=str(cursor.value()))

    def __cursor_moved(self,cursor):
        cursor.label.setText("{:.1f}".format(cursor.value()))

    def test_print(self):
        print('test_print')


    def update_tf_plot(self):
        print('latency clicked')
        self.PlotTemporalWidget.clear()
        plotitem     = pg.PlotDataItem(self.const.t*1000,self.maingui.current_waveform/np.max(self.maingui.current_waveform),pen=pg.mkPen('g', width=1))
        self.PlotTemporalWidget.addItem(plotitem)

        analytic_signal   = signal.hilbert(self.maingui.current_waveform)
        self.IAmplitude   = np.abs(analytic_signal)
        self.IAmplitude   = self.IAmplitude/np.max(self.IAmplitude)-2
        plotitem     = pg.PlotDataItem(self.const.t*1000,self.IAmplitude,pen=pg.mkPen('r', width=1))
        self.PlotTemporalWidget.addItem(plotitem)

        self.IPhase       = np.unwrap(np.angle(analytic_signal))
        self.DeltaPhase   = np.abs(self.IPhase - 2*np.pi*self.database.get_frequency(self.maingui.current_sc)*self.const.t)
        self.DeltaPhase   = self.DeltaPhase/np.max(self.DeltaPhase)-4
        plotitem     = pg.PlotDataItem(self.const.t*1000,self.DeltaPhase ,pen=pg.mkPen('b', width=1))
        self.PlotTemporalWidget.addItem(plotitem)







if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = TemporalWidget()
    ex.initUI()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()