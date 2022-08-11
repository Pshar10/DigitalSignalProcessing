
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sem_1_3 import Quant as q

from scipy.fft import fft 
from numpy import sqrt, mean, sum

#***************************************** Making Sine wave****************************************************************###
Fs = 32000   # Sampling frequency
T=1/Fs       # Sampling Time


A=1
freq=3200


t = np.linspace(0, 20, 32000) # Time vector
t_t =  np.linspace(0, 22.5, 32000) # Time vector
S = t_t-2.5
sinewave = A*np.sin(2*np.pi*(freq/Fs)*t)
plt.xlim([0,20])
plt.plot(t,sinewave,'--', label='Original Signal')

plt.xlabel('Time [s]')
plt.ylabel('Amplitude')


#***************************************** Making triangular wave****************************************************************###

triangle = A*signal.sawtooth(2*np.pi*(freq/Fs)*t, 0.5)
plt.xlim([0,20])
plt.plot(t-2.5, triangle)
plt.show()


############################# Quantizing both ##############################################################

quant_rise_rec_sine,quant_tread_rec_sine =q.quantization(sinewave)
quant_rise_rec_trinagle,quant_tread_rec_triangle =q.quantization(triangle)

noise_sine_quant_rise_rec_sine = sinewave -  quant_rise_rec_sine

noise_triangle_quant_rise_rec = triangle - quant_rise_rec_trinagle


plt.plot(noise_sine_quant_rise_rec_sine , label = 'Quantisation(4 bit) noise for Sine Wave')
plt.legend(loc="upper left")
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.show()

plt.plot(noise_triangle_quant_rise_rec , label = 'Quantisation(4 bit) noise for Triangle Wave')
plt.legend(loc="upper left")
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.show()




N = 4

Signal_to_noise_ratio_sine = 1.76+ 6.02*N

Signal_to_noise_ratio_triangle = 6.02*N


print('SNR(dB) of Sine wave after quantization : ',abs(Signal_to_noise_ratio_sine),'\n And SNR(dB) of Triangular wave after quantization : ',abs(Signal_to_noise_ratio_triangle))


