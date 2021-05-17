
# -*- coding: utf-8 -*-
import sys, json
import numpy as np
from scipy import signal


class Workspace(object):
    def __init__(self,maingui):
        self.maingui   = maingui
        self.ffrutils   = maingui.ffrutils
        self.sig       = maingui.sig
        self.workspace = {}

    def init_workspace(self):
        print("init_workspace")
        self.clear()
        self.ffrutils.load_path(self.maingui.current_json)
        with open(self.maingui.current_json) as data_file: json_data = json.load(data_file)
        self.waveform_list, self.sc_label_list    = self.ffrutils.load_AVGs()
        metadata = self.ffrutils.get_metadata()
        for i, label in enumerate(self.sc_label_list):
            if "Noise" in label or "*" in label: continue
            ch,sc = self.sig.get_channel_sc(label)
            label.replace(" ", "")
            print("ch:",ch,"  sc",sc)
            newentry = {i:{"MetaData":metadata,
                        "SC":label,
                        "Data":json_data["FFR"][ch][sc],
                        "Filter":None}
                        }
            self.workspace.update(newentry)
        self.save()

    def get_waveform(self,id):
        return np.array(self.workspace[id]["Data"]["AVG"]["Waveform"])

    def load_AVGs(self):
        sc_list = []
        waveforms = np.zeros( [self.ffrutils.Nt,len(self.workspace)] )
        for id, entry in enumerate(self.workspace):
            label = self.workspace[entry]["SC"]
            channel,sc_string = self.sig.get_channel_sc(label)
            waveforms[:,id]= np.array(self.workspace[entry]["Data"]["AVG"]["Waveform"])
            sc_list.append(sc_string+" "+channel[-1])
        return waveforms, sc_list

    def add(self):
        pass

    def delete(self):
        pass

    def clear(self):
        self.workspace={}

    def list(self):
        pass

    def save(self):
        with open('data.json', 'w') as outfile:
            json.dump(self.workspace, outfile)

    def load(self):
        pass
