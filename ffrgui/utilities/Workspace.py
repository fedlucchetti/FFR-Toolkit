
# -*- coding: utf-8 -*-
import sys
import numpy as np
from scipy import signal


class Workspace(object):
    def __init__(self):
        self.maingui = maingui
        self.ffrjson     = maingui.ffr
        self.sig     = maingui.sig
        self.workspace = {'init_patient':{"init_SC":{}}}

    def init_workspace(self):
        print("init_workspace")

        self.ffrjson.load_path(self.maingui.current_json)
        self.waveform_list, self.sc_string_list    = self.ffrjson.load_AVGs()
        name,number,stim,ear,level = get_meta_data(self)
        self.workspace = {"Patients":{"number":number,"ear":ear,}}
