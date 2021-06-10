import sys, json, copy, os, platform
import numpy as np
from scipy import signal
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QMessageBox
from os.path import split, join
from fnmatch import fnmatch
from tqdm import tqdm



SYSTEM = platform.system()





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
            if SYSTEM=='Windows':
                if len(split(rest)[0])==3:
                    out.append(split(rest)[1])
                    out.append(split(rest)[0][0:2])
                    break
                else:
                    out.append(split(rest)[1])
                    rest = split(rest)[0]
            else:
                if len(split(rest)[0])==1 or len(split(rest)[0])==2:
                    out.append(split(rest)[1])
                    break
                else:
                    out.append(split(rest)[1])
                    rest = split(rest)[0]
        out = out[::-1]
        for id,el in enumerate(out):
            outjson.update({str(id):el})
        return outjson

    def __join_path(self,dict_path):
        if SYSTEM=="Windows":
            outpath=''
            for id,value in enumerate(dict_path.values()):
                if id==0:continue
                else:
                    outpath = join(outpath,value)
            return join(dict_path["0"],os.sep,outpath)
        else:
            outpath=' '
            for id,value in enumerate(dict_path.values()):
                outpath = join(outpath,value)
            return outpath[1::]





    def select_db_path(self,flag=False):
        dbconfpathfile      = os.path.join(self.maingui.CONFDIR,'databasepath.json')

        if not os.path.exists(dbconfpathfile) or flag :
            destDir = QtGui.QFileDialog.getExistingDirectory(None,
                                                             'Open working directory',
                                                             ".",
                                                             QtGui.QFileDialog.ShowDirsOnly)
            out = {'databasepath':self.__split_path(destDir)}

            def popup_button(i):	self.button_text = i.text()
            msg = QMessageBox()
            msg.setWindowTitle("Action required")
            msg.setText("Save as default database path " + '\n' + destDir)
            # print(os.path.split(destDir))
            msg.setStandardButtons( QMessageBox.Save ) # seperate buttons with "|"
            msg.exec_()
            with open(os.path.join(self.maingui.CONFDIR,'databasepath.json'), 'w') as outfile:
                json.dump(out, outfile)

        with open(dbconfpathfile) as data_file:
            data = json.load(data_file)
            self.path_database = self.__join_path(data['databasepath'])
        print("self.path_database", self.path_database)
        # self.load()
        self.maingui.update_database_table()


    def get_value_from_metadata(self,metadata,field):
        value=None
        try:
            value = metadata["MetaData"]["Patient"][field]
        except Exception as e:
            # print('get_value_from_metadata',e)
            if field=='Oreille':
                try:
                    value = metadata["MetaData"]["Patient"][" Oreille"]
                except:
                    value = metadata["MetaData"]["Patient"]["Oreille "]
            elif field=='F1' or field=='F2' or field=="Level[dB]":
                value = str(metadata["MetaData"]["Stimulus"][field])
            else: value = ''
        return value

    def load(self):
        try:
            if self.path_database==None:
                self.select_db_path()
        except:pass
        self.database = {}
        pattern = "*.json"
        key=0
        for subpath, subdirs, files in tqdm(os.walk(self.path_database)):
            # print("ffr.py path = ",path)
            for filename in files:
                if fnmatch(filename, pattern) and 'Meta' in filename:
                    # print(os.path.join(subpath, filename))
                    try:
                        path2json = os.path.join(subpath, filename)
                        with open(path2json) as data_file:
                            data = json.load(data_file)
                        nom    = self.get_value_from_metadata(data,"Nom")
                        prenom = self.get_value_from_metadata(data,"Prenom")
                        number = self.get_value_from_metadata(data,"Number")
                        date   = self.get_value_from_metadata(data,"date string")
                        ear    = self.get_value_from_metadata(data,"Oreille")
                        level  = self.get_value_from_metadata(data,"Level[dB]")
                        year          = data["MetaData"]["date string"]
                        year          = year[len(year)-2:len(year)]
                        f1            = self.get_value_from_metadata(data,"F1")
                        f2            = self.get_value_from_metadata(data,"F2")
                        efr_frequency = str(round(int(f2)-int(f1)))

                        new={str(key):{'name'          : nom  + ' ' + prenom,
                                       'patient_number': year + number      ,
                                       'date'          : date               ,
                                       'frequency_efr' : efr_frequency      ,
                                       'stim'          : 'f1'+str(f1)+'f2'+str(f2),
                                       'f1'            : str(f1),
                                       'f2'            : str(f2),
                                       'ear'           : ear,
                                       'level'         : level,
                                       'code'          : ''.join([nom,' ',prenom,year+number,ear,level,'f1'+str(f1)+'f2'+str(f2) ]),
                                       'path2json'     : path2json
                                       }
                            }
                        self.database.update(new)
                        key+=1
                    except Exception as e:print("database load ERROR:", e)


    def load_AVG(self,json_data,ch,sc):
        waveform=json_data["FFR"][ch][sc]["AVG"]["Waveform"]
        # for id,x in enumerate(waveform):
        #     waveform[id]=float(x.replace(',','.'))
        return waveform

    def load_Analysis(self,json_data,ch,sc):
        analysis=json_data["FFR"][ch][sc]["Analysis"]
        # print("load_Analysis", analysis)
        return analysis







    def get_frequency(self,SCstring):
        metadata = self.get_metadata()
        f1       = float(metadata["Stimulus"]["F1"])
        f2       = float(metadata["Stimulus"]["F2"])

        f        = None
        if SCstring[0:2] == 'F1' :
            f = f1
        elif SCstring[0:2] == 'F2':
            f = f2
        elif SCstring[0:3] == 'EFR'    or fnmatch(SCstring, 'ENV') or SCstring[0:3]=='EFR':
            f = f2-f1
        elif SCstring[0:5] == 'EFR**'  or SCstring[0:4] == 'DENV'  or SCstring[0:5] == 'ENV**':
            f = 2*(f1-f2)
        elif SCstring[0:6] == 'EFR***' or SCstring[0:5] == 'DDENV' or SCstring[0:6] == 'ENV***':
            f = 3*(f1-f2)
        elif SCstring[0:3] == 'CDT':
            f = 2*f1-f2
        elif SCstring[0:4] == 'CDT*':
            f = 2*f2-f1
        elif SCstring[0:3] == 'ABR':
            f = 80
        else:
            print('SC string not valid')

        return f
