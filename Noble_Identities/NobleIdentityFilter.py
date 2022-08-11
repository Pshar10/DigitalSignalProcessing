import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from sound import *
import scipy.fftpack


N = 6

samplerate, wavArray = wav.read('music.wav')

try:
    if wavArray.shape[1] == 2:
        left = wavArray[:, 0]
        right = wavArray[:, 1]
except:
    a = 1

signal_samples = left #input_quantized #quant_stereo #left #wavArray left_quantized



FFT = abs(scipy.fft.fft(signal_samples))
freqs = scipy.fftpack.fftfreq(signal_samples.size)

# w1, h1 = signal.freqz(signal_samples)

plt.plot(freqs*2*np.pi, FFT)
plt.title('Frequency response of original signal')
plt.xlabel('Normalized Frequency')
plt.ylabel('Magnitude of Frequency Response in dB')


plt.show()
#upsampled frequency response of signal
up_samples = np.zeros(N*len(signal_samples))

up_samples[0::N] = signal_samples

FFT_upsampled = abs(scipy.fft.fft(up_samples))
freqs_upsampled = scipy.fftpack.fftfreq(up_samples.size)


# u, v = signal.freqz(up_samples)

plt.plot(freqs_upsampled*2*np.pi, FFT_upsampled)
plt.title('Frequency response of upsampled signal with aliasing')
plt.xlabel('Normalized Frequency')
plt.ylabel('Magnitude of Frequency Response in dB')
plt.show()


# initialising polyphase operations from here. Designing filter first

n = 32
#remez filter design function
filterCoefficients = signal.remez(n,[0,((np.pi/6)-0.20),(np.pi/6),np.pi],[1,0],[1,100],fs=2*np.pi)

w2, h2 = signal.freqz(filterCoefficients)

#Impulse response or filter coefficient
plt.plot(filterCoefficients)
plt.title('Impulse response')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.show()

#Frequency response
plt.plot(w2, 20 * np.log10(abs(h2)+1e-6)) #db conversion
plt.title('Frequency response of filter')
plt.xlabel('Normalized Frequency')
plt.ylabel('Magnitude of Frequency Response in dB')
plt.show()


#filter polyphase components 
#parallel processing at lower sampling rate
h0 = filterCoefficients[0::N]
h1 = filterCoefficients[1::N]
h2 = filterCoefficients[2::N]
h3 = filterCoefficients[3::N]
h4 = filterCoefficients[4::N]
h5 = filterCoefficients[5::N]





# Noble Identities


# up_samples = np.zeros(len(signal_samples)*N) # initializing

# up_samples[0::N] = signal_samples
# up_samples[1::N] = signal_samples
# up_samples[2::N] = signal_samples
# up_samples[3::N] = signal_samples
# up_samples[4::N] = signal_samples
# up_samples[5::N] = signal_samples

# FFT_upsampled = abs(scipy.fft.fft(up_samples))
# freqs_upsampled = scipy.fftpack.fftfreq(up_samples.size)








Y0 = signal.lfilter(h0, [1], signal_samples)
Y1 = signal.lfilter(h1, [1], signal_samples)
Y2 = signal.lfilter(h2, [1], signal_samples)
Y3 = signal.lfilter(h3, [1], signal_samples)
Y4 = signal.lfilter(h4, [1], signal_samples)
Y5 = signal.lfilter(h5, [1], signal_samples)

# begining upsampling

maximum_length=np.max([len(Y0),len(Y1),len(Y2),len(Y3),len(Y4),len(Y5)])
print(maximum_length)
up_samples = np.zeros(maximum_length*N) # initializing

up_samples[0::N] = Y0
up_samples[1::N] = Y1
up_samples[2::N] = Y2
up_samples[3::N] = Y3
up_samples[4::N] = Y4
up_samples[5::N] = Y5

FFT_upsampled = abs(scipy.fft.fft(up_samples))
freqs_upsampled = scipy.fftpack.fftfreq(up_samples.size)

plt.plot(freqs_upsampled*2*np.pi, FFT_upsampled)
plt.title('Frequency response with filtering and  upsampling')
plt.xlabel('Normalized Frequency')
plt.ylabel('Magnitude of Frequency Response in dB')
plt.show()


# u, v = signal.freqz(up_samples)
# plt.plot(freqs*2*np.pi, FFT)
# plt.plot(freqs_upsampled*2*np.pi, FFT_upsampled)
# plt.title('Frequency response of polyphased filtering and then upsampling')
# plt.xlabel('Normalized Frequency')
# plt.ylabel('Magnitude of Frequency Response in dB')
# plt.show()


# sound(signal_samples*0.7,samplerate)
#sound(up_samples*0.7,samplerate*N)
















