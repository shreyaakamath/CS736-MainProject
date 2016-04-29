import os
import numpy as np
import sys

fp = open(sys.argv[1],"r")

lines = fp.read().split("\n")
lines = [line for line in lines if line!='']
lines = lines[1:]

valid_data = []
for line in lines:
	data = line.split(",")
	if len(data) == 15:
		new_data = data[3:-1]
		#time,reqpersec,timeperreqall,timeperreq,transrate
		valid_data.append([new_data[2], new_data[7], new_data[8], new_data[9], new_data[10]])

valid_data = np.array(valid_data,dtype="float")

print sys.argv[1]
print "Mean: "+str(valid_data.mean(axis=0).tolist())
print "Stddev: "+str(valid_data.std(axis=0).tolist())
