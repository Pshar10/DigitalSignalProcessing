import scipy.signal as sp
from sound import *



def warpingphase(w, a):
    theta = np.angle(a);
    r = np.abs(a);
    wy = -w-2*np.arctan((r*np.sin(w-theta))/(1-
    r*np.cos(w-theta)));
    return wy




N=6 #filter coefficients
Amplitude=[1,0] #Desired Amplitude
W=[1, 100] #Weighted error

CuttOffFrequency=0.15*np.pi #cutoff frequency in kHz


fs, wavArray = wav.read('music.wav')
left = wavArray[:, 0]
signal_samples = left

coefficientsAllpass = 1.0674*(2/np.pi*np.arctan(0.06583*fs))**0.5 - 0.1916 #coefficients of warping allpass



CuttOffWarping=-warpingphase(CuttOffFrequency,coefficientsAllpass)#This is wrapped cuttoff frequency
CuttOffNormalized=CuttOffWarping/(2*np.pi)#normalized to 2 pi for remez



F= [0, CuttOffNormalized, CuttOffNormalized+0.05, 0.5] #Band edges


filterCoefficients = sp.remez(N,F,Amplitude,W)#filter Coefficients

# Warping Allpass filters:
Zeros = [-coefficientsAllpass.conjugate(), 1]  #Numerator
Poles = [1, -coefficientsAllpass] #Denominator


downsampled = signal_samples[0:signal_samples.shape[0]:4]#Downs  ampling with factor 4

AmpMax=np.max(downsampled)

print(AmpMax)

# Warped delays:
y1 = sp.lfilter(Zeros,Poles,downsampled)
y2 = sp.lfilter(Zeros,Poles,y1)
y3 = sp.lfilter(Zeros,Poles,y2)
y4 = sp.lfilter(Zeros,Poles,y3)
y5 = sp.lfilter(Zeros,Poles,y4)

yout = filterCoefficients[0]*downsampled+filterCoefficients[1]*y1+filterCoefficients[2]*y2+filterCoefficients[3]*y3+filterCoefficients[4]*y4+filterCoefficients[5]*y5

yout=yout/abs(np.max(yout))

yout= yout*2**15

print('Warped  Output')
sound(yout,fs//4)




#For Minimun Phase Filter

F=[0,0.25,0.25+0.1,0.5]
Amplitude=[1,0]
W=[1,100]
N=6

filterCoefficients=sp.remez(N,F,Amplitude,W)


frequencyRoots = np.roots(filterCoefficients)


[b, r] = sp.deconvolve(filterCoefficients, [1,-frequencyRoots[0]])


minPhase=sp.convolve(b,[1,-1/frequencyRoots[0].conjugate()])


minPhaseResult=sp.lfilter(minPhase, [1], downsampled)



print('Minimum Phase Output')
sound(np.real(minPhaseResult),fs//4)#Minimum phase output















