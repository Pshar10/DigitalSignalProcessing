from scipy.fft import fft 
from scipy import signal
from ctypes import *
import numpy as np
import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
import sounddevice as sd
import scipy.io.wavfile as wav
import math as ma
from scipy.integrate import simps
from numpy import sqrt, mean, sum
import scipy.fftpack


# external imports

from mod import mod as m


def quantization():

    fs_original, original = wav.read("Track48.wav")

    channels = 0

    try:
        if original.shape[1] == 2:
            channels = 2
            left = original[:, 0]
            right = original[:, 1]
        
    except:
    
            channels = 1



#start block-wise signal processing:

    # N = input("Enter your Bit depth: ")
    N = 8
    N = int(N)


    stepsize=int((2**15-(-2**15))/(2**N))
    

    # FOR mu-law
    
    q= 1/2**7  # Because signal amplitude varies from -1 to 1 now levels are 8 bits so q is (1-(-1))/2**8 ==> 1/2**7



    y=np.sign(left)*(np.log(1+255*np.abs(left/32768)))/np.log(256)

    # print(y)

    quant_rise_ind=np.floor(left/stepsize)
    quant_tread_ind=np.round(left/stepsize)
    quant_tread_ind_mu_law=np.round(y/q)


    quant_rise_rec=quant_rise_ind*stepsize+stepsize/2
    quant_tread_rec=quant_tread_ind*stepsize
    quant_tread_rec_mu_law=quant_tread_ind_mu_law*q

    quant_tread_rec_mu_law=np.sign(quant_tread_rec_mu_law)*(np.exp(np.log(256)*np.abs(quant_tread_rec_mu_law))-1)/255*32768

    # print(quant_tread_rec_mu_law)

    plt.subplot(2,1,1)
    plt.plot(quant_tread_rec, "b" , label="Mid-tread Signal")
    plt.legend(loc="upper left")
    plt.plot(quant_tread_rec_mu_law, "r",label="mu-law Signal for Signal")
    plt.legend(loc="upper left")

    plt.show()

    return quant_tread_rec_mu_law,quant_tread_rec

quant_tread_rec_mu_law,quant_tread_rec = quantization()

samplerate, wavArray = wav.read("Track48.wav")

#m.playFile(quant_tread_rec_mu_law, samplerate , 1)

noise_signal_mu_law = (wavArray[:, 0]-quant_tread_rec_mu_law)
noise_signal_tread = (wavArray[:, 0]-quant_tread_rec)

freqs, psd_signal = signal.welch(wavArray[:, 1])
plt.figure(figsize=(5, 4))
plt.semilogx(freqs, psd_signal)
plt.title('PSD: power spectral density of Original Signal')
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.show()


freqs, psd_noise_signal_mu = signal.welch(noise_signal_mu_law)
plt.figure(figsize=(5, 4))
plt.semilogx(freqs, psd_noise_signal_mu)
plt.title('PSD: power spectral density of mu law quanitsed signal')
plt.xlabel('Frequency')
plt.ylabel('Noise_Power_mu')
plt.show()

freqs, psd_noise_signal_tread = signal.welch(noise_signal_tread)
plt.figure(figsize=(5, 4))
plt.semilogx(freqs, psd_noise_signal_tread)
plt.title('PSD: power spectral density of mid tread quantised signal')
plt.xlabel('Frequency')
plt.ylabel('Noise_Power_tread')
plt.show()



X = scipy.fft.fft(wavArray[:, 0])

rayleigh_signal = (sum(abs(X)**2))/len(X) # Trying to apply parseval theorem (Rayleigh's energy theorem)

print(rayleigh_signal)

X = scipy.fft.fft(noise_signal_mu_law)

rayleigh_noise_mu_law = (sum(abs(X)**2))/len(X)

print(rayleigh_noise_mu_law)

X = scipy.fft.fft(noise_signal_tread)

rayleigh_noise_tread = sum(abs(X)**2)/len(X)

rayleigh_Signal_to_noise_ratio = rayleigh_signal/rayleigh_noise_mu_law

rayleigh_Signal_to_noise_ratio_tread = rayleigh_signal/rayleigh_noise_tread

Signal_to_noise_ratio = 10*np.log10(rayleigh_Signal_to_noise_ratio)

Signal_to_noise_ratio_tread = 10*np.log10(rayleigh_Signal_to_noise_ratio_tread)



print('Signal to noise ratio of mu law quant:',Signal_to_noise_ratio,'dB')
print('Signal to noise ratio of Mid Tread quant:',Signal_to_noise_ratio_tread,'dB')


if (Signal_to_noise_ratio>Signal_to_noise_ratio_tread):
    print('SNR of mu law quantization is better than mid tread')
else:
    print('There is some mis-calculation')





