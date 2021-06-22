
# -*- coding: utf-8 -*-
import sys
import numpy as np
from scipy import signal



class Signal(object):
    def __init__(self,maingui):
        super().__init__()
        self.maingui = maingui
        self.const = maingui.const
        self.workspace = maingui.workspace
        self.deepfilter = maingui.deepfilter

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

        waveform,_ = self.maingui.workspace.get_waveform(self.maingui.current_id,'original')
        filters  = self.maingui.workspace.get_filters()
        # print('filter_current_waveform ', filters)
        for id in filters:
            try:
                if filters[id]['type']=='pass':type='bandpass'
                elif filters[id]['type']=='stop':type='bandstop'
                else: continue
                fmin     = filters[id]['state']['pos'][0]
                fmax     = fmin+filters[id]['state']['size'][0]
                b, a     = signal.butter(4, [fmin,fmax], type,fs=self.const.fs)
                waveform = signal.filtfilt(b, a, waveform, padlen=150)
            except:continue
        try:
            if filters['42']['enable']:
                waveform = self.deepfilter.apply_filter(waveform)
        except Exception as e:
            print('filter_current_waveform: ', e)
            raise
        self.workspace.set_waveform(self.maingui.current_id,waveform)


    def get_label(self,channel,sc):
        return sc + ' ' + channel[len(channel)-1]

    def order_waveforms(self,waveforms,label):
        sel_waveforms = {'init':[]}
        for idl in label:
            _wave = {idl:np.zeros(self.const.Nt)}
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


    def get_envelope(self,waveform):
        # dc = np.mean(waveform)
        return self.deepfilter.get_envelope(waveform)

    def get_diffenvelope(self,waveform):
        # TO DO #
        pass
        # dc = np.mean(waveform)
        # return self.deepfilter.get_diffphase(waveform)


    def offset_waveforms(self,waveforms):

        nSC              = waveforms.shape[1]
        DC               = np.array(np.zeros(nSC))
        _waveforms       = waveforms
        for ids in range(nSC-1):
            DC[ids+1]  = DC[ids]   + np.abs(np.min(_waveforms[:,ids])-np.mean(_waveforms[:,ids])) + np.abs(np.max(_waveforms[:,ids+1])-np.mean(_waveforms[:,ids+1]))
            _waveforms[:,ids+1] = _waveforms[:,ids+1]-DC[ids+1]


        return _waveforms

    def smooth_plot(self,x,y,window=23):
        xvals        = np.linspace(0,np.max(self.const.f),self.const.Nf*8)
        interpolated = np.interp(xvals,x,y)
        smoothed     = signal.savgol_filter(interpolated, window, 4)
        return smoothed , xvals
