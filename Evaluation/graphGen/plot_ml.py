import matplotlib.pyplot as pyplot
import csv
import numpy as np
# radius = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# area = [3.14159, 12.56636, 28.27431, 50.26544, 78.53975, 113.09724]

ml=[]
means=[]
stds=[]


with open("ml.csv",'rU') as f:
    j=0
    for line in f:
        if j==0:
            for word in line.split(","):
                ml.append(word.strip())
        elif j==1:
            for word in line.split(","):
                means.append(float(word))
        elif j==2:
            for word in line.split(","):
                stds.append(float(word))
        j=j+1
# print means
# print stds
# print ml
# means   = [26.82,26.4,61.17,61.55]         # Mean Data 
# stds    = [4.59,4.39,4.37,4.38]            # Standard deviation Data
# peakval = ['26.82','26.4','61.17','61.55'] # String array of means

ind = np.arange(len(means))
width = 0.35
colours = ['yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow']

pyplot.figure()
pyplot.title('ML Accuracy')
for i in range(len(means)):
    print means[i]
    pyplot.bar(ind[i],means[i],width,color=colours[i],align='center',yerr=stds[i],ecolor='k')
pyplot.ylabel('Accuracy')
pyplot.xticks(ind,ml)

def autolabel(bars,peakval):
    for ii,bar in enumerate(bars):
        height = bars[ii]
        pyplot.text(ind[ii], height-5, '%s'% (peakval[ii]), ha='center', va='bottom')
# autolabel(means,peakval)
# autolabel(means)    


# pyplot.grid()
pyplot.savefig("ml.eps", format='eps',dpi=300,bbox_inches='tight')

