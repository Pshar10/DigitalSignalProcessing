from scipy.fft import fft 
import scipy.signal
from ctypes import *
import struct
import numpy as np
import scipy
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
# external imports

from play_clip import mod as m


class Quant(object):


    def quantization(original):
        
        
        


    #start block-wise signal processing:

        # N = input("Enter your Bit depth: ")



        N = 8
        N = int(N)

        stepsize=int((np.max(original))- (np.min(original))/(2**N))





        quant_tread_ind=np.round(original/stepsize)



        quant_tread_rec=quant_tread_ind*stepsize



        
        
        plt.plot(quant_tread_rec, "r",label="Quantised Signal for MID TREAD")
        plt.plot(original, "g" , label="Original Signal")
        plt.legend(loc="upper left")

        plt.show()

        return quant_tread_rec

samplerate, wavArray = wav.read("Track48.wav")

print(wavArray[:,1].shape)








