

import sys, copy
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon, QColor, QPen, QMouseEvent, QFont
from PyQt5.QtCore import pyqtSlot,QRectF
from PyQt5 import QtCore



from pyqtgraph.Qt import QtGui

import numpy as np
import pyqtgraph as pg
import matplotlib

font=QtGui.QFont()
font.setPixelSize(30)

class LatencyPlotWidget():

    def __init__(self,maingui):
        super().__init__()
        self.maingui   = maingui
        self.sig       = maingui.sig
        self.const     = maingui.const
        self.workspace = maingui.workspace
        self.TMAX            = 1000*max(self.const.t)

    def initUI(self,flag='new'):
        try:
            if self.win:self.win.clear()
        except: pass
        self.win = pg.GraphicsLayoutWidget(show=True, title=self.maingui.current_sc)
        self.win.resize(1400,800)
        self.latencyPlot = self.win.addPlot(title='')
        # self.latencyPlot.setXRange(0,self.TMAX)
        # self.latencyPlot.setXRange(-1.3,1.3)
        self.createPlot()
        try:
            self.save_button()
            self.add_phaseshift_button()
            self.exit_button()
        except Exception as e:
            print('latencyPlotWidget initUI:', e)


    def save_button(self):
        _font = QtGui.QFont()
        _font.setPointSize(18)
        _font.setBold(True)
        _font.setWeight(75)
        proxy = QtGui.QGraphicsProxyWidget()
        button = QtGui.QPushButton('Save')
        button.clicked.connect(lambda: self.workspace.set_on_offset())
        button.setFont(_font)
        proxy.setWidget(button)
        self.win.addItem(proxy,row=1,col=0)

    def add_phaseshift_button(self):
        _font = QtGui.QFont()
        _font.setPointSize(18)
        _font.setBold(True)
        _font.setWeight(75)
        proxy = QtGui.QGraphicsProxyWidget()
        button = QtGui.QPushButton('Add phase shift')
        button.clicked.connect(lambda: self.__add_on_offset_cursors("phaseshift"))
        button.setFont(_font)
        proxy.setWidget(button)
        self.win.addItem(proxy,row=2,col=0)

    def exit_button(self):
        _font = QtGui.QFont()
        _font.setPointSize(18)
        _font.setBold(True)
        _font.setWeight(75)
        proxy = QtGui.QGraphicsProxyWidget()
        button = QtGui.QPushButton('Exit')
        button.clicked.connect(lambda: self.win.destroy())
        button.setFont(_font)
        proxy.setWidget(button)
        self.win.addItem(proxy,row=3,col=0)


    def update(self):
        try:
            if self.latencyPlot:pass
            else: self.initUI()
        except:
            self.initUI()

        try:
            self.latencyPlot.removeItem(self.signal)
            self.latencyPlot.removeItem(self.envelope1)
            self.latencyPlot.removeItem(self.envelope2)
            self.latencyPlot.removeItem(self.phase)
            # self.latencyPlot.removeItem(self.proxy)
        except:pass
        sig_waveform, _      = self.workspace.get_waveform(self.maingui.current_id,flag='filtered')
        envelope = self.sig.get_envelope(sig_waveform)
        ton_dist,toff_dist = self.sig.get_onet_offset_dist(sig_waveform)
        self.signal = pg.PlotDataItem(self.const.t*1000,sig_waveform/max(sig_waveform),pen=pg.mkPen('w', width=2))
        self.envelope1 = pg.PlotDataItem(self.const.t*1000,envelope,pen=pg.mkPen('b', width=2))
        self.envelope2 = pg.PlotDataItem(self.const.t*1000,-envelope,pen=pg.mkPen('b', width=2))
        self.phase     = pg.PlotDataItem(self.const.t*1000,self.sig.get_diffenvelope(sig_waveform,scaled=True)-2,pen=pg.mkPen('g', width=2))
        self.on_latency  = pg.PlotDataItem(self.const.t*1000,ton_dist,fillLevel=0,brush=(0,255,0,70),fillOutline=False, width=0)
        self.off_latency = pg.PlotDataItem(self.const.t*1000,toff_dist,fillLevel=0,brush=(255,0,0,70),fillOutline=False, width=0)
        self.__add_on_offset_cursors('load') #update the cursor with cross correlation

        self.latencyPlot.addItem(self.signal)
        self.latencyPlot.addItem(self.envelope1)
        self.latencyPlot.addItem(self.envelope2)
        self.latencyPlot.addItem(self.phase)
        self.latencyPlot.addItem(self.on_latency)
        self.latencyPlot.addItem(self.off_latency)
        self.latencyPlot.update()

    def createPlot(self):


        self.__add_on_offset_cursors("load")

            # self.__add_cursor()


        sig_waveform, _      = self.workspace.get_waveform(self.maingui.current_id,flag='filtered')
        envelope = self.sig.get_envelope(sig_waveform)
        ton_dist,toff_dist = self.sig.get_onet_offset_dist(sig_waveform)
        self.signal = pg.PlotDataItem(self.const.t*1000,sig_waveform/max(sig_waveform),pen=pg.mkPen('w', width=2))
        self.envelope1   = pg.PlotDataItem(self.const.t*1000,envelope,pen=pg.mkPen('b', width=2))
        self.envelope2   = pg.PlotDataItem(self.const.t*1000,-envelope,pen=pg.mkPen('b', width=2))
        self.phase       = pg.PlotDataItem(self.const.t*1000,self.sig.get_diffenvelope(sig_waveform,scaled=True)-2,pen=pg.mkPen('g', width=2))
        self.on_latency  = pg.PlotDataItem(self.const.t*1000,ton_dist,fillLevel=0,brush=(0,255,0,70),fillOutline=False, width=0)
        self.off_latency = pg.PlotDataItem(self.const.t*1000,toff_dist,fillLevel=0,brush=(255,0,0,70),fillOutline=False, width=0)
        self.w_plv       = pg.TextItem('PLV',color=(255, 0, 255))
        self.w_plv.setPos(75,-1.5)
        self.w_plv.setFont(QFont("Times", 20, QFont.Bold))

        self.latencyPlot.addItem(self.signal)
        self.latencyPlot.addItem(self.envelope1)
        self.latencyPlot.addItem(self.envelope2)
        self.latencyPlot.addItem(self.phase)
        self.latencyPlot.addItem(self.on_latency)
        self.latencyPlot.addItem(self.off_latency)
        self.latencyPlot.addItem(self.w_plv)

        self.latencyPlot.showGrid(x=True, y=True)
        self.latencyPlot.setLabel('left', "Amplitude [nV]")
        self.latencyPlot.setLabel('bottom', "Time [ms]",fontsize=20)

        font=QtGui.QFont()
        font.setPixelSize(100)
        self.latencyPlot.getAxis("left").tickFont = font
        self.latencyPlot.getAxis("bottom").tickFont = font
        self.latencyPlot.setXRange(0,self.TMAX, padding=0)
        self.latencyPlot.setYRange(-2.0,1.2, padding=0)
        self.latencyPlot.setLimits(xMin=0,xMax=self.TMAX,yMin=-1.4,yMax=1.4)
        self.latencyPlot.update()

    def __clear_plot(self):
        pass


    def __cursor_moved(self,cursor):
        if cursor.name()=="onsetCursor":
            self.workspace.onset = float(cursor.value())
            cursor.label.setText("{:.1f}".format(self.workspace.onset))
            self._offsetcursor.label.setText("{:.1f}".format(self._offsetcursor.value()-cursor.value()))
        elif cursor.name()=="offsetCursor":
            self.workspace.offset = float(cursor.value())
            cursor.label.setText("{:.1f}".format(self.workspace.offset-self.workspace.onset))

        #Update windowed PLV
        sig_waveform, _ = self.workspace.get_waveform(self.maingui.current_id,flag='filtered')
        _w_plv = self.sig.get_wind_plv(self.sig.get_diffenvelope(sig_waveform))
        self.w_plv.setText(str("{:.3f}".format(_w_plv)))
        self.w_plv.setColor(self.colormapPLV(int(_w_plv*100)))

    def colormapPLV(self,plv):
        cmap = matplotlib.cm.get_cmap('jet')
        norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
        rgba = cmap(norm(np.arange(0,1.01,0.01)))*255
        rgb  = (int(rgba[plv][0]),int(rgba[plv][1]),int(rgba[plv][2]))
        return rgb

    def __add_on_offset_cursors(self,flag):
        if flag=='new':
            xpos_onset,xpos_offset  = 5, 62
            on_color = pg.mkPen((0, 255, 0,255))
            off_color = pg.mkPen((255, 0, 0,255))
        elif flag=="phaseshift":
            xpos_onset  = np.random.randint(5,self.TMAX,1)[0]
            xpos_offset = xpos_onset+57
            on_color = pg.mkPen((255, 255, 0,255))
            off_color = pg.mkPenself.workspace.offset-((255, 255, 0,255))

        elif flag=='load':
            xpos_onset,xpos_offset  = self.workspace.get_on_offset(self.maingui.current_id)
            if xpos_onset==-1 and (self.maingui.current_id=='0' or self.maingui.current_id=='5'): #only for EFR
                time_shift = self.sig.cross_corr_stim(self.workspace.get_waveform(self.maingui.current_id,flag='filtered')[0])
                xpos_onset = time_shift
                xpos_offset = time_shift + 57.0
                self.workspace.onset = xpos_onset
                self.workspace.offset = xpos_offset
                print(xpos_onset, xpos_offset)
            on_color = pg.mkPen((0, 255, 0,255))
            off_color = pg.mkPen((255, 0, 0,255))

        _onsetcursor = pg.InfiniteLine(pos=xpos_onset,
                                 pen=on_color, markers = '<|>',
                                 hoverPen=pg.mkPen((0, 255, 0,255), width=10),
                                 label=str(5),bounds=[0,max(self.const.t)*1000],
                                 name="onsetCursor",movable=True)
        _onsetcursor.label.setMovable(True)
        _onsetcursor.label.setPosition(0.95)
        _onsetcursor.label.setColor(pg.mkColor((255, 200, 0,255)))
        _onsetcursor.label.setFont(QFont("Times", 20, QFont.Bold))
        _onsetcursor.label.setText("{:.1f}".format(_onsetcursor.value()))
        _onsetcursor.sigDragged.connect(self.__cursor_moved)

        _offsetcursor = pg.InfiniteLine(pos=xpos_offset,
                                 pen=off_color, markers = '<|>',
                                 hoverPen=pg.mkPen((255, 0, 0,255), width=10),
                                 label=str(5),bounds=[0,max(self.const.t)*1000],
                                 name="offsetCursor",movable=True)
        _offsetcursor.label.setMovable(True)
        _offsetcursor.label.setPosition(0.95)
        _offsetcursor.label.setColor(pg.mkColor((255, 200, 0,255)))
        _offsetcursor.label.setFont(QFont("Times", 20, QFont.Bold))
        _offsetcursor.label.setText("{:.1f}".format(_offsetcursor.value()))

        _offsetcursor.sigDragged.connect(self.__cursor_moved)
        self._onsetcursor, self._offsetcursor = _onsetcursor, _offsetcursor
        self.latencyPlot.addItem(self._onsetcursor)
        self.latencyPlot.addItem(self._offsetcursor)

    def __load_cursors_from_workspace(self):
        self.__add_on_offset_cursors('load')








if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = latencyPlotWidget()
    ex.initUI()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()
