from numpy.lib.function_base import append
from scipy.fft import fft 
import scipy.signal
from ctypes import *
import struct
import numpy as np
import getch
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
import wave
import pyaudio
from playsound import playsound
import sounddevice as sd
import soundfile as sf

class mod(object):
    
    def playFile(audio, samplingRate, channels):


        p = pyaudio.PyAudio()

        # open audio stream

        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=samplingRate,
                        output=True)
        


        sound = (audio.astype(np.int16).tostring())
        stream.write(sound)

        # close stream and terminate audio object
        stream.stop_stream()
        stream.close()
        p.terminate()
        return


    def clipaudio(audio, samplingRate, channels):


        Chunk = 1024

        p = pyaudio.PyAudio()

        Clip_Time = 8

        n = Clip_Time* samplingRate

        buf = audio[0:n-1]


        # open audio stream

        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=samplingRate,
                        output=True)
        


            
        sound = (buf.astype(np.int16).tostring())
    
        stream.write(sound)

        # close stream and terminate audio object
        stream.stop_stream()
        stream.close()
        p.terminate()
        return
