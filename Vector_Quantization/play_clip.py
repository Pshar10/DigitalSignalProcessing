from numpy.lib.function_base import append
from ctypes import *
import numpy as np
import scipy.io.wavfile as wavfile
import numpy as np
from matplotlib import pyplot as plt
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


    def clipaudio(audio, samplingRate, channels ,Clip_Time):


        Chunk = 1024

        p = pyaudio.PyAudio()

        n = Clip_Time* samplingRate

        buf = audio[0:n]


        # open audio stream

        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=samplingRate,
                        output=True)
        


            
        sound = (buf.astype(np.int16).tostring())
    
        #stream.write(sound)

        # close stream and terminate audio object
        stream.stop_stream()
        stream.close()
        p.terminate()
        return buf
