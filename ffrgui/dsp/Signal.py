
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
        self.latencynet = maingui.latencynet
        self.ffrutils   = maingui.ffrutils

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

    def get_diffenvelope(self,waveform,scaled=False):
        # TO DO #
        # dc = np.mean(waveform)
        # return self.deepfilter.get_diffphase(waveform)
        _sc        = self.maingui.temporalWidget.current_sc.split(' ')[0]
        f_sc       = self.maingui.database.get_frequency(_sc)
        ip_wav     = np.unwrap(np.angle(signal.hilbert(waveform)))
        y          = np.sin(2 * np.pi * f_sc * np.arange(self.const.Nt) / self.const.fs)
        ip_sin     = np.unwrap(np.angle(signal.hilbert(y)))
        phase_diff = np.abs(ip_wav - ip_sin)
        if scaled:
            scale      = phase_diff.max()
            phase_diff = phase_diff/scale

        return phase_diff

    def get_wind_plv(self,phase_diff): #windowed PLV
        onset = int(self.workspace.onset/1000*self.const.fs)
        if (self.workspace.offset) == 0:
            offset = self.const.Nt
        else:
            offset = int(self.workspace.offset/1000*self.const.fs)

        _plv = np.empty(np.abs(offset-onset), dtype='complex')
        for i,j in enumerate(range(onset,offset)):
            _plv[i] = np.exp(complex(0,phase_diff[j]))
        w_plv = np.abs(np.sum(_plv, axis=0)/len(_plv))

        return w_plv

    def gaussian(self,mu,sigma=1):
        """
        units in [ms]
        """
        y = 1/(sigma * np.sqrt(2 * np.pi)) * \
            np.exp( - (self.const.t*1000-mu)**2 / (2 * sigma**2))
        return y/max(y)

    def get_onet_offset_dist(self,waveform):
        ton_list,toff_list = self.latencynet.get(waveform)
        ton_dist,toff_dist  = np.zeros(self.const.Nt),np.zeros(self.const.Nt)
        for idt in ton_list:
            center = idt*self.const.dt*1000
            if center < 40:
                ton_dist+=self.gaussian(center)
        for idt in toff_list:
            center = idt*self.const.dt*1000
            if center > 40:
                toff_dist+=self.gaussian(center)
        return ton_dist/max(ton_dist),toff_dist/max(toff_dist)

    def offset_waveforms(self,waveforms):

        nSC              = waveforms.shape[1]
        DC               = np.array(np.zeros(nSC))
        _waveforms       = waveforms
        for ids in range(nSC-1):
            DC[ids+1]  = DC[ids]   + np.abs(np.min(_waveforms[:,ids])-np.mean(_waveforms[:,ids])) + np.abs(np.max(_waveforms[:,ids+1])-np.mean(_waveforms[:,ids+1]))
            _waveforms[:,ids+1] = _waveforms[:,ids+1]-DC[ids+1]


        return _waveforms

    def cross_corr_stim(self,waveform):
        # Stimulus
        onset    = round(5/1000*self.const.fs)   # 5 ms
        length   = round(57/1000*self.const.fs)  # 55 ms
        risefall = round(1/1000*self.const.fs)   # rise and fall time
        t_gate   = self.const.dt*np.array([x for x in range(risefall)])

        f1    = self.maingui.database.get_frequency("F1")
        f2    = self.maingui.database.get_frequency("F1")
        data  = self.ffrutils.load_json()
        a1    = float(data["MetaData"]['Stimulus']['V1[V]'])
        a2    = float(data["MetaData"]['Stimulus']['V2[V]'])

        pause = np.zeros(onset)
        on    = np.ones(length)
        cos2  = np.square(np.cos(2*np.pi*250*t_gate))
        gate  = np.concatenate((pause,np.flip(cos2),on,cos2))
        end   = np.zeros(self.const.Nt-len(gate))
        gate  = np.append(gate,end)

        f_efr    = self.maingui.database.get_frequency("EFR")
        stimulus = np.sin(2*np.pi*f_efr*self.const.t) #stimulus =  a1*np.sin(2*np.pi*f1*self.const.t+np.pi/2) + a2*np.sin(2*np.pi*f2*self.const.t-np.pi/2)
        stimulus = np.append(pause,stimulus)[0:self.const.Nt]
        stimulus = np.multiply(stimulus,gate)

        #Cross correlation
        corr = signal.correlate(waveform, stimulus, mode='same') / np.sqrt(signal.correlate(stimulus,stimulus, mode='same')[int(self.const.Nt/2)] * signal.correlate(waveform, waveform, mode='same')[int(self.const.Nt/2)])
        delay_arr = np.linspace(-0.5*self.const.Nt/self.const.fs, 0.5*self.const.Nt/self.const.fs, self.const.Nt)
        delay = delay_arr[np.argmax(corr)]

        return (delay*1000)+5.0

    def smooth_plot(self,x,y,window=23):
        xvals        = np.linspace(0,np.max(self.const.f),self.const.Nf*8)
        interpolated = np.interp(xvals,x,y)
        smoothed     = signal.savgol_filter(interpolated, window, 4)
        return smoothed , xvals
