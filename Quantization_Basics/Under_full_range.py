import pyaudio
import scipy.io.wavfile as wav
import struct
from numpy import clip
import numpy as np
from ctypes import *
from matplotlib import pyplot as plt
import scipy
import scipy.fftpack
from scipy.signal import freqz

# external imports

from mod import mod as m


#handled the warnings.
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()



warnings.filterwarnings("ignore", category=DeprecationWarning)  
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

channels = 0

#   Reading the file


samplerate, wavArray = wav.read("Track48.wav")

print("Sample rate for the track is: ",samplerate)


        
left = wavArray[:, 0]

        

	
channels = 2


audio = wavArray

m.playFile(audio, samplerate , channels) #To play the file


# m.clipaudio(audio, samplerate , channels)  #To clip the file

# plt.plot(20*np.log10(np.abs(left)+1e-6), label = 'Original Signal' )
# plt.legend(loc="upper left")

plt.plot(left, label = 'Original Signal' )
plt.legend(loc="upper left")


############### 35 db under the full range #######################

# -20log(x+1e-6) = 35 ==> log(x) = -(35/20) ==> x = 10**(-(35/20)) ==> x = 0.01778279410038923

# Since X is the amplitude ratio i.e New amp = amp* 0.01778279410038923\


# plt.plot(20*np.log10(np.abs(left * 0.01778279410038923)+1e-6), label = 'Under the full range Signal' )
plt.plot(left * 0.01778279410038923, label = 'Under the full range Signal' )
plt.legend(loc="upper left")
plt.show()


# m.playFile(audio * 0.01778279410038923, samplerate , channels) # To play the attenuated the file