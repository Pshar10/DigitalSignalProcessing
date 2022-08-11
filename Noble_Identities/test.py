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
################################################################################################################################################################################


FFT = abs(scipy.fft.fft(signal_samples))
freqs = scipy.fftpack.fftfreq(signal_samples.size)

# w1, h1 = signal.freqz(signal_samples)

plt.plot(freqs*2*np.pi, FFT)
plt.title('Frequency response of original signal')
plt.xlabel('Normalized Frequency')
plt.ylabel('Magnitude of Frequency Response in dB')


plt.show()

