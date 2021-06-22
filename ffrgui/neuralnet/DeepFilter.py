import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from tensorflow.keras.models import load_model
# tf.get_logger().setLevel('INFO')

import sys
from os.path import split

import numpy as np




class DeepFilter(object):
    def __init__(self,maingui):
        print("Initializing DeepFilter  Class with default parameters")
        self.const = maingui.const
        path2filter_model = os.path.join(split(os.path.realpath(__file__))[0], "models", "EFR_Autoencoder.h5")
        path2envelope_model = os.path.join(split(os.path.realpath(__file__))[0], "models", "Envelope_model.h5")
        # path2phase_model    = os.path.join(split(os.path.realpath(__file__))[0], "models", "Phase_model.h5")
        self.filtermodel = load_model(path2filter_model,compile=False)
        self.envelopemodel = load_model(path2envelope_model,compile=False)
        # self.phasemodel = load_model(path2phase_model,compile=False)
        # self.filtermodel.summary()
        self.fs          = self.const.fs
        self.Nt          = self.filtermodel.layers[0].input.shape[1]


    # TO DO
    def set_frequency(self,target_frequency):
        self.target_frequency = target_frequency

    # TO DO
    def lowpass_filter(self,waveform):
        pass

    def __reshape__(self,waveform):
        waveform = np.reshape(waveform,[1,np.amax(waveform.shape)])
        return waveform

    def apply_filter(self,waveform):
        scale       = waveform.max()
        waveform    = waveform/scale
        waveform    = self.__reshape__(waveform)
        filtered    = np.array(self.filtermodel.predict(waveform,batch_size=1)).astype('float')
        filtered    = np.reshape(filtered,[self.Nt])
        return (filtered*2-1)*scale

    def get_envelope(self,waveform):
        scale       = waveform.max()
        waveform    = waveform/scale
        waveform    = self.__reshape__(waveform)
        filtered    = np.array(self.envelopemodel.predict(waveform,batch_size=1)).astype('float')
        filtered    = np.reshape(filtered,[self.Nt])
        return filtered

    def get_diffphase(self,waveform):
        scale       = waveform.max()
        filtered    = np.zeros(waveform.shape)
        # waveform    = waveform/scale
        # waveform    = self.__reshape__(waveform)
        # filtered    = np.array(self.phasemodel.predict(waveform,batch_size=1)).astype('float')
        # filtered    = np.reshape(filtered,[self.Nt])
        return filtered


if __name__ == "__main__":
    deepfilter = DeepFilter()
    input = np.array(sys.argv[1::])
    flag  = False
    try:
        assert input.size==deepfilter.Nt
        flag==True
    except:
        print("DeepFilter: Input signal size needs to be 2048, input received:", input.size)

    if flag:
        waveform   = input
        waveform = waveform.astype('float')
        waveform = waveform.reshape([2048,1])
        filtered = deepfilter.apply_filter(waveform)
        print(filtered)
