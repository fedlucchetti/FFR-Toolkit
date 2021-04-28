# -*- coding: utf-8 -*-
import sys,os,re
import numpy as np
from scipy import signal

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QColor, QPen, QMouseEvent
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import pyqtSlot





dir_path = os.path.dirname(os.path.realpath(__file__))

#from pyqtgraph import PlotWidget, plot, mkPen, RectROI, PlotDataItem
import pyqtgraph as pg
from pyqtgraph import PlotWidget, GraphicsLayout, GraphicsWindow

from PyQt5.QtCore import QEvent, QRect


######################
from ffrgui.utilities import FFRJSON
from ffrgui import PatientTable
from ffrgui import Combo_Select_Patient as combo_patient
from ffrgui import Signal


class Ui_MainWindow(object):
    def __init__(self):
        self.ffrjson   = FFRJSON.FFRJSON()
        self.sig   = Signal.Signal()
        self.table = PatientTable.App()
        self.tableWidget = self.table.initUI()



        #super().__init__()
        name,number,date,stim,ear,level,path2json, code = self.ffrjson.list_all()
        self.name      = np.array(name)
        self.number    = np.array(number)
        self.date      = np.array(date)
        self.stim      = np.array(stim)
        self.ear       = np.array(ear)
        self.level     = np.array(level)
        self.path2json = np.array(path2json)
        self.code      = np.array(code)
        self.defaultScList = {'Channel-V':{'EFR':[],'CDT':[],'F1':[],'F2':[],'ABR':[]}, \
                              'Channel-H':{'EFR':[],'CDT':[],'F1':[],'F2':[],'ABR':[],} }
        self.initSClist    = ['EFR V','EFR H','F1 V','F1 H','F2 V','F2 H','CDT V','CDT H','ABR V','ABR H',]

        self.initpath     = '/media/ergonium/KINGSTON/AnalyseFFR_LV/Patients&Subjects/NewNH20172018/170392/Harmonique_RE/85dB/Meta_AVG_data.json'
        self.current_json = self.initpath
        self.current_sc   = 'EFR V'
        self.rois         = []

        self.highpass = 4000
        self.lowpass  = 50

        self.roi_High_filter = pg.RectROI(pos = [0,1000], size = [1, 1])
        self.roi_Low_filter  = pg.RectROI(pos = [0,100],  size = [1, 1])


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

        self.ComboName, self.ComboNumber, self.ComboEar, self.ComboLevel, self.ComboStim = combo_patient.setupComboUi(self.SelectPatientWidget)

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
        self.WidgetFilter = QtWidgets.QWidget(self.centralwidget)
        self.WidgetFilter.setGeometry(QtCore.QRect(1320, 110, 461, 801))
        self.WidgetFilter.setObjectName("WidgetFilter")
        self.PlotSpectralWidget = PlotWidget(self.WidgetFilter)
        self.PlotSpectralWidget.setGeometry(QtCore.QRect(10, 10, 441, 701))
        self.PlotSpectralWidget.setObjectName("PlotSpectralWidget")
        self.ButtonAddFilter = QtWidgets.QPushButton(self.WidgetFilter)
        self.ButtonAddFilter.setGeometry(QtCore.QRect(310, 720, 51, 51))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonAddFilter.setFont(font)
        self.ButtonAddFilter.setObjectName("ButtonAddFilter")
        self.ButtonRemoveFilter = QtWidgets.QPushButton(self.WidgetFilter)
        self.ButtonRemoveFilter.setGeometry(QtCore.QRect(380, 720, 51, 51))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonRemoveFilter.setFont(font)
        self.ButtonRemoveFilter.setObjectName("ButtonRemoveFilter")
        self.ComboFilterType = QtWidgets.QComboBox(self.WidgetFilter)
        self.ComboFilterType.setGeometry(QtCore.QRect(10, 720, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setItalic(True)
        self.ComboFilterType.setFont(font)
        self.ComboFilterType.setObjectName("ComboFilterType")
        self.ComboFilterType.addItem("")
        self.ComboFilterType.addItem("")
        self.ComboFilterType.addItem("")



        self.ButtonWidget = QtWidgets.QWidget(self.centralwidget)
        self.ButtonWidget.setGeometry(QtCore.QRect(10, 510, 271, 371))
        self.ButtonWidget.setObjectName("ButtonWidget")
        self.ButtonExport = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonExport.setGeometry(QtCore.QRect(30, 250, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonExport.setFont(font)
        self.ButtonExport.setObjectName("ButtonExport")
        self.ButtonPrint = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonPrint.setGeometry(QtCore.QRect(30, 190, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonPrint.setFont(font)
        self.ButtonPrint.setObjectName("ButtonPrint")
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
        self.ButtonFilter = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonFilter.setGeometry(QtCore.QRect(30, 130, 221, 51))
        self.ButtonFilter.setCheckable(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonFilter.setFont(font)
        self.ButtonFilter.setStyleSheet("")
        self.ButtonFilter.setObjectName("ButtonFilter")
        self.PlotTemporalWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.PlotTemporalWidget_2.setGeometry(QtCore.QRect(300, 110, 1481, 731))
        self.PlotTemporalWidget_2.setObjectName("PlotTemporalWidget_2")
        self.PlotTemporalWidget = PlotWidget(self.PlotTemporalWidget_2)
        self.PlotTemporalWidget.setGeometry(QtCore.QRect(10, 10, 1451, 731))
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

        self.populate_combos()
        self.actions()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def populate_combos(self):
        for idx in range(len(self.name)):self.ComboName.addItem("")
        for idx in range(5):self.ComboNumber.addItem("")
        for idx in range(2):self.ComboEar.addItem("")
        for idx in range(5):self.ComboLevel.addItem("")
        for idx in range(10):self.ComboStim.addItem("")

    def actions(self):
        # define action
        self.ComboName.activated['QString'].connect(  lambda : self.update_all_combo('name')             )
        self.ComboNumber.activated['QString'].connect(lambda : self.update_all_combo('number')           )
        self.ComboEar.activated['QString'].connect(   lambda : self.update_all_combo('ear')              )
        self.ComboLevel.activated['QString'].connect( lambda : self.update_all_combo('level')            )
        self.ComboStim.activated['QString'].connect(  lambda : self.update_all_combo('stim')             )
        self.ComboStim.activated['QString'].connect(  lambda : self.update_temporal_Plot                 )
        # self.ButtonExport.clicked.connect(            lambda : self.update_temporal_Plot()               )
        self.ButtonExport.clicked.connect(            lambda : self.table.show()               )
        self.ButtonAddControl.clicked.connect(            lambda : print(self.table.selected_json) )
        # self.tableWidget.doubleClicked.connect(lambda : self.table_on_click)


        self.ButtonFilter.clicked.connect(            lambda : self.update_widget_size(self.ButtonFilter.isChecked()))

        self.ButtonAddFilter.clicked.connect(         lambda : self.update_temporal_Plot(arg = 'auto_filter'))
        self.roi_High_filter.sigRegionChanged.connect(lambda:print('roi changed'))

        self.roi_High_filter.sigRegionChanged.connect(lambda:self.update_temporal_Plot())
        self.roi_Low_filter.sigRegionChanged.connect(lambda:self.update_temporal_Plot())

        self.ButtonLatency.clicked.connect(lambda: self.update_tf_plot())
        self.ButtonLatency.clicked.connect(lambda : self.update_widget_size(self.ButtonLatency.isChecked()))
        #self.PlotTemporalWidget.mouseDoubleClickEvent(self, event)


    def update_widget_size(self,flag):
        if flag:
            self.PlotTemporalWidget_2.setGeometry(QtCore.QRect(300, 110, 1011, 771))
            self.PlotTemporalWidget.setGeometry(QtCore.QRect(10, 10, 991, 731))
            self.WidgetFilter.setVisible(True)
            #self.WidgetFilter.activateWindow()
            #self.WidgetFilter.show()
        else:
            self.PlotTemporalWidget_2.setGeometry(QtCore.QRect(300, 110, 1481, 771))
            self.PlotTemporalWidget.setGeometry(QtCore.QRect(10, 10, 1451, 731))
            self.WidgetFilter.setVisible(False)


    def update_labels(self):
        self.PatientLabel_9.setText(self.current_sc)

    def update_all_combo(self,combo):
        if self.ComboName.currentText()!="":


            pattern = ''.join([self.ComboName.currentText()   , \
                               self.ComboNumber.currentText() , \
                               self.ComboEar.currentText()    , \
                               self.ComboLevel.currentText()  , ])

            match         = np.array([])
            displayStim   = np.array([])
            displayLevel  = np.array([])
            displayEar    = np.array([])
            displayNumber = np.array([])
            for idx in range(len(self.code)):
                #print(self.code[idx])
                if len(pattern)!= 0 and re.search(pattern,self.code[idx]):
                    match = np.append(match,idx)
                    #print(self.code[idx])

                    if combo == 'level':
                        displayStim   = np.append(displayStim,self.stim[idx])
                    elif combo == 'ear':
                        displayStim   = np.append(displayStim,self.stim[idx])
                        displayLevel  = np.append(displayLevel,self.level[idx])
                    elif combo == 'number':
                        displayStim   = np.append(displayStim,self.stim[idx])
                        displayLevel  = np.append(displayLevel,self.level[idx])
                        displayEar    = np.append(displayEar,self.ear[idx])
                    elif combo == 'name':
                        displayStim   = np.append(displayStim,self.stim[idx])
                        displayLevel  = np.append(displayLevel,self.level[idx])
                        displayEar    = np.append(displayEar,self.ear[idx])
                        displayNumber = np.append(displayNumber,self.number[idx])
                else:pass

            open_json_path = list()
            if combo == 'stim':
                search_json = pattern+self.ComboStim.currentText()
                for idx in range(len(self.code)):
                    if re.search(search_json,self.code[idx]):
                        open_json_path.append(self.path2json[idx])
                    else:
                        pass

            elif combo == 'level':
                displayStim   = np.array(list(dict.fromkeys(displayStim)))
                self.ComboStim.clear()
                self.ComboStim.addItem("?")
                for idx in range(len(displayStim)): self.ComboStim.addItem(displayStim[idx])
            elif combo == 'ear':
                displayStim   = np.array(list(dict.fromkeys(displayStim)))
                self.ComboStim.clear()
                self.ComboStim.addItem("?")
                for idx in range(len(displayStim)): self.ComboStim.addItem(displayStim[idx])

                displayLevel  = np.array(list(dict.fromkeys(displayLevel)))
                self.ComboLevel.clear()
                self.ComboLevel.addItem("")
                for idx in range(len(displayLevel)): self.ComboLevel.addItem(displayLevel[idx])
            elif combo == 'number':
                displayStim   = np.array(list(dict.fromkeys(displayStim)))
                self.ComboStim.clear()
                self.ComboStim.addItem("?")
                for idx in range(len(displayStim)): self.ComboStim.addItem(displayStim[idx])

                displayLevel  = np.array(list(dict.fromkeys(displayLevel)))
                self.ComboLevel.clear()
                self.ComboLevel.addItem("")
                for idx in range(len(displayLevel)): self.ComboLevel.addItem(displayLevel[idx])

                displayEar    = np.array(list(dict.fromkeys(displayEar)))
                self.ComboEar.clear()
                self.ComboEar.addItem("")
                for idx in range(len(displayEar)): self.ComboEar.addItem(displayEar[idx])
            elif combo == 'name':
                displayStim   = np.array(list(dict.fromkeys(displayStim)))
                self.ComboStim.clear()
                self.ComboStim.addItem("?")
                for idx in range(len(displayStim)): self.ComboStim.addItem(displayStim[idx])

                displayLevel  = np.array(list(dict.fromkeys(displayLevel)))
                self.ComboLevel.clear()
                self.ComboLevel.addItem("")
                for idx in range(len(displayLevel)): self.ComboLevel.addItem(displayLevel[idx])

                displayEar    = np.array(list(dict.fromkeys(displayEar)))
                self.ComboEar.clear()
                self.ComboEar.addItem("")
                for idx in range(len(displayEar)): self.ComboEar.addItem(displayEar[idx])

                displayNumber = np.array(list(dict.fromkeys(displayNumber)))
                self.ComboNumber.clear()
                self.ComboNumber.addItem("")
                for idx in range(len(displayNumber)): self.ComboNumber.addItem(displayNumber[idx])

            else:pass

            if   len(open_json_path) > 1 and open_json_path!=None :
                self.current_json = open_json_path[0]
                self.update_temporal_Plot()
            elif len(open_json_path) ==1 and open_json_path!=None :
                self.current_json = open_json_path
                self.update_temporal_Plot()
            else: pass

    def update_rois(self):
        self.roisdict = {'initROI':pg.RectROI([0,1], [1, 1],pen=QPen(QColor(255, 0, 0,0)))}
        roi_width = np.max(self.ffrjson.t*1000)
        for sc in self.waveforms.keys():
            roi_y_pos  = np.min(self.waveforms[sc])
            roi_height = np.abs(np.max(self.waveforms[sc])-np.min(self.waveforms[sc]))
            _roi       = {sc:pg.RectROI([0,roi_y_pos], [roi_width, roi_height],pen=QPen(QColor(255, 0, 0,0)))}
            self.roisdict.update(_roi)
            self.PlotTemporalWidget.addItem(self.roisdict[sc])
            self.roisdict[sc].setAcceptedMouseButtons(QtCore.Qt.LeftButton)
            self.roisdict[sc].sigClicked.connect(self.select_waveform)
            self.roisdict[sc].sigClicked.connect(self.update_labels)
            self.roisdict[sc].sigClicked.connect(self.update_temporal_Plot)
        del self.roisdict['initROI']

    def select_waveform(self,roi):
        x,y = roi.pos()
        w,h = roi.size()
        y   = y + 0.5*h
        for sc in self.waveforms.keys():
            if y<=np.max(self.waveforms[sc]) and y>=np.min(self.waveforms[sc]):
                break
            else: pass
        print(sc)
        self.update_filter_Plot(sc)
        self.current_sc       = sc
        self.current_waveform = self.waveforms[sc]
        return sc

    def update_filter_Plot(self,sc=None, bandwidth=None):
        if bandwidth!=None:
            roi_height = bandwidth
        else: roi_height = 500
        if sc==None: sc = self.current_sc
        self.PlotSpectralWidget.clear()
        _tmp    = np.absolute(np.fft.fft(self.waveforms[sc]-np.mean(self.waveforms[sc])))
        spectra =_tmp[0:self.ffrjson.Nf]
        self.plotitem     = pg.PlotDataItem(spectra,self.ffrjson.f,pen=pg.mkPen('w', width=1))
        self.PlotSpectralWidget.addItem(self.plotitem)
        self.PlotSpectralWidget.setYRange(0, 6000, padding=0)
        self.PlotSpectralWidget.setMouseEnabled(x=False, y=False)
        self.roi_High_filter = pg.RectROI(pos = [0,1000], size = [np.max(spectra), 100],    \
                                maxBounds=QRect(0, 0, np.max(spectra), 6000),   \
                                pen='r')
        self.roi_Low_filter = pg.RectROI(pos = [0,100], size = [np.max(spectra), 100],    \
                                maxBounds=QRect(0, 0, np.max(spectra), 6000),   \
                                pen='b')
        self.roi_High_filter.addScaleHandle([0.5, 0], [0.5, 1])
        self.roi_High_filter.addScaleHandle([0.5, 0], [0.5, 1])
        self.PlotSpectralWidget.addItem(self.roi_High_filter)
        self.PlotSpectralWidget.addItem(self.roi_Low_filter)

    def update_tf_plot(self):
        print('latency clicked')
        self.PlotTemporalWidget.clear()
        self.plotitem     = pg.PlotDataItem(self.ffrjson.t*1000,self.current_waveform/np.max(self.current_waveform),pen=pg.mkPen('g', width=1))
        self.PlotTemporalWidget.addItem(self.plotitem)

        analytic_signal   = signal.hilbert(self.current_waveform)
        self.IAmplitude   = np.abs(analytic_signal)
        self.IAmplitude   = self.IAmplitude/np.max(self.IAmplitude)-2
        self.plotitem     = pg.PlotDataItem(self.ffrjson.t*1000,self.IAmplitude,pen=pg.mkPen('r', width=1))
        self.PlotTemporalWidget.addItem(self.plotitem)

        self.IPhase       = np.unwrap(np.angle(analytic_signal))
        self.DeltaPhase   = np.abs(self.IPhase - 2*np.pi*self.ffrjson.get_frequency(self.current_sc)*self.ffrjson.t)
        self.DeltaPhase   = self.DeltaPhase/np.max(self.DeltaPhase)-4
        self.plotitem     = pg.PlotDataItem(self.ffrjson.t*1000,self.DeltaPhase ,pen=pg.mkPen('b', width=1))
        self.PlotTemporalWidget.addItem(self.plotitem)

        self.PlotTemporalWidget.setLabel('bottom', 'Time [ms]', color='white', size=100)


    def update_temporal_Plot(self,arg=None):

        #pg.setConfigOptions(antialias=True)

        try:
            if os.path.isdir(self.current_json):
                self.current_json = self.current_json
        except:
            self.current_json = self.current_json[0]

        self.ffrjson.load_path(self.current_json)
        waveforms = self.ffrjson.load_AVG()
        sc_list = self.initSClist

        self.PlotTemporalWidget.clear()
        waveforms, scale_factor = sig.normalize_waveforms(waveforms)
        waveforms               = sig.order_waveforms(waveforms,sc_list)
        self.waveforms, DC      = sig.offset_waveforms(waveforms)


        _tmp ,fmax = self.roi_High_filter.pos()
        _tmp ,fmin = self.roi_Low_filter.pos()
        fmax = max([fmin,fmax])
        fmin = min([fmin,fmax])
        if fmin<=0: fmin=1
        fmax = (fmax)/(self.ffrjson.fs/2)
        fmin = (fmin)/(self.ffrjson.fs/2)
        print(fmin,fmax)


        if self.current_sc!=None and self.ComboFilterType.currentText()=='Auto':
            self.waveforms[self.current_sc] = self.ffrjson.filter_SC(self.waveforms[self.current_sc],self.current_sc)
        elif  self.current_sc!=None and self.ComboFilterType.currentText()=='Pass':

            b, a = signal.butter(4, [fmin,fmax], 'bandpass')
            self.waveforms[self.current_sc] = signal.filtfilt(b, a, self.waveforms[self.current_sc], padlen=150)
        elif  self.current_sc!=None and self.ComboFilterType.currentText()=='Stop':

            b, a = signal.butter(4, [fmin,fmax], 'bandstop')
            self.waveforms[self.current_sc] = signal.filtfilt(b, a, self.waveforms[self.current_sc], padlen=150)
        self.plotitem     = list()
        for sc in sc_list:
            if sc=="Stimulus":c='g'
            elif sc[0]=="R ": c='r'
            elif sc[0]=="C ": c='b'
            elif self.current_sc!=None and self.current_sc==sc: c = 'g'
            else: c='w'
            self.plotitem     = pg.PlotDataItem(self.ffrjson.t*1000,self.waveforms[sc],pen=pg.mkPen(c, width=1))
            self.PlotTemporalWidget.addItem(self.plotitem)
        self.PlotTemporalWidget.setLabel('bottom', 'Time [ms]', color='white', size=100)
        self.update_rois()




    def test_print(self):
        print('yes baby')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ComboName.setItemText(0, _translate("MainWindow", "John Doe"))
        self.ComboNumber.setItemText(0, _translate("MainWindow", "190001"))
        self.ComboEar.setItemText(0, _translate("MainWindow", "LE"))
        self.ComboEar.setItemText(1, _translate("MainWindow", "RE"))
        self.ComboLevel.setItemText(0, _translate("MainWindow", "85"))
        self.ComboStim.setItemText(0, _translate("MainWindow", "EFR220"))
        self.PatientLabel.setText(_translate("MainWindow", "               Patient"))
        self.ButtonAddFilter.setText(_translate("MainWindow", "+"))
        self.ButtonRemoveFilter.setText(_translate("MainWindow", "-"))
        self.ComboFilterType.setItemText(0, _translate("MainWindow", "Auto"))
        self.ComboFilterType.setItemText(1, _translate("MainWindow", "Pass"))
        self.ComboFilterType.setItemText(2, _translate("MainWindow", "Stop"))
        self.ButtonExport.setText(_translate("MainWindow", "Add to Workflow"))
        self.ButtonPrint.setText(_translate("MainWindow", "Print"))
        self.ButtonLatency.setText(_translate("MainWindow", "Latency"))
        self.ButtonFFT.setText(_translate("MainWindow", "Spectral"))
        self.ButtonAddControl.setText(_translate("MainWindow", "Add to Control"))
        self.ButtonFilter.setText(_translate("MainWindow", "Filter"))
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
        displayNames = list(dict.fromkeys(self.name))
        for idx in range(len(displayNames)):
            self.ComboName.setItemText(idx, _translate("MainWindow", displayNames[idx]))
        self.ComboName.setDuplicatesEnabled(False)

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
