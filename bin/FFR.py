#from IPython import embed
import numpy as np
import matplotlib.pyplot as plt
import json
from scipy import signal
import os
import sys
import math
from fnmatch import fnmatch

#from pathlib import Path, PureWindowsPath


class FFR():
    name = "FFR"

    def __init__(self):
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

        _temppath      = os.path.dirname(os.getcwd())
        # print("_temppath = ",_temppath)
        self.conf_path = os.path.join("conf" , "display.json")
        print(self.conf_path)
        # self.conf_path = os.path.join(_temppath , "conf" , "display.json")

        #self.conf_path = 'C:/Users/Tauonium/Documents/FFR_App/conf/display.json'

        with open(self.conf_path) as data_file:
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
        print('dir home',self.home_dir)
        if os.path.exists(os.path.join(_dir[0],'Signal_Spectra')):
            pass
        else:
            print(os.path.join(_dir[0],'Signal_Spectra'))
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

    def load_metadata(self):
        with open(self.path) as data_file:
            data = json.load(data_file)
        return data["MetaData"]

    def load_json(self):
        data = []
        with open(self.path) as data_file:
            data = json.load(data_file)
        return data

    def load_AVG(self,waveforms=None):

        if waveforms == None:waveforms = self.initwaveforms
        #if json_path == None: json_path = self.path
        json_path = self.path
        print('FFR.py load JSON path: ',json_path)

        with open(json_path) as data_file: data = json.load(data_file)

        for channel in data["FFR"]:
            for sc_string in data["FFR"][channel]:
                waveforms[channel][sc_string]= 10**-2 * np.array(data["FFR"][channel][sc_string]["AVG"]["Waveform"])
        return waveforms



    def get_frequency(self,SCstring):
        metadata = self.load_metadata()
        f1       = float(metadata["Stimulus"]["F1"])
        f2       = float(metadata["Stimulus"]["F2"])

        f        = None
        print('wsfvwsdf = ',SCstring[0:3])
        #if fnmatch(SCstring, 'EFR'): print('yeeeeeeeeeeeeeeeeee')
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
        metadata = self.load_metadata()
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

    def list_all(self):
        name      = list()
        number    = list()
        date      = list()
        stim      = list()
        ear       = list()
        level     = list()
        code      = list()
        path2json = list()
        root    = '/media/ergonium/KINGSTON/AnalyseFFR_LV/Patients&Subjects/NewNH20172018'
        pattern = "*.json"
        for path, subdirs, files in os.walk(root):
            for filename in files:
                if fnmatch(filename, pattern):

                    path = os.path.join(path, filename)
                    path2json.append(path)
                    with open(path) as data_file:
                        data = json.load(data_file)
                    if data["MetaData"]["Patient"]["Nom"]           != None \
                       or data["MetaData"]["Patient"]["Prenom"]     != None \
                       or data["MetaData"]["Patient"]["Number"]     != None \
                       or data["MetaData"]["date string"]           != None \
                       or data["MetaData"]["Patient"]["Oreille"]    != None \
                       or data["MetaData"]["Stimulus"]["Level[dB]"] != None :
                        year      = data["MetaData"]["date string"]
                        year      = year[len(year)-2:len(year)]
                        frequency = str(round(int(data["MetaData"]["Stimulus"]["F2"])-int(data["MetaData"]["Stimulus"]["F1"])))

                        name.append(data["MetaData"]["Patient"]["Nom"]  + ' ' + data["MetaData"]["Patient"]["Prenom"])
                        number.append(year + data["MetaData"]["Patient"]["Number"])
                        date.append(data["MetaData"]["date string"])
                        stim.append('EFR' + frequency)
                        ear.append(data["MetaData"]["Patient"]["Oreille"])
                        level.append(str(data["MetaData"]["Stimulus"]["Level[dB]"]))
                        code.append(''.join([data["MetaData"]["Patient"]["Nom"]  , ' ' , data["MetaData"]["Patient"]["Prenom"] ,\
                                            year + data["MetaData"]["Patient"]["Number"]                                       ,\
                                            data["MetaData"]["Patient"]["Oreille"]                                             ,\
                                            str(data["MetaData"]["Stimulus"]["Level[dB]"])                                     ,\
                                            'EFR' , frequency                                                                   ]))



        return name,number,date,stim,ear,level,path2json,code


    def plot_recording(self,export=True,display=True):


        SC                               = self.load_AVG()
        RV, CV, RH, CH                   = self.compute_RC(SC)
        SC                               = self.order_SCs(SC)
        outputwfm                        = np.array([])
        outputlabelpos                   = np.array([[],[]])
        outputlabel                      = list()


        plt.figure()
        fig, ax = plt.subplots()

        # stimulus
        stim = self.generate_stimulus()
        stim = stim/max(stim)*max(RV)
        plt.plot(self.t*1000,-stim  + 3*max(stim),'k',linewidth=self.width_line/2)
        outputwfm = np.append(outputwfm,-stim  + 3*max(stim),axis=0)
        plt.text(-20, 3*max(stim), 'Stimulus',fontsize=self.font_text,color='k')
        outputlabelpos = np.append(outputlabelpos, [[-20],[3*max(stim)]], axis=1)
        outputlabel = np.append(outputlabel,'Stimulus')

        # R&C
        plt.plot(self.t*1000,RV,'r',linewidth=self.width_line/2)
        plt.plot(self.t*1000,CV,'b',linewidth=self.width_line/2)
        outputwfm = np.append(outputwfm,RV,axis=0)
        outputwfm = np.append(outputwfm,CV,axis=0)
        xpos = np.average(RV)
        plt.text(-20, xpos, 'R',fontsize=self.font_text,color=self.color_R)
        plt.text(-16, xpos, '&',fontsize=self.font_text,color='k')
        plt.text(-12, xpos, 'C',fontsize=self.font_text,color=self.color_C)
        plt.text(-6,  xpos, 'V',fontsize=self.font_text,color='k')
        outputlabelpos = np.append(outputlabelpos, [[-20],[xpos]], axis=1)
        outputlabel = np.append(outputlabel,'R V')
        outputlabel = np.append(outputlabel,'C V')

        DC                               = np.abs(np.min(RV))+np.max(RV)
        plt.plot(self.t*1000,RH-DC,'r',linewidth=self.width_line/2)
        plt.plot(self.t*1000,CH-DC,'b',linewidth=self.width_line/2)
        outputwfm = np.append(outputwfm,RH-DC,axis=0)
        outputwfm = np.append(outputwfm,CH-DC,axis=0)
        outputlabel = np.append(outputlabel,'R H')
        outputlabel = np.append(outputlabel,'C H')

        xpos = np.average(RH-DC)
        plt.text(-20, xpos, 'R',fontsize = self.font_text,color=self.color_R)
        plt.text(-16, xpos, '&',fontsize = self.font_text,color='k')
        plt.text(-12, xpos, 'C',fontsize = self.font_text,color=self.color_C)
        plt.text(-6,  xpos, 'H',fontsize = self.font_text,color='k')
        outputlabelpos = np.append(outputlabelpos, [[-20],[xpos]], axis=1)


        DC                               = DC+2*np.abs(np.min(RH))+np.max(RH)
        DC                               = DC+self.compute_offsets(SC)

        # gPTPV waveforms
        filt_SC = self.filter_SC(SC,self.SCstring)
        for idx in range(len(DC)):
            if idx%2==0:
                color = self.color_V
                text  = self.SCstring[idx] + ' V'
            else:
                color = self.color_H
                text  = self.SCstring[idx] + ' H'

            plt.plot(self.t*1000,filt_SC[:,idx]-DC[idx],color,linewidth=self.width_line)
            plt.text(-20, np.average(SC[:,idx]-DC[idx]),text,fontsize=self.font_text)
            outputwfm = np.append(outputwfm,filt_SC[:,idx]-DC[idx],axis=0)
            outputlabelpos = np.append(outputlabelpos, [[-20],[np.average(SC[:,idx]-DC[idx])]], axis=1)
            outputlabel = np.append(outputlabel,text)

        plt.xlabel('Temps [ms]',fontsize=self.font_axes)
        plt.xlim([-25,98])
        plt.xticks([0,10,20,30,40,50,60,70,80],['0','10','20','30','40','50','60','70','80'],fontsize=self.font_ticks)
        labels = [item.get_text() for item in ax.get_yticklabels()]
        empty_string_labels = ['']*len(labels)
        ax.set_yticklabels(empty_string_labels)
        plt.grid(axis='x')
        plt.errorbar(86, 0 , yerr=0.1/(10**9), uplims=True, lolims=True,label='uplims=True, lolims=True',color=self.color_scale)
        plt.text(91, 0, '0.1 $\mu$V',fontsize=self.font_text,rotation=90,verticalalignment='center')

        header = 'FFR  \n' + self.generate_header()
        plt.title(header,fontsize=self.font_text)


        _tmp    = os.path.split(self.path)
        outpath = os.path.join(_tmp[0] , "Signal_Spectra" , "temporal.png")
        print(outpath)
        #outpath = "/media/ergonium/Données/FFR/FFR_App/Data/183527/Harmonique_LE/85dB/Signal_Spectra/temporal.png"

        if export: plt.savefig(outpath,quality=100,format='png',dpi=800)
        if display:
            plt.show()
            plt.close()
        return outputwfm, outputlabel, outputlabelpos

    def plot_spectra(self,scale=1):
        SC           = self.load_AVG()
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







if __name__ == "__main__":


    _temppath     = os.path.dirname(os.getcwd())
    if len(sys.argv[1:])!=0:
        path = sys.argv[1]
        print('loading input path')
        print(path)
    else:
        #path = os.path.join(_temppath , "Data", "183527" , "Harmonique_LE" , "85dB" , "Meta_AVG_data.json")

        #path = "C:\\Users\\Delpau\\Desktop\\FFR_RZ6\\2020\\209998\\ENV1000_RE85dB\\Meta_AVG_data.json"
        path = "sample/202692/Harmonique_LE85dB/Meta_AVG_data.json"
        print('loading test path')
        print(path)


    ffr = FFR()
    ffr.load_path(path)

    ffr.plot_recording()
    ffr.plot_spectra(scale = 10)
    #SC = ffr.load_AVG()
