import pickle
import csv
import sys
import numpy as np
import io

#python module expects : concurrency,time,reqpersec,timeperreqall,timerperreq,trasrate
#customer Info csv File : id, class, concurrency, time, reqpersec, timerperreq, transrate
#			  [0],[1]  , [2]        , [3] , [4]	 , [5]        , [6]
#timeperreqall = concurrency * timeperreq
print "Start of pickling"

#print sys.argv[1]
#print sys.argv[2]

data_reader = csv.reader(open(sys.argv[1], "rb"))
output_file = io.open(sys.argv[2], 'w')

#print "Before readin ML obj"
fileObj = open("testOutput", 'r')
b = pickle.load(fileObj)
#test_data = []
for row in data_reader:
	test_data = []
	csvString = ""
	custid = row[0]
	custClass = row[1] 
	concurrency = row[2] 
	time = row[3]
	reqpersec = row[4]
	timeperreq = row[5]
	transrate = row[6]
	timeperreqall = float(concurrency) * float(timeperreq)
	#instance = [row[4], row[5], row[10],row[11],row[12],row[13]]
       	instance = [concurrency, time, reqpersec, timeperreqall, timeperreq, transrate]
	test_data.append([float(x) for x in instance])
	test_data = np.array(test_data,dtype="float")
	prediction =  b.predict(test_data)
	if(prediction == 0.0):
		family = 'micro'
	elif(prediction == 1.0):
		family = 'nano'
	elif(prediction == 2.0):
		family = 'small'
	elif(prediction == 3.0):
		family = 'medium'
	elif(prediction == 4.0):
		family = 'large'
	csvString = custid + "," + custClass + "," + concurrency + "," + time + "," + reqpersec + "," + timeperreq + "," + transrate + "," + family
	output_file.write(unicode(csvString + "\n"))

output_file.close() 

print "End of pickling"
#test_data = np.array(test_data,dtype="float")
#print test_data # rt format

