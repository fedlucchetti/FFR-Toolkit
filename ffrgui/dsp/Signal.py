
# -*- coding: utf-8 -*-
import sys
import numpy as np
from scipy import signal


class Signal(object):
    def __init__(self,maingui):
        super().__init__()
        self.maingui = maingui
        self.ffrutils = maingui.ffrutils
        self.workspace = maingui.workspace
        # self.ffrutils = ffr
        # self.ui  = ui

    def normalize_waveforms(self,waveforms):
        n_sc     = 0
        max_values = list()
        for ids in range(waveforms.shape[1]):
            max_values.append(np.max(waveforms[:,ids]))
        scale_factor = np.max(max_values)
        for ids in range(waveforms.shape[1]):
            waveforms[:,ids] = waveforms[:,ids]/scale_factor

        return waveforms, scale_factor


    def filter_current_waveform(self):
        waveform = self.maingui.workspace.get_waveform(self.maingui.current_id)
        filters  = self.maingui.workspace.current_workspace[self.maingui.current_id]['Filters']
        for id in filters:
            if filters[id]['type']=='pass':type='bandpass'
            elif filters[id]['type']=='stop':type='bandstop'
            fmin     = filters[id]['state']['pos'][0]
            fmax     = fmin+filters[id]['state']['pos'][0]
            b, a     = signal.butter(4, [fmin,fmax], type,fs=self.ffrutils.fs)
            waveform = signal.filtfilt(b, a, waveform, padlen=150)
        self.workspace.current_workspace[self.maingui.current_id]["Data"]["AVG"]["Waveform"] = waveform


    def get_label(self,channel,sc):
        return sc + ' ' + channel[len(channel)-1]

    def order_waveforms(self,waveforms,label):
        sel_waveforms = {'init':[]}
        for idl in label:
            _wave = {idl:np.zeros(self.ffrutils.Nt)}
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

        nSC              = waveforms.shape[1]
        DC               = np.array(np.zeros(nSC))
        print("offset_waveforms ",waveforms.shape)
        _waveforms       = waveforms
        for ids in range(nSC-1):
            DC[ids+1]  = DC[ids]   + np.abs(np.min(_waveforms[:,ids])-np.mean(_waveforms[:,ids])) + np.abs(np.max(_waveforms[:,ids+1])-np.mean(_waveforms[:,ids+1]))
            _waveforms[:,ids+1] = _waveforms[:,ids+1]-DC[ids+1]


        return _waveforms

    def get_sc_temporal(self):
        print("ffr.py: current_json ",self.maingui.current_json)
        print("ffr.py: current sc   ",self.maingui.current_sc)
        channel, sc = self.ffrutils.get_channel_sc(self.maingui.current_sc)
        _, noise_waveform = self.ffrutils.load_AVG(sc,channel)
        sig_waveform = self.maingui.current_waveform
        return sig_waveform, noise_waveform

    def get_sc_spectral(self):
        print("ffr.py: current_json ",self.maingui.current_json)
        print("ffr.py: current sc   ",self.maingui.current_sc)
        sig_waveform, noise_waveform = self.get_sc_temporal()
        sig_waveform = np.absolute(np.fft.fft(sig_waveform))
        noise_waveform = np.absolute(np.fft.fft(noise_waveform))
        return sig_waveform[0:self.ffrutils.Nf], noise_waveform[0:self.ffrutils.Nf]
