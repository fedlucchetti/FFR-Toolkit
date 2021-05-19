
# -*- coding: utf-8 -*-
import sys, json, copy
import numpy as np
from scipy import signal
from PyQt5.QtWidgets import  QFileDialog
from ffrgui.gui       import FileDialog



class Workspace(object):
    def __init__(self,maingui):
        self.maingui   = maingui
        self.ffrutils   = maingui.ffrutils
        self.current_current_workspace = {}

    def init_workspace(self):

        print("init_current_workspace")
        self.clear()
        self.ffrutils.load_path(self.maingui.current_json)
        with open(self.maingui.current_json) as data_file: json_data = json.load(data_file)
        self.waveform_list, self.sc_label_list    = self.ffrutils.load_AVGs()
        metadata = self.ffrutils.get_metadata()
        for i, label in enumerate(self.sc_label_list):
            if "Noise" in label or "*" in label: continue
            ch,sc = self.ffrutils.get_channel_sc(label)
            label.replace(" ", "")
            # print("id ",i," ch:",ch,"  sc",sc)
            newentry = {i:{"MetaData":metadata,
                        "SC":label,
                        "Data":{'original':copy.deepcopy(json_data["FFR"][ch][sc]),
                                "filtered":copy.deepcopy(json_data["FFR"][ch][sc]),
                                "noise"   :json_data["FFR"][ch]['Noise']},
                        "Filters":{-1:None}}
                        }
            self.current_workspace.update(newentry)
        self.maingui.update_temporal_plot()
        # self.save()

    def get_waveform(self,id,flag='original'):
        signal = np.array(self.current_workspace[id]["Data"][flag]["AVG"]["Waveform"]).astype("float")
        noise  = np.array(self.current_workspace[id]["Data"]['noise']["AVG"]["Waveform"]).astype("float")
        return signal, noise

    def set_waveform(self,id,waveform):
        self.current_workspace[id]["Data"]["filtered"]["AVG"]["Waveform"] = waveform

    def get_sc_spectral(self,flag='original'):
        # print("ffr.py: current_json ",self.maingui.current_json)
        # print("ffr.py: current sc   ",self.maingui.current_sc)
        sig_waveform, noise_waveform = self.get_waveform(self.maingui.current_id,flag)
        sig_waveform   = np.absolute(np.fft.fft(sig_waveform))
        noise_waveform = np.absolute(np.fft.fft(noise_waveform))
        return sig_waveform[0:self.ffrutils.Nf], noise_waveform[0:self.ffrutils.Nf]

    def get_sc_spectral_original(self,flag='original'):
        # print("ffr.py: current_json ",self.maingui.current_json)
        # print("ffr.py: current sc   ",self.maingui.current_sc)
        sig_waveform   = np.array(self.current_workspace[self.maingui.current_id]["Data"]['original']["AVG"]["Waveform"]).astype("float")
        sig_waveform   = np.absolute(np.fft.fft(sig_waveform))
        return sig_waveform[0:self.ffrutils.Nf]

    def get_filters(self):
        return self.current_workspace[self.maingui.current_id]['Filters']


    def load_AVGs(self):
        sc_list = []
        waveforms = np.zeros( [self.ffrutils.Nt,len(self.current_workspace)] )
        for id, entry in enumerate(self.current_workspace):
            label             = self.current_workspace[entry]["SC"]
            channel,sc_string = self.ffrutils.get_channel_sc(label)
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

    def save(self):
        self.filedialog = self.maingui.filedialog
        filename = self.filedialog.saveFileDialog()
        with open(filename, 'w') as outfile:
            json.dump(self.current_workspace, outfile)


    def load(self):
        self.filedialog = self.maingui.filedialog
        filename = self.filedialog.openFileNameDialog()
        with open(filename, 'r') as outfile:
            self.current_workspace = json.load(outfile)
        self.maingui.update_temporal_plot()
