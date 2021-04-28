
# -*- coding: utf-8 -*-
import sys
import numpy as np
from scipy import signal


class Signal(object):
    def __init__(self,maingui):
        super().__init__()
        self.maingui = maingui
        self.ffrjson     = maingui.ffr
        # self.ffrjson = ffr
        # self.ui  = ui

    def normalize_waveforms(self,waveforms):
        channels = list()
        n_sc     = 0
        max_values = list()
        for idc in waveforms.keys():
            channels.append(idc)
            for ids in waveforms[idc]:
                max_values.append(np.max(waveforms[idc][ids]))
        scale_factor = np.max(max_values)
        for idc in waveforms.keys():
            for ids in waveforms[idc]:
                waveforms[idc][ids] = waveforms[idc][ids]/scale_factor

        return waveforms, scale_factor

    def get_channel_sc(self,label):
        channel = 'Channel-' + label[len(label)-1]
        sc = label[len(label)-3::-1]
        sc = sc[::-1]
        return channel, sc

    def get_label(self,channel,sc):
        return sc + ' ' + channel[len(channel)-1]

    def order_waveforms(self,waveforms,label):
        sel_waveforms = {'init':[]}
        for idl in label:
            _wave = {idl:np.zeros(self.ffrjson.Nt)}
            sel_waveforms.update(_wave)

        for channel in waveforms.keys():
            for sc in waveforms[channel]:
                _label = self.get_label(channel,sc)
                try:
                    if str(label.index(_label)).isnumeric:
                        _wave = {_label:waveforms[channel][sc]}
                        sel_waveforms.update(_wave)

                except: pass
        del sel_waveforms['init']
        return sel_waveforms

    def offset_waveforms(self,waveforms):

        nSC              = len(waveforms.keys())
        DC               = np.array(np.zeros(nSC))
        sc_list          = waveforms.keys()
        _waveforms       = np.array(np.zeros([self.ffrjson.Nt,nSC]))
        dc_waveforms = sel_waveforms = {'init':[]}
        idx        = 0
        for label in waveforms.keys():
            try:_waveforms[:,idx] = waveforms[label]
            except: pass
            idx+=1
        for ids in range(nSC-1):
            DC[ids+1]  = DC[ids]   + np.abs(np.min(_waveforms[:,ids])-np.mean(_waveforms[:,ids])) + np.abs(np.max(_waveforms[:,ids+1])-np.mean(_waveforms[:,ids+1]))
            _waveforms[:,ids+1] = _waveforms[:,ids+1]-DC[ids+1]
            #_waveforms[:,ids+1] = _waveforms[:,ids+1] - (np.max(_waveforms[:,ids+1])-np.mean(_waveforms[:,ids+1]))
        ids = 0
        for label in waveforms.keys():
            #waveforms[label] = _waveforms[:,ids]
            dc_waveforms.update({label:_waveforms[:,ids]})
            ids+=1
        del dc_waveforms['init']

        return dc_waveforms, DC

    def get_sc_temporal(self):
        print("ffr.py: current_json ",self.maingui.current_json)
        print("ffr.py: current sc   ",self.maingui.current_sc)
        channel, sc = self.get_channel_sc(self.maingui.current_sc)
        self.ffrjson.load_path(self.maingui.current_json)
        sig_waveform, noise_waveform = self.ffrjson.load_AVG(sc,channel)
        return sig_waveform, noise_waveform

    def get_sc_spectral(self):
        print("ffr.py: current_json ",self.maingui.current_json)
        print("ffr.py: current sc   ",self.maingui.current_sc)
        sig_waveform, noise_waveform = self.get_sc_temporal()
        sig_waveform = np.absolute(np.fft.fft(sig_waveform))
        noise_waveform = np.absolute(np.fft.fft(noise_waveform))
        return sig_waveform[0:self.ffrjson.Nf], noise_waveform[0:self.ffrjson.Nf]
