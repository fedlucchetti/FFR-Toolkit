import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from tensorflow.keras.models import load_model
# tf.get_logger().setLevel('INFO')
import matplotlib.pyplot as plt

import sys
from os.path import split

import numpy as np




class LatencyNet(object):
    def __init__(self,maingui):
        print("Initializing LatencyNet  Class with default parameters")
        self.const = maingui.const
        self.deepfilter = maingui.deepfilter
        path2latency_model = os.path.join(split(os.path.realpath(__file__))[0], "models", "LatencyNetwork.h5")
        self.latencymodel  = load_model(path2latency_model,compile=False)

        self.fs            = self.const.fs
        self.Nt            = self.const.Nt
        self.dt            = self.const.dt
        self.t            = self.const.t



    def __reshape__(self,waveform):
        waveform = np.reshape(waveform,[self.Nt])
        return waveform



    def __get_ton_toff(self,gate):
        ton, toff=[],[]
        for id, g in enumerate(gate):
            try:
                if gate[id]==0 and gate[id+1]==1:
                    ton.append(id+1)
                elif gate[id]==1 and gate[id+1]==0:
                    toff.append(id+1)
            except: pass
        return ton, toff

    def get(self,waveform,threshold=0.95):
        ongate           = np.zeros([self.Nt])
        waveform         = self.deepfilter.apply_filter(waveform)
        waveform         = waveform/waveform.max()
        waveform         = np.reshape(waveform,[1,np.amax(waveform.shape)])
        forward,backward = self.latencymodel.predict(waveform),self.latencymodel.predict(waveform[::-1])
        gate          = 0.5*(forward+backward[::-1])
        gate          = self.__reshape__(gate)
        id_on         = np.where(gate>threshold)[0]
        ongate[id_on] = 1
        ton_list,toff_list = self.__get_ton_toff(ongate)
        return ton_list,toff_list




if __name__ == "__main__":
    latnet = LatencyNet()
