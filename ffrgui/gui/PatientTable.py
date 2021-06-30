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
        self.maingui   = maingui
        self.workspace = maingui.workspace
        self.database  = maingui.database
        self.__title = ''
        self.__left = 0
        self.__top = 0
        self.__width = 800
        self.__height = 1000
        self.__header = ["Number","Name","Ear","Level","EFR [Hz]","F1 [Hz]","F2 [Hz]"]
        self.__order  = np.ones(len(self.__header))

    def initUI(self):
        #
        self.setWindowTitle(self.__title)
        self.setGeometry(self.__left, self.__top, self.__width, self.__height)
        self.createTable()
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
        self.__order[logicalIndex] = (self.__order[logicalIndex]+1)%2
        self.tableWidget.sortItems(logicalIndex,int(self.__order[logicalIndex]))

    def updateTable(self):
        self.database.load()
        self.populate()
        self.tableWidget.move(0,0)
        self.show()

    def populate(self):
        self.tableWidget.setRowCount(len(self.database.database))
        self.tableWidget.setColumnCount(self.Ncolumns)
        self.tableWidget.setHorizontalHeaderLabels(self.__header)
        for col,item in enumerate(self.__header):
            item=QTableWidgetItem(str(item))
            self.tableWidget.setHorizontalHeaderItem(col,item)
        for row in range(len(self.database.database)):
            self.tableWidget.setItem(row,0, QTableWidgetItem(str(self.database.database[str(row)]['patient_number'])))
            self.tableWidget.setItem(row,1, QTableWidgetItem(str(self.database.database[str(row)]['name'])))
            self.tableWidget.setItem(row,2, QTableWidgetItem(str(self.database.database[str(row)]['ear'])))
            self.tableWidget.setItem(row,3, QTableWidgetItem(str(self.database.database[str(row)]['level'])))
            self.tableWidget.setItem(row,4, QTableWidgetItem(str(self.database.database[str(row)]['frequency_efr'])))
            self.tableWidget.setItem(row,5, QTableWidgetItem(str(self.database.database[str(row)]['f1'])))
            self.tableWidget.setItem(row,6, QTableWidgetItem(str(self.database.database[str(row)]['f2'])))
            self.tableWidget.setItem(row,7, QTableWidgetItem(str(self.database.database[str(row)]['path2json'])))
        self.tableWidget.setColumnHidden(7,True)


    def createTable(self):
       # Create table

        self.Nrows    = len(self.database.database)
        self.Ncolumns = 8
        self.tableWidget = QTableWidget()
        self.populate()
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)
        self.tableWidget.move(0,0)
        self.tableWidget.clicked.connect(self.on_click)
        self.tableWidget.clicked.connect(self.workspace.init_workspace)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.maingui.current_json = self.tableWidget.item(currentQTableWidgetItem.row(),7).text()
            self.maingui.current_code = self.database.database[str(currentQTableWidgetItem.row())]['code']
            print("on_click: ",self.database.database[str(currentQTableWidgetItem.row())]['code'])




# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())
