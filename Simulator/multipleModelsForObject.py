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

data_reader = csv.reader(open(sys.argv[1], "rb"))
data_reader.next()

training_data_A = [] #A = (Apache, Ng..), (L)
testing_data_A = []

training_data_B = [] #B = (Ng.., L...), (Apache)
testing_data_B = []

training_data_C = [] #C = (L.., Apache..), (Ng...)
testing_data_C = []

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
		training_data_A.append([float(x) for x in instance])
		testing_data_B.append([float(x) for x in instance])
		training_data_C.append([float(x) for x in instance])
	elif("nginx" in server):
		training_data_A.append([float(x) for x in instance])
		training_data_B.append([float(x) for x in instance])
		testing_data_C.append([float(x) for x in instance])
	else:
		testing_data_A.append([float(x) for x in instance])
		training_data_B.append([float(x) for x in instance])
		training_data_C.append([float(x) for x in instance])
	whole.append([float(x) for x in instance])

'''
#Convert to numpy
training_data_A = np.array(training_data_A,dtype="float")
training_data_B = np.array(training_data_B,dtype="float")
training_data_C = np.array(training_data_C,dtype="float")
testing_data_A = np.array(testing_data_A,dtype="float")
testing_data_B = np.array(testing_data_B,dtype="float")
testing_data_C = np.array(testing_data_C,dtype="float")
'''
whole = np.array(whole, dtype="float")

'''
np.random.shuffle(training_data_A)
np.random.shuffle(training_data_B)
np.random.shuffle(training_data_C)
np.random.shuffle(whole)
'''

input_whole_data = whole[0:len(whole),:-1]
output_whole_data = whole[0:len(whole),-1]

training_data_input, testing_data_input, training_data_output, testing_data_output = train_test_split(input_whole_data, output_whole_data, test_size=0.30, random_state=0)

RFmodel= RandomForestClassifier(n_estimators = 100)
RFmodel = RFmodel.fit(training_data_input, training_data_output)
RFaccuracy = RFmodel.score(testing_data_input, testing_data_output)
print "RF (All Data) :"+str(RFaccuracy*100.0)

'''
#Generate training data for 3 scenarios
input_training_data_A = training_data_A[0:len(training_data_A),:-1]
input_training_data_B = training_data_B[0:len(training_data_B),:-1]
input_training_data_C = training_data_C[0:len(training_data_C),:-1]
output_training_data_A = training_data_A[0:len(training_data_A),-1]
output_training_data_B = training_data_B[0:len(training_data_B),-1]
output_training_data_C = training_data_C[0:len(training_data_C),-1]

#Generate testing data for 3 scenarios
input_testing_data_A = testing_data_A[0:len(testing_data_A),:-1]
input_testing_data_B = testing_data_B[0:len(testing_data_B),:-1]
input_testing_data_C = testing_data_C[0:len(testing_data_C),:-1]
output_testing_data_A = testing_data_A[0:len(testing_data_A),-1]
output_testing_data_B = testing_data_B[0:len(testing_data_B),-1]
output_testing_data_C = testing_data_C[0:len(testing_data_C),-1]

RFmodel_A = RandomForestClassifier(n_estimators = 100)
RFmodel_A = RFmodel_A.fit(input_training_data_A,output_training_data_A)
RFaccuracy = RFmodel_A.score(input_testing_data_A,output_testing_data_A)
print "RF Train --> (A,N) Test ---> (L) :"+str(RFaccuracy*100.0)

RFmodel_B= RandomForestClassifier(n_estimators = 100)
RFmodel_B = RFmodel_B.fit(input_training_data_B,output_training_data_B)
RFaccuracy = RFmodel_B.score(input_testing_data_B,output_testing_data_B)
print "RF Train --> (N,L) Test ---> (A) :"+str(RFaccuracy*100.0)

RFmodel_C = RandomForestClassifier(n_estimators = 100)
RFmodel_C = RFmodel_C.fit(input_training_data_C,output_training_data_C)
RFaccuracy = RFmodel_C.score(input_testing_data_C,output_testing_data_C)
print "RF Train --> (L,A) Test ---> (N) :"+str(RFaccuracy*100.0)
'''

'''
with open("testOutput.m", "wb") as f:
	pickle.dump(RFmodel.fit(input_data,output_data),f)

NBmodel = MultinomialNB()
NBmodel.fit(training_data_input,training_data_output)
NBaccuracy = NBmodel.score(testing_data_input,testing_data_output)
predicted_output = NBmodel.predict(testing_data_input)
print "MultinomialNB : "+str(NBaccuracy*100.0)

NBmodel = BaggingClassifier(MultinomialNB(),max_samples=1.0, max_features=1.0)
NBmodel.fit(training_data_input,training_data_output)
NBaccuracy = NBmodel.score(testing_data_input,testing_data_output)
predicted_output = NBmodel.predict(testing_data_input)
print "Bagging MultinomialNB : "+str(NBaccuracy*100.0)

DTmodel = DecisionTreeClassifier()
DTmodel.fit(training_data_input,training_data_output)
DTaccuracy = DTmodel.score(testing_data_input,testing_data_output)
predicted_output = DTmodel.predict(testing_data_input)
print "Decision Tree : "+str(DTaccuracy*100.0)

DTmodel = BaggingClassifier(DecisionTreeClassifier(),max_samples=1.0, max_features=1.0)
DTmodel.fit(training_data_input,training_data_output)
DTaccuracy = DTmodel.score(testing_data_input,testing_data_output)
predicted_output = DTmodel.predict(testing_data_input)
print "Bagging Decision Tree : "+str(DTaccuracy*100.0)

LinearSVCmodel = LinearSVC()
LinearSVCmodel.fit(training_data_input,training_data_output)
LinearSVCaccuracy = LinearSVCmodel.score(testing_data_input,testing_data_output)
predicted_output = LinearSVCmodel.predict(testing_data_input)
print "Linear SVC : "+str(LinearSVCaccuracy*100.0)

LinearSVCmodel = BaggingClassifier(LinearSVC(),max_samples=1.0, max_features=1.0)
LinearSVCmodel.fit(training_data_input,training_data_output)
LinearSVCaccuracy = LinearSVCmodel.score(testing_data_input,testing_data_output)
predicted_output = LinearSVCmodel.predict(testing_data_input)
print "Bagging  Linear SVC : "+str(LinearSVCaccuracy*100.0)

SVCmodel = SVC()
SVCmodel.fit(training_data_input,training_data_output)
SVCaccuracy = SVCmodel.score(testing_data_input,testing_data_output)
predicted_output =SVCmodel.predict(testing_data_input)
print "SVC : "+str(SVCaccuracy*100.0)

SVCmodel = BaggingClassifier(SVC(),max_samples=1.0, max_features=1.0)
SVCmodel.fit(training_data_input,training_data_output)
SVCaccuracy = SVCmodel.score(testing_data_input,testing_data_output)
predicted_output =SVCmodel.predict(testing_data_input)
print "Bagging SVC : "+str(SVCaccuracy*100.0)
'''
