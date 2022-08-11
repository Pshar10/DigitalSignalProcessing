import scipy.signal as sp
import matplotlib.pyplot as plt
from zplane import zplane
import numpy as np







def plottingWarped(b, a=1, whole=False, axisFreqz=None, axisPhase=None):
    w, h = sp.freqz(b, a, worN=512, whole=whole)
    plt.suptitle('Warped Filter frequency response')
    plt.plot(w, 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude (dB)')
    plt.xlabel('Normalized Frequency')
    plt.grid()
    if axisFreqz is not None:
        plt.axis(axisFreqz)

    plt.show()



    angles = np.angle(h)
    plt.plot(w, angles, 'r')
    plt.title("warped filter angular response")
    plt.ylabel('Angle (radians)')
    plt.xlabel('Normalized Frequency')
    plt.grid()

    if axisPhase is not None:
        plt.axis(axisPhase)
    plt.show()
    return h




def warpingphase(w, a):
    theta = np.angle(a);
    r = np.abs(a);
    wy = -w-2*np.arctan((r*np.sin(w-theta))/(1- r*np.cos(w-theta)));
    return wy






N=6 #filter coefficients
Amplitude=[1,0] #Amplitude
W=[1, 100] #Weight


SamplingFrequency=44.1
CuttoffFrequency=0.15*np.pi

coefficientsAllpass = 1.0674*(2/np.pi*np.arctan(0.6583*SamplingFrequency))**0.5 - 0.1916 #coefficients of warping allpass




CuttOffWarping = - warpingphase(CuttoffFrequency,coefficientsAllpass) #This is wrapped cuttoff frequency
CuttOffNormalized=CuttOffWarping/(2*np.pi) #normalized to 2 pi for remez


F= [0, CuttOffNormalized, CuttOffNormalized+0.05, 0.5] #Band edges

print('CuttOffWarping = ',CuttOffWarping)
print('CuttOffNormalized = ',CuttOffNormalized)



# Warping Allpass filters:
Zeros = [-coefficientsAllpass.conjugate(), 1]  #Numerator
Poles = [1, -coefficientsAllpass] #Denominator






filterCoefficients = sp.remez(N,F,Amplitude,W)#filter Coefficients




# Impulse with 50 zeros:
Imp = np.zeros(50)
Imp[0] = 1
impulseResponse = Imp

# Warped delays:
y1 = sp.lfilter(Zeros,Poles,impulseResponse)
y2 = sp.lfilter(Zeros,Poles,y1)
y3 = sp.lfilter(Zeros,Poles,y2)
y4 = sp.lfilter(Zeros,Poles,y3)
y5 = sp.lfilter(Zeros,Poles,y4)

yout = filterCoefficients[0]*impulseResponse+filterCoefficients[1]*y1+filterCoefficients[2]*y2+filterCoefficients[3]*y3+filterCoefficients[4]*y4+filterCoefficients[5]*y5



plt.plot(yout)
plt.xlabel('Sample')
plt.ylabel('value')
plt.title('Impulse Response ')
plt.tight_layout()
plt.show()



plottingWarped(b=yout, a=1)


zplane(np.roots(yout), 0, [-1.5, 2.5, -1.5, 1.5])




