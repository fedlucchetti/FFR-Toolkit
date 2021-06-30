
# -*- coding: utf-8 -*-
import sys, json, copy, os
import numpy as np
from scipy import signal
from PyQt5.QtWidgets import  QFileDialog
from ffrgui.gui       import FileDialog
from collections.abc import Mapping




class Workspace(object):
    def __init__(self,maingui):
        self.maingui   = maingui
        self.database  = maingui.database
        self.const     = maingui.const
        self.current_workspace = {}
        self.onset,self.offset=0,0
        # self.database.load()

    def init_workspace(self):

        print("init_current_workspace from", self.maingui.current_json)
        self.clear()
        self.database.path = self.maingui.current_json
        with open(self.maingui.current_json) as data_file: json_data = json.load(data_file)
        self.waveform_list, self.sc_label_list    = self.database.load_AVGs()
        metadata = self.database.get_metadata()
        id=0
        for i, label in enumerate(self.sc_label_list):
            if "Noise" in label or "*" in label: continue
            ch,sc = self.database.get_channel_sc(label)
            label.replace(" ", "")
            # print("id ",i," ch:",ch,"  sc",sc)
            newentry = {str(id):{"MetaData":metadata,
                           "SC":label,
                           "Data":{"original":
                                        {"waveform":list(copy.deepcopy(self.database.load_AVG(json_data,ch,sc))),
                                         "analysis":copy.deepcopy(self.database.load_Analysis(json_data,ch,sc)),
                                         "gui":{"ymax":np.max(np.abs(np.fft.fft(self.database.load_AVG(json_data,ch,sc))))}},
                                   "filtered":
                                        {"waveform":list(copy.deepcopy(self.database.load_AVG(json_data,ch,sc))),
                                         "analysis":copy.deepcopy(self.database.load_Analysis(json_data,ch,sc))},
                                   "noise"   :list(copy.deepcopy(copy.deepcopy(self.database.load_AVG(json_data,ch,"Noise"))))
                                   },
                           "Filters":{'42':{'state':{'pos':(0.0,0.0),'size':(0.0,0.0),'angle':(0.0)},'type':'autoencoder','enable':0}}
                           }
                        }

            self.current_workspace.update(newentry)
            id+=1
        self.maingui.update_temporal_plot()
        # self.save()




    def get_waveform(self,id,flag='original'):
        # print("get_waveform: all id ", self.current_workspace.keys())
        # print("get_waveform: id", id)
        signal = np.array(self.current_workspace[id]["Data"][flag]["waveform"]).astype("float")
        noise  = np.array(self.current_workspace[id]["Data"]["noise"]).astype("float")
        return signal, noise

    def set_waveform(self,id,waveform):
        self.current_workspace[id]["Data"]["filtered"]["waveform"] = list(waveform)

    def get_sc_spectral(self,flag='original'):
        # print("ffr.py: current_json ",self.maingui.current_json)
        # print("ffr.py: current sc   ",self.maingui.current_sc)

        sig_waveform, noise_waveform = self.get_waveform(self.maingui.current_id,flag)
        sig_waveform   = np.absolute(np.fft.fft(sig_waveform))

        noise_waveform = np.absolute(np.fft.fft(noise_waveform))
        return sig_waveform[0:self.const.Nf], noise_waveform[0:self.const.Nf]


    def get_filters(self):
        try:
            return self.current_workspace[self.maingui.current_id]["Filters"]
        except: return {}

    def set_on_offset(self):
        # print("set_on_offset",self.onset,self.offset)
        self.current_workspace[self.maingui.current_id]["Data"]["original"]["analysis"]["Latency"] = self.onset
        self.current_workspace[self.maingui.current_id]["Data"]["original"]["analysis"]["Lenght"] = self.offset-self.onset

    def get_on_offset(self,id):
        id=str(id)
        _x = self.current_workspace[id]["Data"]["original"]["analysis"]["Latency"]
        try:
            if isinstance(_x, str):
                onset=float(_x.replace(',','.'))
            else: onset =  _x
        except Exception as e:
            # print("get_on_offset: first",e,"  _x",_x)
            onset=-1
        _x = self.current_workspace[id]["Data"]["original"]["analysis"]["Lenght"]
        try:
            if isinstance(_x, str):
                offset = onset + float(_x.replace(',','.'))
            else: offset = onset + _x
        except Exception as e:
            # print("get_on_offset: second",e,"  _x",_x)
            offset = -1


        if onset < 5:
            return -1,-1
        else:
            return onset, offset


    def load_AVGs(self):
        sc_list = []
        waveforms = np.zeros( [self.const.Nt,len(self.current_workspace)] )
        for id, entry in enumerate(self.current_workspace):
            label             = self.current_workspace[entry]["SC"]
            channel,sc_string = self.database.get_channel_sc(label)
            waveforms[:,id],_   = self.get_waveform(entry,flag='filtered')
            sc_list.append(sc_string+" "+channel[-1])
        return waveforms, sc_list

    def add(self):
        pass

    def delete(self):
        pass

    def clear(self):
        self.current_workspace={}

    def list(self):
        pass

    def commit(self):
        self.filedialog = self.maingui.filedialog
        message = "\n"
        with open(self.maingui.current_json) as data_file: json_data = json.load(data_file)
        for id, entry in enumerate(self.current_workspace):
            label             = self.current_workspace[entry]["SC"]
            channel,sc_string = self.database.get_channel_sc(label)
            on,off = self.get_on_offset(id)
            # print("Replace in MetaAVG: ",json_data["FFR"][channel][sc_string]["Analysis"]["Latency"],"---->",str(on) )
            # print("Replace in MetaAVG: ",json_data["FFR"][channel][sc_string]["Analysis"]["Lenght"],"---->",str(off-on) )
            message = message + sc_string+" "+channel+"\n"
            message = message + " onset :  " + str(json_data["FFR"][channel][sc_string]["Analysis"]["Latency"]) + "---->"+str(on)+"\n"
            message = message +   " length:  " + str(json_data["FFR"][channel][sc_string]["Analysis"]["Lenght"]) + "---->" +str(off-on) +"\n"+"\n"
            json_data["FFR"][channel][sc_string]["Analysis"]["Latency"]= on
            json_data["FFR"][channel][sc_string]["Analysis"]["Lenght"] = off-on
        out=self.filedialog.showdialog(message)
        if out:
            with open(self.maingui.current_json, 'w') as outfile:
                json.dump(json_data, outfile,ensure_ascii=False)
            print("Changes written to file", self.maingui.current_json)




    def save(self):
        outjson = self.__serialize(self.current_workspace)
        self.filedialog = self.maingui.filedialog
        filename = self.filedialog.saveFileDialog()
        if filename != False:
            with open(filename, 'w') as outfile:
                json.dump(outjson, outfile)



    def load(self):
        self.filedialog = self.maingui.filedialog
        filename = self.filedialog.openFileNameDialog()
        with open(filename, 'r') as outfile:
            self.current_workspace = self.__deserialize(json.load(outfile))
        self.maingui.update_temporal_plot()

    def __deserialize(self,datajson):
        return {k:v for k,v in datajson.items()}

    def __serialize(self,datajson):
        return {str(k):v for k,v in datajson.items()}
