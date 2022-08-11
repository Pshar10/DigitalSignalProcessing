from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import pyaudio
from sound import *
import pickle
from play_clip import mod as m
from quant import Quant as q

n = 4  #4 bits

rate1, data = wav.read("Track48.wav")   
test_signal = data[:,1]  
pickle.dump(test_signal,open("test_signal.bin","wb"),1)  


samplerate, speech = wav.read("speech.wav")
speech = m.clipaudio(speech,samplerate,1,3)
data = speech





q =int((np.max(test_signal))- (np.min(test_signal))/(2**n))    #stepsize
index = np.round(test_signal/q)    # mid-tread
mid_tread_quantized = index*q

l1, = plt.plot(test_signal, color= 'red')
l2, = plt.plot(mid_tread_quantized, color= 'green')
plt.title('comparison of reconstructed signal')
plt.xlabel('samples')
plt.ylabel('Magnitude')
plt.legend(handles = [l1,l2,],labels = ['original','mid-tread'])
plt.show()

#index = index.astype('int8')
pickle.dump(index,open("coded_uniform_q_signal.bin","wb"),1)

