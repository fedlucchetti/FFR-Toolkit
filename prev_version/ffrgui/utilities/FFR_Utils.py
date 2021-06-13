import os, sys, json,math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from fnmatch import fnmatch
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import  QtGui



#from pathlib import Path, PureWindowsPath


class FFR_Utils():
    name = "FFR_Utils"

    def __init__(self,maingui):
        self.maingui = maingui
        self.workspace   = maingui.workspace
        self.database    = maingui.database


        self.home_dir  = ''
        self.path      = ''
        self.fs        = 24414.0
        self.dt        = 1/self.fs
        self.Nt        = 2048
        self.Nf        = 1024
        self.df        = self.fs/self.Nt
        self.t         = self.dt*np.array([x for x in range(self.Nt)])
        self.f         = self.df*np.array([x for x in range(self.Nf)])
        self.SCstring  = ['EFR','EFR','F1','F1','F2','F2','CDT','CDT','ABR','ABR']

        self.initwaveforms = {'Channel-V':{'EFR':[],'EFR**':[],'EFR***':[],'CDT':[],'CDT*':[],'F1':[],'F2':[],'ABR':[],'Noise':[]},\
                     'Channel-H':{'EFR':[],'EFR**':[],'EFR***':[],'CDT':[],'CDT*':[],'F1':[],'F2':[],'ABR':[],'Noise':[]} }



        self.database.select_db_path(False)

        self.path_conf     = os.path.join(self.maingui.CONFDIR,"display.json")
        with open(self.path_conf) as data_file:
            display = json.load(data_file)

        self.font_ticks   = int(display["font_size"]["ticks"])
        self.font_axes    = int(display["font_size"]["axes"])
        self.font_text    = int(display["font_size"]["text"])
        self.font_y_unit  = int(display["font_size"]["y_unit"])
        self.font_title   = int(display["font_size"]["title"])

        self.color_R      = display["color"]["R"]
        self.color_C      = display["color"]["C"]
        self.color_V      = display["color"]["V"]
        self.color_H      = display["color"]["H"]
        self.color_Noise  = display["color"]["Noise"]
        self.color_scale  = display["color"]["scale"]

        self.width_line   = int(display["width"]["line"])


        print("FFR class initialized")






    def load_path(self,path):
        self.path = path
        _dir = os.path.split(path)
        self.home_dir = _dir[0]
        if os.path.exists(os.path.join(_dir[0],'Signal_Spectra')):
            pass
        else:
            # print(os.path.join(_dir[0],'Signal_Spectra'))
            try:os.mkdir(os.path.join(_dir[0],'Signal_Spectra'))
            except: print('error creating ',os.path.join(_dir[0],'Signal_Spectra'))

    def order_SCs(self,SC):
        _SC = np.zeros([self.Nt,10])

        _SC[:,0] = SC["Channel-V"]["EFR"]      # EFR V
        _SC[:,1] = SC["Channel-H"]["EFR"]      # EFR H
        _SC[:,2] = SC["Channel-V"]["F1"]       # F1 V
        _SC[:,3] = SC["Channel-H"]["F1"]       # F1 H
        _SC[:,4] = SC["Channel-V"]["F2"]       # F2 V
        _SC[:,5] = SC["Channel-H"]["F2"]       # F2 H
        _SC[:,6] = SC["Channel-V"]["CDT"]      # CDT V
        _SC[:,7] = SC["Channel-H"]["CDT"]      # CDT H
        _SC[:,8] = SC["Channel-V"]["ABR"]      # ABR V
        _SC[:,9] = SC["Channel-H"]["ABR"]      # ABR H

        return _SC

    def get_working_directory(self,path):
        dir_file = os.path.split(path)
        self.home_dir = dir_file[0]



    def load_json(self):
        data = []
        with open(self.path) as data_file: data = json.load(data_file)
        return data

    def load_AVG(self,sc_string,channel):
        json_path = self.path
        with open(json_path) as data_file: data = json.load(data_file)
        signal = np.array(data["FFR"][channel][sc_string]["AVG"]["Waveform"])
        noise  = np.array(data["FFR"][channel]["Noise"]["AVG"]["Waveform"])
        return signal, noise

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


    def get_channel_sc(self,label):
        channel = 'Channel-' + label[len(label)-1]
        sc = label[len(label)-3::-1]
        sc = sc[::-1]
        return channel, sc



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

    def generate_stimulus(self):
        f1       = self.get_frequency("F1")
        f2       = self.get_frequency("F2")
        onset    = round(5/1000*self.fs)                      # 5 ms
        length   = round(55/1000*self.fs)                     # 55 ms
        risefall = round(1/1000*self.fs)                      # rise and fall time

        pause    = np.zeros(onset)
        gate     = np.tanh(500*self.t[1:length+2*risefall])
        gate     = 0.5*(gate + np.flip(gate,axis=0))
        gate     = np.append(pause,gate)
        end      = np.zeros(self.Nt-len(gate))
        gate     = np.append(gate,end)
        stimulus = np.sin(2*np.pi*f1*self.t+np.pi/2) + np.sin(2*np.pi*f2*self.t-np.pi/2)
        stimulus = np.multiply(stimulus,gate)
        return stimulus

    def filter_SC(self,SCwfm,SCstring):
        print('FFR.py    current waveform   ',SCstring)

        #for idx in range(np.size(SCwfm,1)):
        if isinstance(SCstring,list):
            filtSC = np.zeros([self.Nt,len(SCstring)])
            for idx in range(len(SCstring)):
                fc = self.get_frequency(SCstring[idx])
                print('SC frequency',fc)

                if SCstring[idx] == 'ABR':
                    fmin = 20/(self.fs/2)
                    fmax = 1500/(self.fs/2)
                    b, a = signal.butter(4, [fmin,fmax], 'bandpass')
                else:
                    fmin = (fc+300)/(self.fs/2)
                    fmax = (4000)/(self.fs/2)
                    b, a = signal.butter(4, [fmin,fmax], 'bandstop')
                filtSC[:,idx] = signal.filtfilt(b, a, SCwfm[:,idx], padlen=150)
                print(fmin*(self.fs/2), fmax*(self.fs/2))
        else:
            filtSC = []
            fc = self.get_frequency(SCstring)
            if SCstring == 'ABR':
                fmin = 20/(self.fs/2)
                fmax = 1500/(self.fs/2)
                b, a = signal.butter(4, [fmin,fmax], 'bandpass')
            else:
                fmin = (fc+300)/(self.fs/2)
                fmax = (4000)/(self.fs/2)
                b, a = signal.butter(4, [fmin,fmax], 'bandstop')


            filtSC = signal.filtfilt(b, a, SCwfm, padlen=150)

        return filtSC

    def compute_offsets(self,SC):
        nSC  = np.size(SC,1)
        DC   = np.array(np.zeros(nSC))
        for idx in range(nSC-1):
            DC[idx+1] = DC[idx] + np.abs(np.min(SC[:,idx])) + np.max(SC[:,idx+1]) + 2*(idx%2)*np.max(SC[:,idx+1])
            DC[idx+1] = DC[idx+1] + 0.05*DC[idx+1]
        return DC

    def compute_RC(self,SC):
        RV =      SC["Channel-V"]["EFR"] + SC["Channel-V"]["EFR**"] + SC["Channel-V"]["EFR***"] + SC["Channel-V"]["ABR"]
        RV = RV + SC["Channel-V"]["F1"]  - SC["Channel-V"]["F2"]    - SC["Channel-V"]["CDT"]    - SC["Channel-V"]["CDT*"]
        CV =      SC["Channel-V"]["EFR"] + SC["Channel-V"]["EFR**"] + SC["Channel-V"]["EFR***"] + SC["Channel-V"]["ABR"]
        CV = CV - SC["Channel-V"]["F1"]  - SC["Channel-V"]["F2"]    - SC["Channel-V"]["CDT"]    - SC["Channel-V"]["CDT*"]

        RH =      SC["Channel-H"]["EFR"] + SC["Channel-H"]["EFR**"] + SC["Channel-H"]["EFR***"] + SC["Channel-H"]["ABR"]
        RH = RH + SC["Channel-H"]["F1"]  - SC["Channel-H"]["F2"]    - SC["Channel-H"]["CDT"]    - SC["Channel-H"]["CDT*"]
        CH =      SC["Channel-H"]["EFR"] + SC["Channel-H"]["EFR**"] + SC["Channel-H"]["EFR***"] + SC["Channel-H"]["ABR"]
        CH = CH - SC["Channel-H"]["F1"]  - SC["Channel-H"]["F2"]    - SC["Channel-H"]["CDT"]    - SC["Channel-H"]["CDT*"]

        return RV, CV, RH, CH

    def compute_spectra(self,SC,scale):
        spectra = SC
        for channel in SC:
            for sc_string in SC[channel]:
                _tmp = scale*np.absolute(np.fft.fft(SC[channel][sc_string]))
                spectra[channel][sc_string]=_tmp[0:self.Nf]

        _tmpV = np.absolute(np.fft.fft(SC["Channel-V"]["F1"]+SC["Channel-V"]["F2"]))
        F1F2V=np.array(_tmpV[0:self.Nf])

        _tmpH = np.absolute(np.fft.fft(SC["Channel-H"]["F1"]+SC["Channel-H"]["F2"]))
        F1F2H=np.array(_tmpH[0:self.Nf])


        spectra["Channel-V"].update({"F1F2":F1F2V})
        spectra["Channel-H"].update({"F1F2":F1F2H})
        return spectra

    def generate_header(self):
        metadata = self.get_metadata()
        title = 'Patient: ' + metadata["Patient"]["Number"] + '\n Stim: ' + str(metadata["Stimulus"]["Level[dB]"])
        title = title + ' dB SPL' + ' --- $f_1$= ' + str(metadata["Stimulus"]["F1"])
        title = title + 'Hz & $f_2$= ' + str(metadata["Stimulus"]["F2"])+'Hz'
        return title

    def generate_outputpath(self):
        outputpath = None
        return outputpath

    def smooth_plot(self,x,y,window=23):
        xvals        = np.linspace(0,np.max(self.f),self.Nf*8)
        interpolated = np.interp(xvals,x,y)
        smoothed     = signal.savgol_filter(interpolated, window, 4)
        return smoothed , xvals

    def find_index(self,array,element,delta):
        index = []
        for idx in range(len(array)):
            if array[idx] > element - delta and  array[idx] < element + delta :
                index.append(idx)

        return index




    def plot_spectra(self,scale=1):
        SC,_           = self.load_AVGs()
        Noise_V      = SC["Channel-V"]["Noise"]
        Noise_H      = SC["Channel-H"]["Noise"]
        #♀SC           = self.order_SCs(SC)
        fft_SC       = self.compute_spectra(SC,scale)

        Noisefloor_V = np.absolute(scale*np.fft.fft(Noise_V))
        Noisefloor_V = Noisefloor_V[0:self.Nf]
        Noisefloor_H = np.absolute(scale*np.fft.fft(Noise_H))
        Noisefloor_H = Noisefloor_H[0:self.Nf]


        ############################################################ ALL ############################################################
        selSC = ['EFR','CDT','F1','F2']
        #selSC = ['F1']
        for sc_string in selSC:
            if sc_string == "F1F2":
                f1    = self.get_frequency("F1")
                f2    = self.get_frequency("F2")
                header = 'Spectre ' + '$F_1F_2$' + '\n' + self.generate_header()
                if f2>1200:
                    minF = (math.floor(f1/100)-2)*100
                    maxF = (math.ceil(f2/100)+2)*100
                else:
                    minF = 0
                    maxF = 1200
            else:

                minF = 0
                maxF = 1200
                header = 'Spectre ' + sc_string + '\n' + self.generate_header()


            waveV = fft_SC["Channel-V"][sc_string]
            waveH = fft_SC["Channel-H"][sc_string]
            MaxFFT_V       = (round(np.max(waveV)*10**6/10)+1)*10
            MaxFFT_H       = (round(np.max(waveH)*10**6/10)+1)*10


            plt.figure()
            #fig, ax = plt.subplots()

            y,f = self.smooth_plot(self.f,10**6*waveV)
            plt.plot(f,y,'k',linewidth=self.width_line)

            if sc_string == "F1F2":
                    index = self.find_index(f,self.get_frequency("F1"),25)
                    ypos = np.max(y[index])
                    xpos = np.argmax(10**6*y[index])
                    plt.text(round(f[xpos+min(index)]), ypos+2.5, "$F_1$" + ' V',fontsize=self.font_text,color='k',weight='bold',ha='center')
                    index = self.find_index(f,self.get_frequency("F2"),25)
                    ypos = np.max(y[index])
                    xpos = np.argmax(10**6*y[index])
                    plt.text(round(f[xpos+min(index)]), ypos+2.5, "$F_2$" + ' V',fontsize=self.font_text,color='k',weight='bold',ha='center')
            else:
                    index = self.find_index(f,self.get_frequency(sc_string),25)
                    ypos = np.max(y[index])
                    xpos = np.argmax(10**6*y[index])
                    plt.text(round(f[xpos+min(index)]), ypos+2.5, sc_string + ' V',fontsize=self.font_text,color='k',weight='bold',ha='center')


            y,f = self.smooth_plot(self.f,10**6*Noisefloor_V,99)
            plt.fill_between(f,y,color=self.color_Noise)



            y,f = self.smooth_plot(self.f,10**6*waveH)
            plt.plot(f,-y,'k',linewidth=self.width_line)

            if sc_string == "F1F2":
                    index = self.find_index(f,self.get_frequency("F1"),25)
                    ypos = np.max(y[index])
                    xpos = np.argmax(10**6*y[index])
                    plt.text(round(f[xpos+min(index)]), -ypos-2.5, "$F_1$" + ' H',fontsize=self.font_text,color='k',weight='bold',ha='center')
                    index = self.find_index(f,self.get_frequency("F2"),25)
                    ypos = np.max(y[index])
                    xpos = np.argmax(10**6*y[index])
                    plt.text(round(f[xpos+min(index)]), -ypos-2.5, "$F_2$" + ' H',fontsize=self.font_text,color='k',weight='bold',ha='center')
            else:
                    index = self.find_index(f,self.get_frequency(sc_string),25)
                    ypos = np.max(y[index])
                    xpos = np.argmax(10**6*y[index])
                    plt.text(round(f[xpos+min(index)]), -ypos-2.5, sc_string + ' H',fontsize=self.font_text,color='k',weight='bold',ha='center')


            y,f = self.smooth_plot(self.f,10**6*Noisefloor_H,79)
            plt.fill_between(f,-y,color=self.color_Noise)


            plt.xlabel('Fréquence [Hz]',fontsize=self.font_axes)
            plt.ylabel('Amplitude [nV]',fontsize=self.font_axes)
            plt.xlim([minF,maxF])
            plt.ylim([-MaxFFT_H,MaxFFT_V])

            yticks = []
            yticklabels = []
            for idx in range(-int(MaxFFT_H),int(MaxFFT_V),+5):
                yticks.append(idx)
                yticklabels.append(str(abs(idx)))
            plt.yticks(yticks,yticklabels,fontsize=self.font_ticks)
            plt.tick_params(axis='both',labelsize=self.font_ticks)

            plt.grid(True)


            print(header)
            plt.title(header,fontsize=self.font_text)

            _tmp    = os.path.split(self.path)
            outpath = os.path.join(_tmp[0] , "Signal_Spectra" , sc_string+"_spectrum.png")
            try:
                plt.savefig(outpath,quality=100,format='png',dpi=800)
            except:
                pass
                #plt.show()
            plt.close()
