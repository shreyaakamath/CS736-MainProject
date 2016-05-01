import csv
import sys
import random

class Customer:
	
	def __init__(self, params):
		self.id = params[0]
		self.custClass = params[1]
		self.concurrency = params[2]
		self.time = params[3]
		self.reqpersec = params[4]
		self.timeperreq = params[5]
		#timeperreqall = concurrency * timeperreq
		self.timeperreqall= float(params[2]) * float(params[5])
		self.transrate = params[6]
		self.family = params[7]
		
		
	def __str__(self):
		output = []
		for key in ["id","custClass","concurrency","time","reqpersec","timeperreq","timeperreqall","transrate","family"]:
			output.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
		return ', '.join(output)
		
		
class Distribution:
	
	def __init__(self,family,proc,fraction,time_mean,time_stddev,rps_mean,rps_stddev,timeprall_mean,timeprall_stddev,timepr_mean,timepr_stddev,transrate_mean,transrate_stddev,priority):
		self.family = family
		self.proc = proc
		self.fraction = fraction
		#Each Parameter affect systems directly or indirectly
		#SLAs which are inversely proportional to system performance
		self.time_mean = time_mean
		self.time_stddev = time_stddev
		self.timeprall_mean = timeprall_mean
		self.timeprall_stddev = timeprall_stddev
		self.timepr_mean = timepr_mean
		self.timepr_stddev = timepr_stddev
		#SLAs which are directly proportional to system performance
		self.rps_mean = rps_mean
		self.rps_stddev = rps_stddev
		self.transrate_mean = transrate_mean
		self.transrate_stddev = transrate_stddev
		self.priority = priority
		
	def __str__(self):
		output = []
		for key in ["family","proc","fraction","time_mean","time_stddev","rps_mean","rps_stddev","timeprall_mean","timeprall_stddev","timepr_mean","timepr_stddev","transrate_mean","transrate_stddev"]:
			output.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
		return ', '.join(output)

def rank_max_similarity(customer, vmInstances):
	#print customer
	list = []
	for eachVM in vmInstances:
		#print eachVM.priority
		count = 0
		if (float(customer.time) < (float(eachVM.time_mean) + float(eachVM.time_stddev)) and float(customer.time) > (float(eachVM.time_mean) - float(eachVM.time_stddev))):
			count += 1
		if (float(customer.reqpersec) < (float(eachVM.rps_mean) + float(eachVM.rps_stddev)) and float(customer.reqpersec) > (float(eachVM.rps_mean) - float(eachVM.rps_stddev))):
			count += 1
		if (float(customer.timeperreq) < (float(eachVM.timepr_mean) + float(eachVM.timepr_stddev)) and float(customer.timeperreq) > (float(eachVM.timepr_mean) - float(eachVM.timepr_stddev))):
			count += 1
		if (float(customer.timeperreqall) < (float(eachVM.timeprall_mean) + float(eachVM.timeprall_stddev)) and float(customer.timeperreqall) > (float(eachVM.timeprall_mean) - float(eachVM.timeprall_stddev))):
			count += 1
		if(float(customer.transrate) < (float(eachVM.transrate_mean) + float(eachVM.transrate_stddev)) and float(customer.transrate) > (float(eachVM.transrate_mean) - float(eachVM.transrate_stddev))):
			count += 1
		list.append([count,eachVM.priority,eachVM])
	print list
	sortedList = sorted(list, key=lambda x: (-x[0], x[1]))
	print sortedList[0]
	return sortedList[0][-1]
	print "End of rank similarity"
		
		
	
#static we compare with entire cloudDist file eachVM.e: across all families and processors
#dynamic we compare with only subset of the instances whose family is same as family of the instance currently the customer is running on
if __name__ == "__main__":
	
	completeInstancesList = []
	familyCloudDist = dict()
	procDict = dict()
	#higher priority for lesser cost system
	CostPriorityDict = {'nano':1, 'micro':2, 'small':3, 'medium':4, 'large':5} 
	
	#custInfoAfterPredictFile - id,class,concurrency,time,reqpersec,timerperreq,transrate,family
	customers = []
	custInfoAfterPredictFile = csv.reader(open(sys.argv[2], "r"))
	for eachCustStats in custInfoAfterPredictFile:
		customer = Customer(eachCustStats)
		customers.append(customer)
			
	#cloudDistFile - family,proc,fraction,time_mean,time_stddev,rps_mean,rps_stddev,timeprall_mean,timeprall_stddev,timepr_mean,time_pr_stddev,transrate_mean,transrate_stddev
	cloudDistfile = csv.reader(open(sys.argv[1], "rb"))
	cloudDistfile.next()	
	for row in cloudDistfile:

		family = row[0]
		proc = row[1]
		vmInstance = Distribution(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],CostPriorityDict.get(family))
		completeInstancesList.append(vmInstance)
		if family in familyCloudDist.keys():
			procDict = familyCloudDist.get(family)
			procDict[proc] = vmInstance
			familyCloudDist[family] = procDict
			
		else:
			#print "First encounter of " + family
			procDict = dict()
			procDict[proc] = vmInstance
			familyCloudDist[family] = procDict
	
	#-----static check-----
	for eachCust in customers:
		preferredInstance = rank_max_similarity(eachCust, completeInstancesList)
		#print preferredInstance
	
	#-----dynamic check----- 
	#to be called at the beginning of every launch by comparing dynamically collected high level SLAs by various sys monitors running on each instance
	for eachCust in customers:
		vmSubsetInstances = []
		for i in familyCloudDist.get(eachCust.family):
			vmSubsetInstances.append(familyCloudDist.get(eachCust.family).get(i))
		preferredInstance = rank_max_similarity(eachCust, vmSubsetInstances)
		#print preferredInstance


	
