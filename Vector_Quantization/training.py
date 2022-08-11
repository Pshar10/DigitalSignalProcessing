from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from sound import *
import pickle
import scipy.spatial.distance as sd
from scipy.spatial import voronoi_plot_2d,Voronoi
# external imports

from play_clip import mod as m
from quant import Quant as q


N = 2
M = 16**N  #Codevectors

def Training_Signal_data():

   samplerate, speech = wav.read("speech.wav")  # one channel or mono
   speech = m.clipaudio(speech,samplerate,1,3)
   data = speech
   #print(data.shape)
   return data

def Audio_test_Signal_data():

   rate, data = wav.read("Track48.wav") # two channels or stereo
   #print(data.shape)
   return data[:,1]

def Boundary_Calc(Codebook_Vector):

   print("Boundaries are being calculated....\n")


   num = len(Codebook_Vector)
   boundarynum = (num+1)*num/2       # number of boundaries
   boundary = np.zeros((int(boundarynum),2))

   codeVec = np.zeros((2,2))   # calculate the b between two codevector 
   b_seq = 0   # the sequence number of b

   for i in range(0,num-1):
       codeVec[0] = Codebook_Vector[i,:]
       for j in range(i+1,num):
          codeVec[1] = Codebook_Vector[j,:]
          boundary[b_seq] = (codeVec[0] + codeVec[1])/2
          b_seq = b_seq+1

   return boundary

def Code_Vectors_calc(training_vectors,Codebook_Vector):

   distance = np.zeros(M)  #Initiate Euclidean distance array(for one sample)
   row,col = training_vectors.shape
   index = np.zeros(row)   # x belongs to which codevector

   print("computing distance of each training vector with codebook vectors....\n")
   for i in range(row):
      for j in range(M):
         distance[j] = sd.euclidean(Codebook_Vector[j],training_vectors[i])
      index[i] = np.argmin(distance)   #find minimum distance for x
      #print("distance",i)

   vector = np.zeros((M,2))   # the sum of training sequences for regions 
   vectornum = np.zeros(M)   # how many samples in each region
   New_Codebook_Vector = np.zeros(Codebook_Vector.shape)   # new Yk
 
   print("computing new Codebook_Vectors by averaging the clusters of each index.....\n")
   for i in range(row):
      for j in range(M):
         if index[i] == j :   # if x[i] is in the region j
            vector[j] = vector[j] + training_vectors[i]  # add x[i] to region j
            vectornum[j] = vectornum[j] + 1   # the number of x in j
   
   for i in range(M):
      if vectornum[i] != 0:
         New_Codebook_Vector[i] = vector[i]/vectornum[i]    # new Yk

   Diff = np.sum(np.abs(New_Codebook_Vector-Codebook_Vector))   # the Diff between Codebook_Vector and new Codebook_Vector

   return New_Codebook_Vector,Diff



def Show_plot(Codebook_Vector,training_vectors):
    
    vor = Voronoi(Codebook_Vector)

    fig = voronoi_plot_2d(vor,show_points = None,show_vertices = None,line_colors = 'g')

    plt.scatter(training_vectors[:,0],training_vectors[:,1], color = 'b', s=10, label = 'Training signal')
    plt.scatter(Codebook_Vector[:,0],Codebook_Vector[:,1],color = 'r', marker = '*',s=30, label = 'code vector')
    plt.legend (loc = 'upper left')
    plt.show()

    return

if __name__ == '__main__':

   

   Training_Signal = Training_Signal_data()  #speech.wav
   Test_Signal_audio = Audio_test_Signal_data() #track48.wav
   
   #step one
   Codebook_Vector = np.zeros((M,2))    #Initiate Codebook_Vector

   training_vectors = np.reshape(Training_Signal,(-1,N))  #Initiate Xk

   Seq = np.linspace(np.min(Test_Signal_audio),np.max(Test_Signal_audio),M)
   Codebook_Vector[:,0] = Seq    #Assigned Codebook_Vector vectors
   Codebook_Vector[:,1] = Seq

   Diff = 30000   #Initialize Diff
   rep = 0
 
   while Diff > 20000 :   
     boundary = Boundary_Calc(Codebook_Vector)  
     Codebook_Vector,Diff = Code_Vectors_calc(training_vectors,Codebook_Vector)
     rep = rep +1
     print("Diff is:",Diff,"\n","This step is repeated :",rep , " times\n")

   boundary = Boundary_Calc(Codebook_Vector)  

   print("Boundaries and Codebook has been calculated.\n")

   # print("The Codebook_Vector is",Codebook_Vector)

   # codebook_dict = {ind : val for ind,val in enumerate(Codebook_Vector.tolist())}

   pickle.dump(Codebook_Vector,open("Codebook.bin  ","wb"),1)
   pickle.dump(boundary,open("voronoi_regions.bin","wb"),1)
   # pickle.dump(Test_Signal_audio,open("test_signal.bin","wb"),1)


   print("Showing the results............\n")

   Show_plot(Codebook_Vector,training_vectors)

   print("\n\n\n\n\n\nThe training is complete\n\n\n\n\n\n")











   

######### Test THE RESULTS ############
   
   # Training_Signal = Training_Signal_data()
   # training_vectors = np.reshape(Training_Signal,(-1,N)) 
   
   # Codebook_Vector = pickle.load(open("Codebook.binㅤ","rb"))
   # boundry = Boundary_Calc(Codebook_Vector)
   # print(boundry.shape)
   # print(Codebook_Vector.shape) #(256, 2)
   # print(Training_Signal.shape) #(16000,)
   # print(training_vectors.shape) #(8000, 2)
   # Show_plot(Codebook_Vector,training_vectors)
