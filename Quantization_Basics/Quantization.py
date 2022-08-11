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


class Quant(object):


    def quantization(original):
        
        a=0
        

        channels = 0

        try:
            if original.shape[1] == 2:
                channels = 2
                left = original[:, 0]
                right = original[:, 1]
                a=1

            
            
                
            
        except:
        
                channels = 1


    #start block-wise signal processing:

        # N = input("Enter your Bit depth: ")



        Bit_depth = 8
        Bit_depth =  int(Bit_depth)

        stepsize=int((2**15-(-2**15))/(2**Bit_depth))

        if a == 0:
            
            N = 4  #change the value accordingly
            N = int(N)
            stepsize = 1/2**(N-1)
            left = original

        # FOR mu-law
        
        y=np.sign(left)*(np.log(1+255*np.abs(left/32768.0)))/np.log(256)

        quant_rise_ind=np.floor(left/stepsize)
        quant_tread_ind=np.round(left/stepsize)
        quant_tread_ind_mu_law=np.round(y/stepsize)


        quant_rise_rec=quant_rise_ind*stepsize+stepsize/2
        quant_tread_rec=quant_tread_ind*stepsize
        quant_tread_rec_mu_law=quant_tread_ind_mu_law*stepsize
        
        plt.subplot(2,1,1)
        plt.plot(left, "b" , label="Original Signal")
        plt.plot(quant_rise_rec, "r",label="Quantised Signal for MID RISE")
        plt.legend(loc="upper left")
        
        plt.subplot(2,1,2)
        plt.plot(left, "g" , label="Original Signal")
        plt.plot(quant_tread_rec, "r",label="Quantised Signal for MID TREAD")
        plt.legend(loc="upper left")

        plt.show()

        return quant_rise_rec,quant_tread_rec

samplerate, wavArray = wav.read("Track48.wav")


quant_rise_rec,quant_tread_rec = Quant.quantization(wavArray) 


#######################

# print(wavArray[:, 0]-quant_tread_rec)

# plt.subplot(2,1,1)
# plt.plot((wavArray[:, 0]-quant_tread_rec), "b" , label="Original Signal")
# plt.legend(loc="upper left")

# plt.show()