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

data_reader = csv.reader(open(sys.argv[1], "rb"))
data_reader.next()

data = []
for row in data_reader:
     
        type = row[-1]
        #if type == 'nano':
	if(str(type).startswith("micro")):
		type = 0
	elif(str(type).startswith("nano")):
		type = 1	
	
	elif(str(type).startswith("small")):
		type = 2
        #print type
	instance = [row[4], row[5], row[10],row[11],row[12],row[13],type]
	data.append([float(x) for x in instance])

#print data[0]
print data
'''
min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(data)
'''

data = np.array(data,dtype="float")
#from random import shuffle
#np.random.shuffle(data)

input_data = data[0:len(data),:-1]
output_data = data[0:len(data),-1]

#print input_data[0]
#print output_data[0]

training_data_input, testing_data_input, training_data_output, testing_data_output = train_test_split(input_data, output_data, test_size=0.95, random_state=0)

print len(training_data_input)
print len(testing_data_input)

RFmodel = RandomForestClassifier(n_estimators = 100)
RFmodel.fit(training_data_input,training_data_output)
RFaccuracy = RFmodel.score(testing_data_input,testing_data_output)
predicted_output = RFmodel.predict(testing_data_input)
print predicted_output
print "RFs :"+str(RFaccuracy*100.0)

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






