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
        self.waveform_rois = []
        self.cursor_list       = []
        self.on_markers,self.off_markers = [],[]




    def initUI(self):
        self.PlotTemporalWidget = PlotWidget(self.maingui.TemporalWidgetContainer)
        self.PlotTemporalWidget.setGeometry(QtCore.QRect(10, 10, 1451, 800))
        self.PlotTemporalWidget.setObjectName("PlotTemporalWidget")
        # self.__add_cursor_button("Add cursor")






    def update(self,arg=None):
        waveforms, self.sc_list = self.workspace.load_AVGs()

        # self.PlotTemporalWidget.clear()
        try:
            for item in self.plotitem:
                self.PlotTemporalWidget.removeItem(item)
            self.PlotTemporalWidget.removeItem(self.envelope_up)
            # self.PlotTemporalWidget.removeItem(self.envelope_do)
        except:pass
        try:
            for item in self.labellist:
                self.PlotTemporalWidget.removeItem(item)
        except:pass
        try:
            for item in self.waveform_rois:
                self.PlotTemporalWidget.removeItem(item)
        except Exception as e:print(e)
        try:
            for item in self.on_markers:
                self.PlotTemporalWidget.removeItem(item)
        except Exception as e:print(e)
        try:
            for item in self.off_markers:
                self.PlotTemporalWidget.removeItem(item)
        except Exception as e:print(e)
        self.plotitem = []
        self.labellist = []
        self.on_markers,self.off_markers = [],[]
        waveforms, scale_factor = self.sig.normalize_waveforms(waveforms)
        # waveforms               = self.sig.order_waveforms(waveforms,self.initSClist)
        self.waveforms       = self.sig.offset_waveforms(waveforms)


        for id, sc in enumerate(self.sc_list):
            if sc=="Stimulus":c='g'
            elif sc[0]=="R ": c='r'
            elif sc[0]=="C ": c='b'
            elif self.maingui.current_sc!=None and self.maingui.current_id==str(id):
                dc = np.mean(self.waveforms[:,id])
                envelope=self.sig.get_envelope(self.waveforms[:,id]-dc)+dc
                # self.deepfilter.get_envelope(waveform-dc)+dc
                self.envelope_up = pg.PlotDataItem(self.const.t*1000,envelope,pen=pg.mkPen('b', width=1))
                # self.envelope_do = pg.PlotDataItem(self.const.t*1000,-((envelope-np.mean(envelope))+np.mean(self.waveforms[:,id])),pen=pg.mkPen('b', width=1))
                self.PlotTemporalWidget.addItem(self.envelope_up)
                # self.PlotTemporalWidget.addItem(self.envelope_do)
                c = 'r'
            else: c='w'
            self.plotitem.append(pg.PlotDataItem(self.const.t*1000,self.waveforms[:,id],pen=pg.mkPen(c, width=1)))
            self.PlotTemporalWidget.addItem(self.plotitem[id])
            label = pg.TextItem(sc, color="r", anchor=(0, 0))
            label.setPos(np.amax(self.const.t*1000),self.waveforms[:,id].mean() )
            self.labellist.append(label)
            # label.setTextWidth(10)
            self.PlotTemporalWidget.addItem(self.labellist[id])
            on, off = self.workspace.get_on_offset(str(id))
            _onmarker  = pg.PlotDataItem([on,on],[np.mean(self.waveforms[:,id]),np.max(self.waveforms[:,id])],pen=pg.mkPen('y', width=2))
            _offmarker = pg.PlotDataItem([off,off],[np.mean(self.waveforms[:,id]),np.max(self.waveforms[:,id])],pen=pg.mkPen('y', width=2))
            self.on_markers.append(_onmarker)
            self.off_markers.append(_offmarker)
            self.PlotTemporalWidget.addItem(self.on_markers[id])
            self.PlotTemporalWidget.addItem(self.off_markers[id])





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
            for item in self.waveform_rois:
                self.PlotTemporalWidget.removeItem(item)
        except:pass
        # self.waveform_rois = {'initROI':pg.RectROI([0,1], [1, 1],pen=QPen(QColor(255, 0, 0,0)))}
        self.waveform_rois=[]
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
            self.waveform_rois.append(_rectroi)
            self.PlotTemporalWidget.addItem(self.waveform_rois[id])
            self.waveform_rois[id].setAcceptedMouseButtons(QtCore.Qt.LeftButton)

            self.waveform_rois[id].sigClicked.connect(self.select_waveform)
            self.waveform_rois[id].sigClicked.connect(self.update)

            # self.waveform_rois[id].sigHoverEvent.connect(self.update_temporal_plot)
            # self.waveform_rois[id].sigHoverEvent.connect(self.select_waveform)

            self.waveform_rois[id].sigRegionChangeFinished.connect(self.move_waveform)
            self.waveform_rois[id].sigRegionChanged.connect(self.move_waveform)
        # del self.waveform_rois['initROI']

    def select_waveform(self,roi):
        x,y = roi.pos()
        w,h = roi.size()
        y   = y + 0.5*h
        for id, sc in enumerate(self.sc_list):
            if y<=np.max(self.waveforms[:,id]) and y>=np.min(self.waveforms[:,id]):
                break
            else: pass
        print("select_waveform:  id:sc", id, sc)
        on, off = self.workspace.get_on_offset(str(id))
        print("select_waveform:  on:", on,"  off", off)

        self.current_sc       = sc
        self.maingui.current_id = str(id)
        self.current_waveform,_ = self.workspace.get_waveform(self.maingui.current_id)
        self.workspace.onset,self.workspace.offset = self.workspace.get_on_offset(self.maingui.current_id)
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


    def __add_cursor_button(self,label):
        _font = QtGui.QFont()
        _font.setPointSize(18)
        _font.setBold(True)
        _font.setWeight(75)
        self.proxy = QtGui.QGraphicsProxyWidget()
        self.deepfilterbutton = QtGui.QPushButton(label)
        # self.deepfilterbutton.setCheckable(True)
        # self.deepfilterbutton.toggle()

        # self.deepfilterbutton.clicked.connect(self.btnstate)
        self.deepfilterbutton.setFont(_font)
        self.proxy.setWidget(self.deepfilterbutton)
        try:
            self.PlotTemporalWidget.addItem(self.proxy,row=1,col=0)
        except:pass


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
        self.PlotTemporalWidget.addItem(cursor)

        cursorbutton = pg.RectROI(pos=[cursor.value(),1.5], size=[2.5, 0.5],centered=True,
                          movable=False, resizable=False, removable=True,
                          pen=pg.mkPen((255, 255, 0,0)),
                          hoverPen=pg.mkPen((255, 0, 0,255), width=10))

        cursorbutton.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        cursorbutton.sigClicked.connect(self.delete_cursor)
        self.PlotTemporalWidget.addItem(cursorbutton)
        self.cursor_list.append([cursor,cursorbutton])



    def __cursor_moved(self,cursor):
        cursor.label.setText("{:.1f}".format(cursor.value()))
        _tmp = np.array(self.cursor_list)
        idx = np.where(_tmp[:,0] == cursor)[0][0]
        cursorbutton = self.cursor_list[idx][1]
        cursorbutton.setPos(pos=(cursor.value(),1))


    def delete_cursor(self,cursorbutton):
        print(self.cursor_list)
        _tmp = np.array(self.cursor_list)
        idx = np.where(_tmp[:,1] == cursorbutton)[0][0]
        print(idx)
        cursorbutton = self.cursor_list[idx][1]
        cursor = self.cursor_list[idx][0]
        del self.cursor_list[idx]
        self.PlotTemporalWidget.removeItem(cursor)
        self.PlotTemporalWidget.removeItem(cursorbutton)





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
