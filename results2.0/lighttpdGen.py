import os
import numpy as np
import sys

fp = open(sys.argv[1],"r")
count = 0

lines = fp.read().split("\n")
lines = [line for line in lines if line!='']
lines = lines[1:]

valid_data = []
for line in lines:
	data = line.split(",")
	if len(data) == 15:
		server = data[0]
		type = data[-1]
		new_data = data[3:-1]
		#time,reqpersec,timeperreqall,timeperreq,transrate
		if ("lighttpd" in server):
			valid_data.append([new_data[2], new_data[7], new_data[8], new_data[9], new_data[10]])
			count += 1	
valid_data = np.array(valid_data,dtype="float")

#print sys.argv[1]
#print "Mean: "+str(valid_data.mean(axis=0).tolist())
#print "Stddev: "+str(valid_data.std(axis=0).tolist())

meanList = valid_data.mean(axis=0).tolist()
stddevList = valid_data.std(axis=0).tolist()

list = []

if('small' in type or 'medium' in type or 'large' in type):
	csvString = type[0:-4] + "," + "E5" + type[-4:] + "," + "0.125"
elif("nano" in server or 'micro' in server):
	temp_list = server.split("_") 
	csvString = temp_list[0] + "," + "E5" + temp_list[1] + "," + "0.125"

for mean,stddev in zip(meanList,stddevList):
	list.append(mean)
	list.append(stddev)

for i in list:
	csvString += "," + str(i)

#print count	
print csvString
