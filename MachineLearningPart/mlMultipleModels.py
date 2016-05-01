import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.cross_validation import cross_val_predict
from sklearn import preprocessing
import sys
import pickle
import io

data_reader = csv.reader(open(sys.argv[1], "rb"))
data_reader.next()

output_file = io.open(sys.argv[2], 'w')

apache2_data = []
nginx_data = []
light_data = []
whole = []
for row in data_reader:
	server = row[0]
	type = row[-1]
	if('micro' in str(type)):	
		type = 0
	elif('nano' in str(type)):
		type = 1	
	elif('small' in str(type)):
		type = 2
	elif('medium' in str(type)):
		type = 3
	elif('large' in str(type)):
		type = 4
	#concurrency,time,reqpersec,timeperreqall,timerperreq,trasrate,type
	instance = [row[4], row[5], row[10],row[11],row[12],row[13],type]
	if ("apache2" in server):
		apache2_data.append([float(x) for x in instance])
	elif("nginx" in server):
		nginx_data.append([float(x) for x in instance])
	else:
		light_data.append([float(x) for x in instance])

	whole.append([float(x) for x in instance])

apache_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))
nginx_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))
light_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))

apache2_data = np.array(apache2_data,dtype="float")
nginx_data = np.array(nginx_data,dtype="float")
light_data = np.array(light_data,dtype="float")

apache2_data_input = apache2_data[0:len(apache2_data),:-1]
apache2_data_output = apache2_data[0:len(apache2_data),-1]

nginx_data_input = nginx_data[0:len(nginx_data),:-1]
nginx_data_output = nginx_data[0:len(nginx_data),-1]

light_data_input = light_data[0:len(apache2_data),:-1]
light_data_output = light_data[0:len(apache2_data),-1]

print "Apache: " + str(len(apache2_data_input)) + "Nginx: " + str(len(nginx_data_input)) + "Light: " + str(len(light_data_input))
apache2_data_input = apache_scaler.fit_transform(apache2_data_input)
nginx_data_input = nginx_scaler.fit_transform(nginx_data_input)
light_data_input = light_scaler.fit_transform(light_data_input)

training_data_input = np.concatenate((apache2_data_input,nginx_data_input))
training_data_output = np.concatenate((apache2_data_output,nginx_data_output))

testing_data_input = light_data_input
testing_data_output = light_data_output

rfAcc=mnb=bagMnb=dt=bagDt=lSvc=baglSvc=svc=bagSvc = 0
 
#with open("testOutput.m", "wb") as f:
#        pickle.dump(RFmodel.fit(input_data,output_data),f)
csvString = "RF" + "," + "MNB" + "," + "BagMNB" + "," + "DT" + "," + "BagDT" + "," + "LSVC" + "," + "BagLSVC" + "," + "SVC" + "," + "BagSVC" 
output_file.write(unicode(csvString + "\n"))

for i in range(50):
	csvString = ""
	RFmodel= RandomForestClassifier(n_estimators = 100)
	RFmodel = RFmodel.fit(training_data_input, training_data_output)
	RFaccuracy = RFmodel.score(testing_data_input, testing_data_output)
	#print "RF train(A,N)->test(L) :"+str(RFaccuracy*100.0)
	csvString += str(RFaccuracy*100.0) + ","
	rfAcc += RFaccuracy*100.0 
	
	NBmodel = MultinomialNB()
	NBmodel.fit(training_data_input,training_data_output)
	NBaccuracy = NBmodel.score(testing_data_input,testing_data_output)
	predicted_output = NBmodel.predict(testing_data_input)
	#print "MultinomialNB : "+str(NBaccuracy*100.0)
	csvString += str(NBaccuracy*100.0) + ","
	mnb += NBaccuracy*100.0	

	NBmodel = BaggingClassifier(MultinomialNB(),max_samples=1.0, max_features=1.0)
	NBmodel.fit(training_data_input,training_data_output)
	NBaccuracy = NBmodel.score(testing_data_input,testing_data_output)
	predicted_output = NBmodel.predict(testing_data_input)
	#print "Bagging MultinomialNB : "+str(NBaccuracy*100.0)
	csvString += str(NBaccuracy*100.0) + ","
	bagMnb += NBaccuracy*100.0
	
	DTmodel = DecisionTreeClassifier()
	DTmodel.fit(training_data_input,training_data_output)
	DTaccuracy = DTmodel.score(testing_data_input,testing_data_output)
	predicted_output = DTmodel.predict(testing_data_input)
	#print "Decision Tree : "+str(DTaccuracy*100.0)
	csvString += str(DTaccuracy*100.0) + ","
	dt += DTaccuracy*100.0
	
	DTmodel = BaggingClassifier(DecisionTreeClassifier(),max_samples=1.0, max_features=1.0)
	DTmodel.fit(training_data_input,training_data_output)
	DTaccuracy = DTmodel.score(testing_data_input,testing_data_output)
	predicted_output = DTmodel.predict(testing_data_input)
	#print "Bagging Decision Tree : "+str(DTaccuracy*100.0)
	csvString += str(DTaccuracy*100.0) + ","
	bagDt += DTaccuracy*100.0
	
	LinearSVCmodel = LinearSVC()
	LinearSVCmodel.fit(training_data_input,training_data_output)
	LinearSVCaccuracy = LinearSVCmodel.score(testing_data_input,testing_data_output)
	predicted_output = LinearSVCmodel.predict(testing_data_input)
	#print "Linear SVC : "+str(LinearSVCaccuracy*100.0)
	csvString += str(LinearSVCaccuracy*100.0) + ","
	lSvc += LinearSVCaccuracy*100.0 
	
	LinearSVCmodel = BaggingClassifier(LinearSVC(),max_samples=1.0, max_features=1.0)
	LinearSVCmodel.fit(training_data_input,training_data_output)
	LinearSVCaccuracy = LinearSVCmodel.score(testing_data_input,testing_data_output)
	predicted_output = LinearSVCmodel.predict(testing_data_input)
	#print "Bagging  Linear SVC : "+str(LinearSVCaccuracy*100.0)
	csvString += str(LinearSVCaccuracy*100.0) + ","
	baglSvc += LinearSVCaccuracy*100.0
	
	SVCmodel = SVC()
	SVCmodel.fit(training_data_input,training_data_output)
	SVCaccuracy = SVCmodel.score(testing_data_input,testing_data_output)
	predicted_output =SVCmodel.predict(testing_data_input)
	#print "SVC : "+str(SVCaccuracy*100.0)
	csvString += str(SVCaccuracy*100.0) +","
	svc += SVCaccuracy*100.0
	
	SVCmodel = BaggingClassifier(SVC(),max_samples=1.0, max_features=1.0)
	SVCmodel.fit(training_data_input,training_data_output)
	SVCaccuracy = SVCmodel.score(testing_data_input,testing_data_output)
	predicted_output =SVCmodel.predict(testing_data_input)
	#print "Bagging SVC : "+str(SVCaccuracy*100.0)
	csvString += str(SVCaccuracy*100.0) + "\n"
	bagSvc += SVCaccuracy*100.0
	
	output_file.write(unicode(csvString))

print "RF" + "," + "MNB" + "," + "BagMNB" + "," + "DT" + "," + "BagDT" + "," + "LSVC" + "," + "BagLSVC" + "," + "SVC" + "," + "BagSVC" 
accuracyTotalList = [rfAcc,mnb,bagMnb,dt,bagDt,lSvc,baglSvc,svc,bagSvc]
print accuracyTotalList

accuracyList = [x/50.0 for x in accuracyTotalList]
print  sorted(accuracyList)

output_file.close() 
