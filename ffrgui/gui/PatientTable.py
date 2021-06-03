import sys, os, json
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from PyQt5 import  QtGui

from PyQt5.QtCore import pyqtSlot


class PatientTable(QWidget):

    def __init__(self,maingui):
        super().__init__()
        # self.ffrjson = ffr
        # print("PatientTable: ",self.ffrjson)
        self.maingui   = maingui
        self.workspace = maingui.workspace
        self.database  = maingui.database
        self.__title = ''
        self.__left = 0
        self.__top = 0
        self.__width = 800
        self.__height = 1000
        self.__header = ["Number","Name","Ear","Level","EFR [Hz]","F1 [Hz]","F2 [Hz]"]


        # self.initUI()

    def initUI(self):
        #
        self.setWindowTitle(self.__title)
        self.setGeometry(self.__left, self.__top, self.__width, self.__height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        return self.tableWidget

    def showTable(self):
        self.show()

    def test(self):
        print("test")

    def onHeaderClicked(self, logicalIndex):
        header = self.__header[logicalIndex]
        print("onHeaderClicked: ", header, logicalIndex)
        self.tableWidget.sortItems(logicalIndex)
        # if header=="Number":
        #     idx = np.argsort(np.array(self.maingui.number).astype("int")).astype("int")
        #     print(idx)
        # self.maingui.number = self.maingui.number[idx]
        # self.maingui.name   = self.maingui.name[idx]
        # self.maingui.ear    = self.maingui.ear[idx]
        # self.maingui.level  = self.maingui.level[idx]
        # self.maingui.stim   = self.maingui.stim[idx]
        # self.updateTable()

    def updateTable(self):
        for row in range(self.Nrows):
            self.tableWidget.setItem(row,0, QTableWidgetItem(str(self.database.database[str(row)]['patient_number'])))
            self.tableWidget.setItem(row,1, QTableWidgetItem(str(self.database.database[str(row)]['name'])))
            self.tableWidget.setItem(row,2, QTableWidgetItem(str(self.database.database[str(row)]['ear'])))
            self.tableWidget.setItem(row,3, QTableWidgetItem(str(self.database.database[str(row)]['level'])))
            self.tableWidget.setItem(row,4, QTableWidgetItem(str(self.database.database[str(row)]['frequency_efr'])))
            self.tableWidget.setItem(row,5, QTableWidgetItem(str(self.database.database[str(row)]['f1'])))
            self.tableWidget.setItem(row,6, QTableWidgetItem(str(self.database.database[str(row)]['f2'])))
        self.tableWidget.move(0,0)





    def createTable(self):
       # Create table

        self.Nrows    = len(self.database.database)
        self.Ncolumns = 7
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.Nrows)
        self.tableWidget.setColumnCount(self.Ncolumns)
        self.tableWidget.setHorizontalHeaderLabels(self.__header)
        for col,item in enumerate(self.__header):
            item=QTableWidgetItem(str(item))
            self.tableWidget.setHorizontalHeaderItem(col,item)
            # self.tableWidget.itemClicked(item)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)
        for row in range(self.Nrows):
            self.tableWidget.setItem(row,0, QTableWidgetItem(str(self.database.database[str(row)]['patient_number'])))
            self.tableWidget.setItem(row,1, QTableWidgetItem(str(self.database.database[str(row)]['name'])))
            self.tableWidget.setItem(row,2, QTableWidgetItem(str(self.database.database[str(row)]['ear'])))
            self.tableWidget.setItem(row,3, QTableWidgetItem(str(self.database.database[str(row)]['level'])))
            self.tableWidget.setItem(row,4, QTableWidgetItem(str(self.database.database[str(row)]['frequency_efr'])))
            self.tableWidget.setItem(row,5, QTableWidgetItem(str(self.database.database[str(row)]['f1'])))
            self.tableWidget.setItem(row,6, QTableWidgetItem(str(self.database.database[str(row)]['f2'])))
        self.tableWidget.move(0,0)
        # table selection change
        self.tableWidget.clicked.connect(self.on_click)
        self.tableWidget.clicked.connect(self.workspace.init_workspace)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.maingui.current_json = self.database.database[str(currentQTableWidgetItem.row())]['path2json']
            print("table:  ",currentQTableWidgetItem.row())




# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())
