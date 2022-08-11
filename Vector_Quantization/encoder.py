from numpy.core.fromnumeric import size
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sound import *
import pickle
import scipy.spatial.distance as sd
from scipy.spatial import voronoi_plot_2d,Voronoi


def Show_plot(Codebook_Vector,test_vectors):
    
    vor = Voronoi(Codebook_Vector)

    
    voronoi_plot_2d(vor,show_points = None,show_vertices = None,line_colors = 'g')
    
    plt.scatter(test_vectors[:,0],test_vectors[:,1], color = 'b', s=10, label = 'Test signal')
    plt.scatter(Codebook_Vector[:,0],Codebook_Vector[:,1],color = 'r', marker = '*',s=30, label = 'code vector')
    plt.legend (loc = 'upper left')
    
    plt.show()

    return


codebook = pickle.load(open("Codebook.binㅤ","rb"))
Boundaries = pickle.load(open("voronoi_regions.bin","rb"))
test_signal = pickle.load(open("test_signal.bin","rb"))

# print(test_signal.shape)



N = 2
M = 256   # number of codevectors

def encodeVQ(codebook,test_signal):
   
   distance = np.zeros(M)  #Initiate Euclidean distance array
   row,col = test_signal.shape
   index = np.zeros(row)

   for i in range(row):
      for j in range(M):
         distance[j] = sd.euclidean(codebook[j],test_signal[i])  # distance between codebook and test_signal
      index[i] = np.argmin(distance)   #find minimum distance for all test_signal
      print("distance ", i)
   return index



test_signal = np.reshape(test_signal,(-1,N))   



# index = encodeVQ(codebook,test_signal)

# print(index.shape) #(616812,)


# pickle.dump(index,open("coded_vq_signals.bin","wb"),1)

index = pickle.load(open("coded_vq_signals.bin","rb"))

print(index[6000:12000])
print(index.min())
print(index.max())

Show_plot(codebook, test_signal)



