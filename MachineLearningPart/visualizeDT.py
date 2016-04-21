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
from sklearn.tree import export_graphviz
import sys

data_reader = csv.reader(open(sys.argv[1], "rb"))
data_reader.next()

data = []
for row in data_reader:
     
        type = row[-1]
        if type == 'nano':
		type = 0
	else:	
		type = 1
        #print type
	instance = [row[4], row[5], row[10],row[11],row[12],row[13],type]
	data.append([float(x) for x in instance])

data = np.array(data,dtype="float")
input_data = data[0:len(data),:-1]
output_data = data[0:len(data),-1]

training_data_input, testing_data_input, training_data_output, testing_data_output = train_test_split(input_data, output_data, test_size=0.3, random_state=0)

DTmodel = DecisionTreeClassifier()
DTmodel = DTmodel.fit(training_data_input,training_data_output)
DTaccuracy = DTmodel.score(testing_data_input,testing_data_output)
predicted_output = DTmodel.predict(testing_data_input)
print "Decision Tree : "+str(DTaccuracy*100.0)

export_graphviz(DTmodel, out_file='tree.dot', feature_names = ["Concurrency", "Time", "Req/Sec", "Time/ReqAll", "Time/Req","TransRate"], class_names = ["nano","micro"])  