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
from ffrgui.gui       import PatientTable,SpectralWidget,TemporalWidget,LatencyPlotWidget, FileDialog
from ffrgui.utilities import Workspace,FFR_Utils,DataBase, Constants
from ffrgui.neuralnet import DeepFilter





class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.ROOTDIR = os.path.split(os.path.realpath(__file__))[0]
        self.CONFDIR = os.path.join(self.ROOTDIR,'conf')
        self.WORKDIR = os.path.join(self.ROOTDIR,'data','workspaces')
        print("self.ROOTDIR",self.ROOTDIR)
        self.roisdict=[]
        ##############################
        self.defaultScList = {'Channel-V':{'EFR':[],'CDT':[],'F1':[],'F2':[],'ABR':[]}, \
                              'Channel-H':{'EFR':[],'CDT':[],'F1':[],'F2':[],'ABR':[],} }
        self.initSClist    = ['EFR V','EFR H','F1 V','F1 H','F2 V','F2 H','CDT V','CDT H','ABR V','ABR H',]
        self.current_json  = None
        self.current_sc    = 'EFR V'
        self.current_id    = "1"
        ##############################
        self.const   = Constants.Constants()
        ##############################
        self.deepfilter = DeepFilter.DeepFilter(self)
        ##############################
        self.database  = DataBase.DataBase(self)
        self.database.load()
        ##############################
        self.workspace         = Workspace.Workspace(self)
        self.current_workspace = None
        ##############################
        # self.ffrutils   = FFR_Utils.FFR_Utils(self)
        # self.name,self.number,self.date,self.stim,self.ear,self.level,self.path2json, self.code = self.ffrutils.list_all()
        ##############################
        self.sig   = Signal.Signal(self)
        ##############################

        self.table = PatientTable.PatientTable(self)
        self.tableWidget = self.table.initUI()
        ##############################
        self.spectralWidget = SpectralWidget.SpectralWidget(self)
        self.roi_Filter     = self.spectralWidget.initUI()
        ###############################
        self.temporalWidget = TemporalWidget.TemporalWidget(self)
        ###############################
        self.latencyWidget = LatencyPlotWidget.LatencyPlotWidget(self)
        ###############################
        self.filedialog = FileDialog.FileDialog(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1794, 972)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)


        self.SelectPatientWidget = QtWidgets.QWidget(self.centralwidget)
        self.SelectPatientWidget.setGeometry(QtCore.QRect(300, 20, 1011, 81))
        self.SelectPatientWidget.setFont(font)
        self.SelectPatientWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.SelectPatientWidget.setObjectName("SelectPatientWidget")


        self.PatientDataWidget = QtWidgets.QWidget(self.centralwidget)
        self.PatientDataWidget.setGeometry(QtCore.QRect(10, 110, 281, 351))
        self.PatientDataWidget.setObjectName("PatientDataWidget")



        self.PatientView = QtWidgets.QListView(self.PatientDataWidget)
        self.PatientView.setGeometry(QtCore.QRect(10, 30, 251, 291))
        self.PatientView.setObjectName("PatientView")


        self.ButtonWidget = QtWidgets.QWidget(self.centralwidget)
        self.ButtonWidget.setGeometry(QtCore.QRect(10, 510, 271, 371))
        self.ButtonWidget.setObjectName("ButtonWidget")




        self.ButtonOpenDataBase = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonOpenDataBase.setGeometry(QtCore.QRect(30, 10, 221, 51))
        self.ButtonOpenDataBase.setFont(font)
        self.ButtonOpenDataBase.setObjectName("Open")





        self.ButtonFFT = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonFFT.setGeometry(QtCore.QRect(30, 100, 221, 51))
        self.ButtonFFT.setFont(font)
        self.ButtonFFT.setObjectName("ButtonFFT")
        self.ButtonAnalysis = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonAnalysis.setGeometry(QtCore.QRect(30, 170, 221, 51))
        self.ButtonAnalysis.setFont(font)
        self.ButtonAnalysis.setObjectName("ButtonAnalysis")

        self.ButtonRefresh = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonRefresh.setGeometry(QtCore.QRect(30, 240, 221, 51))
        self.ButtonRefresh.setFont(font)
        self.ButtonRefresh.setObjectName("ButtonRefresh")

        self.ButtonCommit = QtWidgets.QPushButton(self.ButtonWidget)
        self.ButtonCommit.setGeometry(QtCore.QRect(30, 310, 221, 51))
        self.ButtonCommit.setFont(font)
        self.ButtonCommit.setObjectName("ButtonCommit")

        self.TemporalWidgetContainer = QtWidgets.QWidget(self.centralwidget)
        self.TemporalWidgetContainer.setGeometry(QtCore.QRect(300, 110, 1481, 1200))
        self.TemporalWidgetContainer.setObjectName("TemporalWidgetContainer")

        self.temporalWidget.initUI()








        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1794, 27))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuWorkspace = QtWidgets.QMenu(self.menubar)
        self.menuWorkspace.setObjectName("menuWorkspace")

        self.menuDatabase = QtWidgets.QMenu(self.menubar)
        self.menuDatabase.setObjectName("menuDatabase")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.actionOpen_Workspace = QtWidgets.QAction(MainWindow)
        self.actionOpen_Workspace.setObjectName("actionOpen_Workspace")


        self.actionSet_DatabasePath = QtWidgets.QAction(MainWindow)
        self.actionSet_DatabasePath.setObjectName("actionSet_DatabasePath")

        self.actionSave_Workspace = QtWidgets.QAction(MainWindow)
        self.actionSave_Workspace.setObjectName("actionSave_Workspace")


        self.menuFile.addSeparator()


        self.menuWorkspace.addAction(self.actionOpen_Workspace)
        self.menuWorkspace.addAction(self.actionSave_Workspace)

        self.menuDatabase.addAction(self.actionSet_DatabasePath)


        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuWorkspace.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())

        self.actions()


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def actions(self):
        self.ButtonOpenDataBase.clicked.connect(lambda : self.update_database_table())
        self.ButtonRefresh.clicked.connect(lambda : self.update_temporal_plot())
        self.ButtonCommit.clicked.connect(lambda : self.workspace.commit())
        self.table.tableWidget.clicked.connect( lambda : self.update_temporal_plot())

        self.ButtonRefresh.clicked.connect(lambda: self.workspace.init_workspace())

        self.ButtonFFT.clicked.connect(lambda: self.spectralWidget.initUI('load'))
        self.ButtonAnalysis.clicked.connect(lambda: self.latencyWidget.initUI('load'))

        self.actionOpen_Workspace.triggered.connect(lambda: self.workspace.load())
        self.actionSave_Workspace.triggered.connect(lambda: self.workspace.save())

        self.actionSet_DatabasePath.triggered.connect(lambda: self.database.select_db_path(True))
        # self.actionOpen_Workspace.clicked.connect(               lambda: self.workspace.load()                        )
        # self.actionSave_Workspace.clicked.connect(               lambda: self.workspace.save()                        )


    def update_plots(self):
        self.spectralWidget.initUI('load')

    def update_database_table(self):
        self.table.updateTable()

    def update_temporal_plot(self):
        self.temporalWidget.update()
        self.latencyWidget.update()











    def test_print(self):
        print('test_print')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


        self.ButtonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.ButtonOpenDataBase.setText(_translate("MainWindow", "Open Database"))
        self.ButtonAnalysis.setText(_translate("MainWindow", "Analysis"))
        self.ButtonFFT.setText(_translate("MainWindow", "Spectral"))
        self.ButtonCommit.setText(_translate("MainWindow", "Commit"))


        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuWorkspace.setTitle(_translate("MainWindow", "Workspace"))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database"))


        self.actionSet_DatabasePath.setText(_translate("MainWindow", "Set path"))

        self.actionOpen_Workspace.setText(_translate("MainWindow", "Open"))
        self.actionSave_Workspace.setText(_translate("MainWindow", "Save"))


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
