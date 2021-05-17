# -*- coding: utf-8 -*-
import sys,os,re
import numpy as np
from scipy import signal

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QColor, QPen, QMouseEvent, QFont
# from PyQt5.QtCore import QEvent
# from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *

dir_path = os.path.dirname(os.path.realpath(__file__))

import pyqtgraph as pg
from pyqtgraph import PlotWidget, GraphicsLayout, GraphicsWindow, GraphicsScene
from PyQt5.QtCore import QEvent, QRect

######################
from ffrgui.dsp       import Signal
from ffrgui.gui       import PatientTable,SpectralWidget
from ffrgui.utilities import Workspace,FFR_Utils





class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        ##############################
        self.defaultScList = {'Channel-V':{'EFR':[],'CDT':[],'F1':[],'F2':[],'ABR':[]}, \
                              'Channel-H':{'EFR':[],'CDT':[],'F1':[],'F2':[],'ABR':[],} }
        self.initSClist    = ['EFR V','EFR H','F1 V','F1 H','F2 V','F2 H','CDT V','CDT H','ABR V','ABR H',]
        self.current_json  = None
        self.current_sc    = 'EFR V'
        self.current_id    = 1
        ##############################
        self.ffrutils   = FFR_Utils.FFR_Utils()
        self.name,self.number,self.date,self.stim,self.ear,self.level,self.path2json, self.code = self.ffrutils.list_all()

        ##############################
        self.workspace      = Workspace.Workspace(self)
        self.current_workspace=None
        ##############################
        self.sig   = Signal.Signal(self)
        ##############################

        self.table = PatientTable.PatientTable(self)
        self.tableWidget = self.table.initUI()
        ##############################
        self.spectralWidget = SpectralWidget.SpectralWidget(self)
        self.roi_Filter     = self.spectralWidget.initUI()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1794, 972)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SelectPatientWidget = QtWidgets.QWidget(self.centralwidget)
        self.SelectPatientWidget.setGeometry(QtCore.QRect(300, 20, 1011, 81))
        font = QtGui.QFont()
        font.setItalic(True)
        self.SelectPatientWidget.setFont(font)
        self.SelectPatientWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.SelectPatientWidget.setObjectName("SelectPatientWidget")


        self.PatientDataWidget = QtWidgets.QWidget(self.centralwidget)
        self.PatientDataWidget.setGeometry(QtCore.QRect(10, 110, 281, 351))
        self.PatientDataWidget.setObjectName("PatientDataWidget")
        self.PatientView = QtWidgets.QListView(self.PatientDataWidget)
        self.PatientView.setGeometry(QtCore.QRect(10, 30, 251, 291))
        self.PatientView.setObjectName("PatientView")
        self.PatientLabel = QtWidgets.QLabel(self.PatientDataWidget)
        self.PatientLabel.setGeometry(QtCore.QRect(10, 10, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PatientLabel.setFont(font)
        self.PatientLabel.setObjectName("PatientLabel")

        self.ButtonWidget = QtWidgets.QWidget(self.centralwidget)
        self.ButtonWidget.setGeometry(QtCore.QRect(10, 510, 271, 371))
        self.ButtonWidget.setObjectName("ButtonWidget")
        self.ButtonRefresh = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonRefresh.setGeometry(QtCore.QRect(30, 250, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonRefresh.setFont(font)
        self.ButtonRefresh.setObjectName("ButtonRefresh")
        self.ButtonOpenPatientTable = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonOpenPatientTable.setGeometry(QtCore.QRect(30, 190, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonOpenPatientTable.setFont(font)
        self.ButtonOpenPatientTable.setObjectName("Open")
        self.ButtonLatency = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonLatency.setGeometry(QtCore.QRect(30, 70, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonLatency.setFont(font)
        self.ButtonLatency.setObjectName("ButtonLatency")
        self.ButtonLatency.setCheckable(True)
        self.ButtonFFT = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonFFT.setGeometry(QtCore.QRect(30, 10, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonFFT.setFont(font)
        self.ButtonFFT.setObjectName("ButtonFFT")
        self.ButtonAddControl = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonAddControl.setGeometry(QtCore.QRect(30, 310, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonAddControl.setFont(font)
        self.ButtonAddControl.setObjectName("ButtonAddControl")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)

        self.PlotTemporalWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.PlotTemporalWidget_2.setGeometry(QtCore.QRect(300, 110, 1481, 1200))
        self.PlotTemporalWidget_2.setObjectName("PlotTemporalWidget_2")
        self.PlotTemporalWidget = PlotWidget(self.PlotTemporalWidget_2)
        self.PlotTemporalWidget.setGeometry(QtCore.QRect(10, 10, 1451, 900))
        self.PlotTemporalWidget.setObjectName("PlotTemporalWidget")
        self.PatientLabel_9 = QtWidgets.QLabel(self.PlotTemporalWidget_2)
        self.PatientLabel_9.setGeometry(QtCore.QRect(200, 730, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PatientLabel_9.setFont(font)
        self.PatientLabel_9.setObjectName("PatientLabel_9")
        self.PatientLabel_10 = QtWidgets.QLabel(self.PlotTemporalWidget_2)
        self.PatientLabel_10.setGeometry(QtCore.QRect(380, 730, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PatientLabel_10.setFont(font)
        self.PatientLabel_10.setObjectName("PatientLabel_10")
        self.PatientLabel_11 = QtWidgets.QLabel(self.PlotTemporalWidget_2)
        self.PatientLabel_11.setGeometry(QtCore.QRect(550, 730, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PatientLabel_11.setFont(font)
        self.PatientLabel_11.setObjectName("PatientLabel_11")
        self.PatientLabel_12 = QtWidgets.QLabel(self.PlotTemporalWidget_2)
        self.PatientLabel_12.setGeometry(QtCore.QRect(750, 730, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PatientLabel_12.setFont(font)
        self.PatientLabel_12.setObjectName("PatientLabel_12")
        self.PatientLabel_13 = QtWidgets.QLabel(self.PlotTemporalWidget_2)
        self.PatientLabel_13.setGeometry(QtCore.QRect(20, 730, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PatientLabel_13.setFont(font)
        self.PatientLabel_13.setObjectName("PatientLabel_13")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1794, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionOpen_Workflow = QtWidgets.QAction(MainWindow)
        self.actionOpen_Workflow.setObjectName("actionOpen_Workflow")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen_Workflow)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.actions()


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def actions(self):
        self.ButtonOpenPatientTable.clicked.connect(  lambda : self.table.show()                                     )
        self.ButtonRefresh.clicked.connect(           lambda : self.update_temporal_Plot()                           )
        self.table.tableWidget.clicked.connect(       lambda : self.update_temporal_Plot())


        self.ButtonLatency.clicked.connect(           lambda: self.update_tf_plot()                                  )
        # self.ButtonLatency.clicked.connect(           lambda : self.update_widget_size(self.ButtonLatency.isChecked()))

        self.ButtonFFT.clicked.connect(               lambda: self.spectralWidget.initUI()                         )
        # self.spectralWidget.lr.sigRegionChanged.connect(lambda: self.test_print())



    def update_labels(self):
        self.PatientLabel_9.setText(self.current_sc)

    def update_rois(self):
        self.roisdict = {'initROI':pg.RectROI([0,1], [1, 1],pen=QPen(QColor(255, 0, 0,0)))}
        roi_width = np.max(self.ffrutils.t*1000)
        # for id,sc in self.waveforms.keys():
        for id, sc in enumerate(self.sc_list):
            roi_y_pos  = np.min(self.waveforms[:,id])
            roi_height = np.abs(np.max(self.waveforms[:,id])-np.min(self.waveforms[:,id]))
            _rectroi   = pg.RectROI(pos=[0,roi_y_pos], size=[roi_width, roi_height], \
                       movable=True, resizable=False, removable=True, \
                       maxBounds=QRectF(0,20*roi_y_pos,roi_width,20*roi_height) ,\
                       pen=pg.mkPen((255, 0, 0,0), width=0),\
                       hoverPen=pg.mkPen((255, 0, 0,0), width=0),\
                       handlePen=pg.mkPen((255, 0, 0,0), width=0))

            _roi       = {id:_rectroi}
            self.roisdict.update(_roi)
            self.PlotTemporalWidget.addItem(self.roisdict[id])
            self.roisdict[id].setAcceptedMouseButtons(QtCore.Qt.LeftButton)
            self.roisdict[id].sigClicked.connect(self.select_waveform)
            self.roisdict[id].sigClicked.connect(self.update_labels)
            self.roisdict[id].sigClicked.connect(self.update_temporal_Plot)

            self.roisdict[id].sigRegionChangeFinished.connect(self.move_waveform)
            self.roisdict[id].sigRegionChanged.connect(self.move_waveform)
        del self.roisdict['initROI']

    def move_waveform(self,roi):
        pass


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
        self.current_id       = id
        self.current_waveform = self.waveforms[:,id]
        return sc

    def __add_clickable_background(self):
        roi = pg.RectROI(pos=[0,0], size=[max(self.ffrutils.t)*1000, 20],centered=True, \
                   movable=False, resizable=False, removable=True ,\
                   pen=pg.mkPen((255, 0, 0,0)),hoverPen=pg.mkPen((0, 255, 0,0)),handlePen=pg.mkPen((0, 255, 0,0)))
        roi.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        roi.sigClicked.connect(self.__add_cursor)
        self.PlotTemporalWidget.addItem(roi)


    def __add_cursor(self):
        print("Add Cursor")
        xpos=np.random.randint(0,max(self.ffrutils.t)*1000)
        cursor = pg.InfiniteLine(pos=xpos,pen=pg.mkPen('r', width=2),\
                                markers = '<|>',label=str(xpos) )
        cursor.setMovable(True)
        cursor.setBounds([0,max(self.ffrutils.t)*1000])
        cursor.label.setMovable(True)
        cursor.label.setMovable(True)
        cursor.label.setY(0)
        cursor.label.setColor(pg.mkColor((255, 0, 0,150)))
        cursor.label.setFont(QFont("Times", 20, QFont.Bold))
        cursor.sigDragged.connect(self.__cursor_moved)
        self.PlotTemporalWidget.addItem(cursor)
        pass

    # def __add_target_label(self,cursor):
    #     label = pg.TargetItem(pos=(cursor.value(),0),size=20,label=str(cursor.value()))

    def __cursor_moved(self,cursor):
        cursor.label.setText("{:.1f}".format(cursor.value()))


    def update_tf_plot(self):
        print('latency clicked')
        self.PlotTemporalWidget.clear()
        plotitem     = pg.PlotDataItem(self.ffrutils.t*1000,self.current_waveform/np.max(self.current_waveform),pen=pg.mkPen('g', width=1))
        self.PlotTemporalWidget.addItem(plotitem)

        analytic_signal   = signal.hilbert(self.current_waveform)
        self.IAmplitude   = np.abs(analytic_signal)
        self.IAmplitude   = self.IAmplitude/np.max(self.IAmplitude)-2
        plotitem     = pg.PlotDataItem(self.ffrutils.t*1000,self.IAmplitude,pen=pg.mkPen('r', width=1))
        self.PlotTemporalWidget.addItem(plotitem)

        self.IPhase       = np.unwrap(np.angle(analytic_signal))
        self.DeltaPhase   = np.abs(self.IPhase - 2*np.pi*self.ffrutils.get_frequency(self.current_sc)*self.ffrutils.t)
        self.DeltaPhase   = self.DeltaPhase/np.max(self.DeltaPhase)-4
        plotitem     = pg.PlotDataItem(self.ffrutils.t*1000,self.DeltaPhase ,pen=pg.mkPen('b', width=1))
        self.PlotTemporalWidget.addItem(plotitem)


        self.PlotTemporalWidget.setLabel('bottom', 'Time [ms]', color='white', size=100)


    def update_temporal_Plot(self,arg=None):
        # self.ffrutils.load_path(self.current_json)
        # waveforms, _ = self.ffrutils.load_AVGs()
        waveforms, self.sc_list = self.workspace.load_AVGs()

        self.PlotTemporalWidget.clear()
        waveforms, scale_factor = self.sig.normalize_waveforms(waveforms)
        # waveforms               = self.sig.order_waveforms(waveforms,self.initSClist)
        self.waveforms       = self.sig.offset_waveforms(waveforms)


        for id, sc in enumerate(self.sc_list):
            if sc=="Stimulus":c='g'
            elif sc[0]=="R ": c='r'
            elif sc[0]=="C ": c='b'
            elif self.current_sc!=None and self.current_id==id: c = 'g'
            else: c='w'
            plotitem     = pg.PlotDataItem(self.ffrutils.t*1000,self.waveforms[:,id],pen=pg.mkPen(c, width=1))
            self.PlotTemporalWidget.addItem(plotitem)
            label = pg.TextItem(sc, color="r", anchor=(0, 0))
            label.setPos(np.amax(self.ffrutils.t*1000),self.waveforms[:,id].mean() )
            # label.setTextWidth(10)
            self.PlotTemporalWidget.addItem(label)


        self.PlotTemporalWidget.setLimits(xMin=0,yMin=self.waveforms[:,id].min(),yMax=2,xMax=1.1*self.ffrutils.t.max()*1000)
        self.PlotTemporalWidget.setLabel('bottom', 'Time [ms]', color='white', size=200)
        self.PlotTemporalWidget.setXRange(0, 1.1*self.ffrutils.t.max()*1000, padding=0)
        self.PlotTemporalWidget.setYRange(self.waveforms[:,id].min(), 2, padding=0)
        self.update_rois()
        self.__add_clickable_background()


    def test_print(self):
        print('test_print')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.PatientLabel.setText(_translate("MainWindow", "               Patient"))

        self.ButtonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.ButtonOpenPatientTable.setText(_translate("MainWindow", "Open"))
        self.ButtonLatency.setText(_translate("MainWindow", "Latency"))
        self.ButtonFFT.setText(_translate("MainWindow", "Spectral"))
        self.ButtonAddControl.setText(_translate("MainWindow", "Add to Control"))
        self.PatientLabel_9.setText(_translate("MainWindow", "SCstring"))
        self.PatientLabel_10.setText(_translate("MainWindow", "On = "))
        self.PatientLabel_11.setText(_translate("MainWindow", "Off ="))
        self.PatientLabel_12.setText(_translate("MainWindow", "Duration ="))
        self.PatientLabel_13.setText(_translate("MainWindow", "t ="))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "New File"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionOpen_Workflow.setText(_translate("MainWindow", "Open Workflow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Breeze')
    #ex = MouseTracker()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
