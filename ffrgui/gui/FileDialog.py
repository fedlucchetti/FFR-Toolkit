import sys, os, json
from PyQt5.QtWidgets import  QWidget,  QFileDialog, QMessageBox, QPushButton


class FileDialog(QWidget):

    def __init__(self,maingui):
        super().__init__()
        self.maingui=maingui
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.savePath=None

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog()
        #
        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", self.maingui.WORKDIR,"All Files (*);;JSON Files (*.txt)", options=options)
        if fileName:
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;JSON Files (*.json)", options=options)
        if files:
            return fileName

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save to",self.maingui.WORKDIR,\
                                                 "All Files (*);;JSON Files (*.json)",\
                                                  options=options)
        # self.show()
        if fileName:
            return fileName

    def showdialog(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Changes will be made to the data base")
        msg.setInformativeText("")
        msg.setWindowTitle("User action required")
        msg.setDetailedText(message)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        msg.setFixedSize(640, 480)

        retval = msg.exec_()
        print("value of pressed message box button:", retval)
        if retval==1024: return 1
        elif retval==4194304: return 0
        else: return 0

    def msgbtn(self,i):
        print("Button pressed is:",i.text())
