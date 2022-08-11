import scipy.signal as sp
import numpy as np
import matplotlib.pyplot as plt
from zplane import zplane




def plottingMinPhase(b, a=1, whole=False, axisFreqz=None, axisPhase=None):
    w, h = sp.freqz(b, a, worN=512, whole=whole)
    plt.suptitle('Minimum Phase frequency response')
    plt.plot(w, 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude (dB)')
    plt.xlabel('Normalized Frequency')
    plt.grid()
    if axisFreqz is not None:
        plt.axis(axisFreqz)

    plt.show()

    angles = np.angle(h)
    plt.plot(w, angles, 'r')
    plt.title("Minimum Phase angular response")
    plt.ylabel('Angle (radians)')
    plt.xlabel('Normalized Frequency')
    plt.grid()

    if axisPhase is not None:
        plt.axis(axisPhase)
    plt.show()
    return h


def plottingDeconvolution(b, a=1, whole=False, axisFreqz=None, axisPhase=None):
    w, h = sp.freqz(b, a, worN=512, whole=whole)
    plt.suptitle('After Decovolution frequency response')
    plt.plot(w, 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude (dB)')
    plt.xlabel('Normalized Frequency')
    plt.grid()
    if axisFreqz is not None:
        plt.axis(axisFreqz)

    plt.show()
    angles = np.angle(h)
    plt.plot(w, angles, 'r')
    plt.title("After Decovolution angular response")
    plt.ylabel('Angle (radians)')
    plt.xlabel('Normalized Frequency')
    plt.grid()

    if axisPhase is not None:
        plt.axis(axisPhase)
    plt.show()
    return h




F=[0,0.25,0.25+0.1,0.5]
Amplitude=[1,0]
W=[1,100]
N=20

filterCoefficients=sp.remez(N,F,Amplitude,W)


plt.plot(filterCoefficients)#Plotting Impulse Response
plt.show()


plottingMinPhase(filterCoefficients)#Plotting Frequency Response


frequencyRoots = np.roots(filterCoefficients)
zplane(frequencyRoots, 0, [-2, 2.1, -1.1, 1.1])#Plotting Z-plane


#mirror in
mirror, root = sp.deconvolve(filterCoefficients, [1, -frequencyRoots[0]])
mirror1,root1= sp.deconvolve(mirror, [1, -frequencyRoots[1]])
mirror2,root2= sp.deconvolve(mirror1, [1, -frequencyRoots[2]])
mirror3,root3= sp.deconvolve(mirror2, [1, -frequencyRoots[3]])
mirror4,root4= sp.deconvolve(mirror3, [1, -frequencyRoots[4]])

convolving = sp.convolve(sp.convolve(sp.convolve(sp.convolve(sp.convolve(mirror4, [1, -1.0/(frequencyRoots[0]).conjugate()]),  [1, -1.0/(frequencyRoots[1]).conjugate()]),[1, -1.0/(frequencyRoots[2]).conjugate()]),[1, -1.0/(frequencyRoots[3]).conjugate()]),[1, -1.0/(frequencyRoots[4]).conjugate()])

zplane(np.roots(convolving), 0, [-2, 2.1, -1.1, 1.1])

plottingDeconvolution(convolving,1)

print(frequencyRoots)
print(convolving)

