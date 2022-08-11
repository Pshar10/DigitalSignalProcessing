import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sound import *
import pickle
from play_clip import mod as m

N = 2
M = 16**N   # number of codevectors

def decodeVQ(codebook,coded_vq_signal):
   
   x = np.zeros((len(coded_vq_signal),2))  #x is of shape (616812,2)
   for i in range(len(coded_vq_signal)):    # len is 616812
      x[i] = codebook[int(coded_vq_signal[i])]
   return x

rate, data = wav.read("Track48.wav")   
test_signal = data[:,1]

codebook = pickle.load(open("Codebook.binㅤ","rb"))
coded_vq_signal = pickle.load(open("coded_vq_signals.bin","rb"))
coded_uniform_q_signal = pickle.load(open("coded_uniform_q_signal.bin","rb"))



decoded = decodeVQ(codebook,coded_vq_signal)    # shape is (616812, 2)


decoded = np.reshape(decoded,(-1))  #shape is (1233624,)

print(decoded.shape)
print(test_signal.shape)

decode = decoded

#sound(decode,rate)
n=4 #4bits
q =int((np.max(test_signal))- (np.min(test_signal))/(2**n))  #stepsize, 4 bit accuracy
mid_tread_quantization = coded_uniform_q_signal*q
error1 = test_signal-mid_tread_quantization
error2 = test_signal-decode

print("signal size",max(mid_tread_quantization),min(mid_tread_quantization))
print("quantization error for mid-tread signal:",error1)
print("quantization error for vector-quantied signal",error2)

l1, = plt.plot(test_signal, color= 'red')
l2, = plt.plot(mid_tread_quantization)
plt.legend(handles = [l1,l2],labels = ['test_signal','mid-tread'])
plt.title('Test_signal vs Mid tread ')
plt.show()

l2, = plt.plot(decode, color = 'blue')
l1, = plt.plot(test_signal, color= 'red')
plt.legend(handles = [l1, l2],labels = ['test_signal','vector-quantied signal'])
plt.title('Test_signal vs vector-quantied ' )
plt.show()


l2, = plt.plot(mid_tread_quantization, color = 'blue')
l1, = plt.plot(decode, color = 'red')
plt.legend(handles = [l1, l2],labels = ['vq','uniform'])
plt.title('Vector-quantied signal vs Uniform quantization' )
plt.show()

# samplerate, speech = wav.read("Track48.wav") 

# m.playFile(mid_tread_quantization,samplerate,1)
# m.playFile(decode,samplerate,1)



import os
print('original_audio.bin   :',int(os.path.getsize('original_audio.bin'))*10**-6,'MB')


print('coded_uniform_q_signal.bin    :',int(os.path.getsize('coded_uniform_q_signal.bin'))*10**-6,'MB')


print('coded_vq_signals.bin    :',int(os.path.getsize('coded_vq_signals.bin'))*10**-6,'MB')