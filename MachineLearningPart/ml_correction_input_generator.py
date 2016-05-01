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

trial_number = sys.argv[2]

data_reader = csv.reader(open(sys.argv[1], "rb"))
data_reader.next()

training_data_A = [] #A = (Apache, Ng..), (L)
testing_data_A = []

training_data_B = [] #B = (Ng.., L...), (Apache)
testing_data_B = []

training_data_C = [] #C = (L.., Apache..), (Ng...)
testing_data_C = []


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


#Initializing Scalars
apache_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))
nginx_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))
light_scaler = preprocessing.MinMaxScaler(feature_range=(0,10))

#Converting to NUMPY
apache2_data = np.array(apache2_data,dtype="float")
nginx_data = np.array(nginx_data,dtype="float")
light_data = np.array(light_data,dtype="float")

'''
np.random.shuffle(apache2_data)
np.random.shuffle(nginx_data)
np.random.shuffle(light_data)
'''
unscaled_light_data = light_data[:]

#Generate data
apache2_data_input = apache2_data[0:len(apache2_data),:-1]
apache2_data_output = apache2_data[0:len(apache2_data),-1]

nginx_data_input = nginx_data[0:len(nginx_data),:-1]
nginx_data_output = nginx_data[0:len(nginx_data),-1]

light_data_input = light_data[0:len(apache2_data),:-1]
light_data_output = light_data[0:len(apache2_data),-1]

#Doing the scaling
apache2_data_input = apache_scaler.fit_transform(apache2_data_input)
nginx_data_input = nginx_scaler.fit_transform(nginx_data_input)
light_data_input = light_scaler.fit_transform(light_data_input)

#Generating data
input_training_data = np.concatenate((apache2_data_input,nginx_data_input))
output_training_data = np.concatenate((apache2_data_output,nginx_data_output))

input_testing_data = light_data_input
output_testing_data = light_data_output

#Training and Outputting
RFmodel= RandomForestClassifier(n_estimators = 100)
RFmodel = RFmodel.fit(input_training_data, output_training_data)

opf_original = open("./ml_correction_input/ml_correction_original_"+trial_number+".csv","w")
opf_scaled = open("./ml_correction_input/ml_correction_scaled_"+trial_number+".csv","w")

for index in range(0,len(light_data)):
	
	unscaled = unscaled_light_data[index].tolist()
	scaled = input_testing_data[index]
	expected_output = unscaled[-1]
	predicted_output = RFmodel.predict([scaled])

	predicted_output = int(predicted_output)
	
	if predicted_output == 0:
		predicted_output = 'micro'
	elif predicted_output == 1:
		predicted_output = 'nano'
	elif predicted_output == 2:
		predicted_output = 'small'
	elif predicted_output ==3:
		predicted_output = 'medium'
	else:
		predicted_output = 'large'

	if expected_output == 0:
		expected_output = 'micro'
	elif expected_output == 1:
		expected_output = 'nano'
	elif expected_output == 2:
		expected_output = 'small'
	elif expected_output ==3:
		expected_output = 'medium'
	else:
		expected_output = 'large'


	scaled = input_testing_data[index].tolist()	
	#0,1,2,3,5
	customer_unscaled_sla = str(unscaled[0])+","+str(unscaled[1])+","+str(unscaled[2])+","+str(unscaled[3])+","+str(unscaled[5])
	customer_scaled_sla = str(scaled[0])+","+str(scaled[1])+","+str(scaled[2])+","+str(scaled[3])+","+str(scaled[5])
	unscaled_output_file = str(index)+",basic,"+customer_unscaled_sla+","+predicted_output+","+str(expected_output)
	scaled_output_file = str(index)+",basic,"+customer_scaled_sla+","+predicted_output+","+str(expected_output)

	opf_original.write(unscaled_output_file+"\n")
	opf_scaled.write(scaled_output_file+"\n")

RFaccuracy = RFmodel.score(input_testing_data, output_testing_data)
print "RF "+trial_number+":"+str(RFaccuracy*100.0)





