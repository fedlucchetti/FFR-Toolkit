import sys, json, copy, os
import numpy as np
from scipy import signal
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QMessageBox
from os.path import split, join









class DataBase(object):
    def __init__(self,maingui):
        self.maingui    = maingui
        self.initwaveforms = {'Channel-V':{'EFR':[],'EFR**':[],'EFR***':[],'CDT':[],'CDT*':[],'F1':[],'F2':[],'ABR':[],'Noise':[]},\
                     'Channel-H':{'EFR':[],'EFR**':[],'EFR***':[],'CDT':[],'CDT*':[],'F1':[],'F2':[],'ABR':[],'Noise':[]} }
        self.path = None
        self.path_database = None

    def load_AVGs(self,waveforms=None):

        if waveforms == None:waveforms = self.initwaveforms
        #if json_path == None: json_path = self.path
        json_path = self.path
        print('FFR.py load JSON path: ',json_path)
        sc_list = []
        with open(json_path) as data_file: data = json.load(data_file)

        for channel in data["FFR"]:
            for sc_string in data["FFR"][channel]:
                waveforms[channel][sc_string]= 10**-2 * np.array(data["FFR"][channel][sc_string]["AVG"]["Waveform"])
                sc_list.append(sc_string+" "+channel[-1])
        return waveforms, sc_list

    def get_metadata(self):
        with open(self.path) as data_file:
            data = json.load(data_file)
        return data["MetaData"]

    def get_channel_sc(self,label):
        channel = 'Channel-' + label[len(label)-1]
        sc = label[len(label)-3::-1]
        sc = sc[::-1]
        return channel, sc

    def __split_path(self,path):
        rest=path
        out,outjson=[],{}
        while True:
            if len(split(rest)[0])==1:break
            else:
                out.append(split(rest)[1])
                rest = split(rest)[0]
        out.append(split(rest)[1])
        out = out[::-1]
        for id,el in enumerate(out):
            outjson.update({str(id):el})
        return outjson

    def __join_path(self,dict_path):
        outpath=' '
        for value in dict_path.values():
            outpath = join(outpath,value)
        return outpath[1::]




    def select_db_path(self,flag):
        dbconfpathfile      = os.path.join(self.maingui.CONFDIR,'databasepath.json')
        if not flag:
            pass
        else :
            destDir = QtGui.QFileDialog.getExistingDirectory(None,
                                                             'Open working directory',
                                                             ".",
                                                             QtGui.QFileDialog.ShowDirsOnly)
            out = {'databasepath':self.__split_path(destDir)}

            def popup_button(i):	self.button_text = i.text()
            msg = QMessageBox()
            msg.setWindowTitle("Action required")
            msg.setText("Save as default database path " + '\n' + destDir)
            print(os.path.split(destDir))
            msg.setStandardButtons( QMessageBox.Save ) # seperate buttons with "|"
            msg.exec_()
            with open(os.path.join(self.maingui.CONFDIR,'databasepath.json'), 'w') as outfile:
                json.dump(out, outfile)

        with open(dbconfpathfile) as data_file:
            data = json.load(data_file)
            self.path_database = self.__join_path(data['databasepath'])
