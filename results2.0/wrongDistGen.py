import os
import numpy as np
import sys
import csv
from sklearn import preprocessing

data_reader = csv.reader(open(sys.argv[1], "rb"))
data_reader.next()
apache2_data = []
nginx_data = []

for row in data_reader:
	server = row[0]
	type = row[-1]
	#concurrency,time,reqpersec,timeperreqall,timerperreq,trasrate,type
	if(len(row) == 15):
		instance = [row[4], row[5], row[10],row[11],row[12],row[13]]
		if ("apache2" in server):
			apache2_data.append([float(x) for x in instance])
		elif("nginx" in server):
			nginx_data.append([float(x) for x in instance])

#Initializing Scalars
apache_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))
nginx_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))

#Converting to NUMPY
apache2_data = np.array(apache2_data,dtype="float")
nginx_data = np.array(nginx_data,dtype="float")

apache2_data_input = apache2_data[0:len(apache2_data),:-1]
apache2_data_output = apache2_data[0:len(apache2_data),-1]

nginx_data_input = nginx_data[0:len(nginx_data),:-1]
nginx_data_output = nginx_data[0:len(nginx_data),-1]

apache2_data_input = apache_scaler.fit_transform(apache2_data_input)
nginx_data_input = nginx_scaler.fit_transform(nginx_data_input)

valid_data = np.concatenate((apache2_data_input,nginx_data_input))

#print "Mean: "+str(valid_data.mean(axis=0).tolist())
#print "Stddev: "+str(valid_data.std(axis=0).tolist())

meanList = valid_data.mean(axis=0).tolist()
stddevList = valid_data.std(axis=0).tolist()
list = []
#nano_2676_nginx_c_540,nginx/1.4.6,52.39.167.138,612,54,1.040,1000,0,853000,612000,961.91,56.138,1.040,801.28,nano
#micro_2670_nginx_c_540,nginx/1.4.6,52.24.180.65,612,54,5.613,10000,0,8530000,6120000,1781.53,30.311,0.561,1484.03,micro
#micro_2676_nginx_c_540,nginx/1.4.6,52.38.252.251,612,54,5.520,10000,0,8530000,6120000,1811.46,29.810,0.552,1508.96,micro
#small2670_nginx_c_540,nginx/1.4.6,52.38.234.213,612,54,0.460,1000,0,853000,612000,2172.85,24.852,0.460,1810.01,small2670
#small2676_nginx_c_720,nginx/1.4.6,52.39.163.150,612,72,0.739,1000,0,853000,612000,1352.69,53.227,0.739,1126.80,small2676
#medium2670_nginx_c_810,nginx/1.4.6,52.39.195.40,612,81,0.617,1000,0,853000,612000,1620.55,49.983,0.617,1349.93,medium2670
#medium2676_nginx_c_900,nginx/1.4.6,52.36.141.9,612,90,0.316,1000,0,853000,612000,3169.45,28.396,0.316,2640.18,medium2676
#large2676_nginx_c_750,nginx/1.4.6,52.38.147.194,612,75,0.206,1000,0,853000,612000,4851.66,15.459,0.206,4041.47,large2676

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

#print list
print csvString

'''
python cloudDistGen.py nano_2676.csv >> test.csv
python cloudDistGen.py micro_2670.csv >> test.csv
python cloudDistGen.py micro_2676.csv >> test.csv
python cloudDistGen.py small_2670.csv >> test.csv
python cloudDistGen.py small_2676.csv >> test.csv
python cloudDistGen.py medium_2670.csv >> test.csv
python cloudDistGen.py medium_2676.csv >> test.csv
python cloudDistGen.py large_2676.csv >> test.csv
'''
