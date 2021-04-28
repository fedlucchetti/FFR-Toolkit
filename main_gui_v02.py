# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QPen
from ffrgui.utilities import FFRJSON
import numpy as np
import re
import  os
dir_path = os.path.dirname(os.path.realpath(__file__))

#from pyqtgraph import PlotWidget, plot, mkPen, RectROI, PlotDataItem
import pyqtgraph as pg
from pyqtgraph import plot, GraphicsWindow

class Ui_MainWindow(object):
    def __init__(self):
        self.ffrjson = FFRJSON.FFRJSON()

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

        self.initpath = '/media/ergonium/KINGSTON/AnalyseFFR_LV/Patients&Subjects/NewNH20172018/170392/Harmonique_RE/85dB/Meta_AVG_data.json'
        self.rois         = []

        self.highpass = 4000
        self.lowpass  = 50

    def test(string):
        print(string)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1789, 895)
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
        self.ComboName = QtWidgets.QComboBox(self.SelectPatientWidget)
        self.ComboName.setGeometry(QtCore.QRect(20, 20, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setItalic(True)
        self.ComboName.setFont(font)
        self.ComboName.setObjectName("ComboName")
        self.ComboName.addItem("")
        self.ComboNumber = QtWidgets.QComboBox(self.SelectPatientWidget)
        self.ComboNumber.setGeometry(QtCore.QRect(400, 20, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setItalic(True)
        self.ComboNumber.setFont(font)
        self.ComboNumber.setObjectName("ComboNumber")
        self.ComboNumber.addItem("")
        self.ComboEar = QtWidgets.QComboBox(self.SelectPatientWidget)
        self.ComboEar.setGeometry(QtCore.QRect(550, 20, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setItalic(True)
        self.ComboEar.setFont(font)
        self.ComboEar.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.ComboEar.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.ComboEar.setObjectName("ComboEar")
        self.ComboEar.addItem("")
        self.ComboEar.addItem("")
        self.ComboLevel = QtWidgets.QComboBox(self.SelectPatientWidget)
        self.ComboLevel.setGeometry(QtCore.QRect(630, 20, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setItalic(True)
        self.ComboLevel.setFont(font)
        self.ComboLevel.setObjectName("ComboLevel")
        self.ComboLevel.addItem("")
        self.ComboStim = QtWidgets.QComboBox(self.SelectPatientWidget)
        self.ComboStim.setGeometry(QtCore.QRect(730, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        font.setItalic(True)
        self.ComboStim.setFont(font)
        self.ComboStim.setObjectName("ComboStim")
        self.ComboStim.addItem("")
        self.PatientDataWidget = QtWidgets.QWidget(self.centralwidget)
        self.PatientDataWidget.setGeometry(QtCore.QRect(10, 120, 271, 341))
        self.PatientDataWidget.setObjectName("PatientDataWidget")
        self.PatientView = QtWidgets.QListView(self.PatientDataWidget)
        self.PatientView.setGeometry(QtCore.QRect(10, 40, 241, 291))
        self.PatientView.setObjectName("PatientView")
        self.PatientLabel = QtWidgets.QLabel(self.PatientDataWidget)
        self.PatientLabel.setGeometry(QtCore.QRect(80, 10, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PatientLabel.setFont(font)
        self.PatientLabel.setObjectName("PatientLabel")





        self.PlotTemporalWidget = pg.PlotWidget(self.centralwidget)
        self.PlotTemporalWidget.setGeometry(QtCore.QRect(300, 120, 1011, 661))
        self.PlotTemporalWidget.setObjectName("PlotTemporalWidget")





        self.WidgetFilter = QtWidgets.QWidget(self.centralwidget)
        self.WidgetFilter.setGeometry(QtCore.QRect(1320, 120, 451, 461))
        self.WidgetFilter.setObjectName("WidgetFilter")
        self.ButtonFilter = QtWidgets.QPushButton(self.WidgetFilter)
        self.ButtonFilter.setGeometry(QtCore.QRect(160, 10, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonFilter.setFont(font)
        self.ButtonFilter.setObjectName("ButtonFilter")
        self.PlotSpectralWidget = pg.PlotWidget(self.WidgetFilter)
        self.PlotSpectralWidget.setGeometry(QtCore.QRect(80, 70, 361, 261))
        self.PlotSpectralWidget.setObjectName("PlotSpectralWidget")
        self.SliderHighpass = QtWidgets.QSlider(self.WidgetFilter)
        self.SliderHighpass.setGeometry(QtCore.QRect(80, 350, 361, 41))
        self.SliderHighpass.setOrientation(QtCore.Qt.Horizontal)
        self.SliderHighpass.setObjectName("SliderHighpass")
        self.SliderLowpass = QtWidgets.QSlider(self.WidgetFilter)
        self.SliderLowpass.setGeometry(QtCore.QRect(80, 400, 361, 41))
        self.SliderLowpass.setOrientation(QtCore.Qt.Horizontal)
        self.SliderLowpass.setObjectName("SliderLowpass")
        self.LabelHigh = QtWidgets.QLabel(self.WidgetFilter)
        self.LabelHigh.setGeometry(QtCore.QRect(11, 360, 52, 28))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.LabelHigh.setFont(font)
        self.LabelHigh.setObjectName("LabelHigh")
        self.LabelLow = QtWidgets.QLabel(self.WidgetFilter)
        self.LabelLow.setGeometry(QtCore.QRect(11, 410, 47, 28))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.LabelLow.setFont(font)
        self.LabelLow.setObjectName("LabelLow")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(10, 470, 271, 311))
        self.widget_2.setObjectName("widget_2")
        self.ButtonExport = QtWidgets.QPushButton(self.widget_2)
        self.ButtonExport.setGeometry(QtCore.QRect(30, 10, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonExport.setFont(font)
        self.ButtonExport.setObjectName("ButtonExport")
        self.ButtonPrint = QtWidgets.QPushButton(self.widget_2)
        self.ButtonPrint.setGeometry(QtCore.QRect(30, 70, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonPrint.setFont(font)
        self.ButtonPrint.setObjectName("ButtonPrint")
        self.ButtonAnalyze = QtWidgets.QPushButton(self.widget_2)
        self.ButtonAnalyze.setGeometry(QtCore.QRect(30, 190, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonAnalyze.setFont(font)
        self.ButtonAnalyze.setObjectName("ButtonAnalyze")
        self.ButtonFFT = QtWidgets.QPushButton(self.widget_2)
        self.ButtonFFT.setGeometry(QtCore.QRect(30, 130, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonFFT.setFont(font)
        self.ButtonFFT.setObjectName("ButtonFFT")
        self.ButtonAddControl = QtWidgets.QPushButton(self.widget_2)
        self.ButtonAddControl.setGeometry(QtCore.QRect(30, 250, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ButtonAddControl.setFont(font)
        self.ButtonAddControl.setObjectName("ButtonAddControl")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1789, 27))
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
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())


        # allocate space in qcombo boxes



        #self.init_slider

        self.populate_combos()
        self.actions()
        self.init_slider()
        self.SliderHighpass.sliderPressed.connect(self.get_slider_values)
        self.SliderLowpass.sliderPressed.connect(self.get_slider_values)
        print(self.highpass,self.lowpass)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_slider(self):
        self.SliderHighpass.setMaximum(5000)
        self.SliderHighpass.setMinimum(1)
        self.SliderLowpass.setMaximum(5000)
        self.SliderLowpass.setMinimum(1)
        self.SliderHighpass.setValue(self.highpass)
        self.SliderLowpass.setValue(self.lowpass)

    def get_slider_values(self):
        #get slider max_values
        self.highpass = self.SliderHighpass.value()
        self.lowpass = self.SliderLowpass.value()
        return self.highpass, self.lowpass

    def populate_combos(self):
        for idx in range(len(self.name)):self.ComboName.addItem("")
        for idx in range(5):self.ComboNumber.addItem("")
        for idx in range(2):self.ComboEar.addItem("")
        for idx in range(5):self.ComboLevel.addItem("")
        for idx in range(10):self.ComboStim.addItem("")


    def actions(self):
        print('actions')
        # define action
        self.ComboName.activated['QString'].connect(  lambda : self.update_all_combo('name')             )
        self.ComboNumber.activated['QString'].connect(lambda : self.update_all_combo('number')           )
        self.ComboEar.activated['QString'].connect(   lambda : self.update_all_combo('ear')              )
        self.ComboLevel.activated['QString'].connect( lambda : self.update_all_combo('level')            )
        self.ComboStim.activated['QString'].connect(  lambda : self.update_all_combo('stim')             )
        self.ComboStim.activated['QString'].connect(  lambda : self.update_temporal_Plot                 )
        self.ButtonExport.clicked.connect(            lambda : self.update_temporal_Plot(self.initpath)  )


    def update_all_combo(self,combo):
        if self.ComboName.currentText()!="":

            print('current name = ',self.ComboName.currentText())
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

            if   len(open_json_path) > 1 and open_json_path!=None :return self.update_temporal_Plot(open_json_path[0])
            elif len(open_json_path) ==1 and open_json_path!=None :return self.update_temporal_Plot(open_json_path)
            else: pass

    def normalize_waveforms(self,waveforms):
        channels = list()
        n_sc     = 0
        max_values = list()
        for idc in waveforms.keys():
            channels.append(idc)
            for ids in waveforms[idc]:
                max_values.append(np.max(waveforms[idc][ids]))
        scale_factor = np.max(max_values)
        for idc in waveforms.keys():
            for ids in waveforms[idc]:
                waveforms[idc][ids] = waveforms[idc][ids]/scale_factor

        return waveforms, scale_factor

    def get_channel_sc(self,label):
        channel = 'Channel-' + idl[len(idl)-1]
        sc = idl[len(idl)-3::-1]
        sc = sc[::-1]
        return channel, sc

    def get_label(self,channel,sc):
        return sc + ' ' + channel[len(channel)-1]

    def select_waveforms(self,waveforms,label):
        sel_waveforms = {'init':[]}
        for idl in label:
            _wave = {idl:np.zeros(self.ffrjson.Nt)}
            sel_waveforms.update(_wave)

        for channel in waveforms.keys():
            for sc in waveforms[channel]:
                _label = self.get_label(channel,sc)
                try:
                    if str(label.index(_label)).isnumeric:
                        _wave = {_label:waveforms[channel][sc]}
                        sel_waveforms.update(_wave)

                except: pass
        del sel_waveforms['init']
        return sel_waveforms

    def offset_waveforms(self,waveforms):

        nSC              = len(waveforms.keys())
        DC               = np.array(np.zeros(nSC))
        sc_list          = waveforms.keys()
        _waveforms       = np.array(np.zeros([self.ffrjson.Nt,nSC]))
        offset_waveforms = sel_waveforms = {'init':[]}
        idx        = 0
        for label in waveforms.keys():
            try:_waveforms[:,idx] = waveforms[label]
            except: pass
            idx+=1
        for ids in range(nSC-1):
            DC[ids+1]  = DC[ids]   + np.abs(np.min(_waveforms[:,ids])-np.mean(_waveforms[:,ids])) + np.abs(np.max(_waveforms[:,ids+1])-np.mean(_waveforms[:,ids+1]))
            _waveforms[:,ids+1] = _waveforms[:,ids+1]-DC[ids+1]
        ids = 0
        for label in waveforms.keys():
            #waveforms[label] = _waveforms[:,ids]
            offset_waveforms.update({label:_waveforms[:,ids]})
            ids+=1
        del offset_waveforms['init']

        return offset_waveforms, DC

    def update_rois(self,waveforms):

        roi_width = np.max(self.ffrjson.t*1000)
        for sc in waveforms.keys():
            roi_y_pos = np.min(waveforms[sc])
            roi_height = np.abs(np.max(waveforms[sc])-np.min(waveforms[sc]))
            self.rois.append(pg.RectROI([0,roi_y_pos], [roi_width, roi_height],pen=QPen(QColor(255, 0, 0,0))))

        for roi in self.rois:
            roi.sigHoverEvent.connect(self.test_print)
            roi.sigRegionChanged.connect(lambda: print('hovered over roi'))
            self.PlotTemporalWidget.addItem(roi)


    def update_temporal_Plot(self,open_json_path):

        #pg.setConfigOptions(antialias=True)

        try:
            if os.path.isdir(open_json_path):
                open_json_path = open_json_path
        except:
            open_json_path = open_json_path[0]

        self.ffrjson.load_path(open_json_path)
        waveforms = self.ffrjson.load_AVG()
        sc_list = self.initSClist

        self.PlotTemporalWidget.clear()
        waveforms, scale_factor = self.normalize_waveforms(waveforms)
        waveforms               = self.select_waveforms(waveforms,sc_list)
        waveforms, DC           = self.offset_waveforms(waveforms)

        self.plotitem     = list()
        for sc in sc_list:
            if sc=="Stimulus":c='g'
            elif sc[0]=="R ": c='r'
            elif sc[0]=="C ": c='b'
            else: c='w'
            self.plotitem     = pg.PlotDataItem(self.ffrjson.t*1000,waveforms[sc],pen=pg.mkPen(c, width=1))
            self.PlotTemporalWidget.addItem(self.plotitem)
        self.PlotTemporalWidget.setLabel('bottom', 'Time [ms]', color='white', size=100)
        self.update_rois(waveforms)

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
        self.PatientLabel.setText(_translate("MainWindow", "Patient"))
        self.ButtonFilter.setText(_translate("MainWindow", "Filter"))
        self.LabelHigh.setText(_translate("MainWindow", "High"))
        self.LabelLow.setText(_translate("MainWindow", "Low"))
        self.ButtonExport.setText(_translate("MainWindow", "Export Waveforms"))
        self.ButtonPrint.setText(_translate("MainWindow", "Print"))
        self.ButtonAnalyze.setText(_translate("MainWindow", "T-F Analyze"))
        self.ButtonFFT.setText(_translate("MainWindow", "FFT"))
        self.ButtonAddControl.setText(_translate("MainWindow", "Add to Control"))
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

        displayNames = list(dict.fromkeys(self.name))
        for idx in range(len(displayNames)):
            self.ComboName.setItemText(idx, _translate("MainWindow", displayNames[idx]))
        self.ComboName.setDuplicatesEnabled(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
