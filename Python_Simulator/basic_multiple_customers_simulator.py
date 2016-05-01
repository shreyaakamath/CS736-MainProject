import os
import sys
import struct
from math import sqrt, log, cos
import copy
import operator
import numpy
import random

#Constants that will be used
WORK_PER_UNIT = 20000
MAX_INSTANCE_TYPES = 100
MAX_INSTANCES = 1000
MAX_TIME_QUANTUMS = 1000
MAX_LINE = 1000

RAND_MAX = 4294967295
PI = 3.14159265358979323846

START_INSTANCE_EVENT_STR = "launch instance"
KILL_INSTANCE_EVENT_STR = "kill instance"
MIGRATED_EVENT_STR = "migrate instance"

DEBUG = 2 # Set to 1 to print Debug statements, else set to 0 for no print statements or set to 2 for Log statements

class Instance_type:

	def __init__(self, rank, frac, mean, stddev):
		self.rank = rank #Rank 0 is the highest
		self.frac = frac  #Fraction of instances of this type
		self.mean = mean  #The mean for normal distribution dictating performance
		self.stddev = stddev #The standard deviation for normal distribution dictating performance

	def __str__(self):

		output = []
		for key in ["rank", "frac", "mean", "stddev"]:
			output.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
		return ', '.join(output)



class Instance:

	def __init__(self, id, type, active, start_time,perf_array, end_time = 0, total_time = 0, total_time_computation = 0, total_work = 0, avg_perf = 0):
		self.id = id #Similar to serial number --- Starts from 0 and increases
		self.type = type #??
		self.active = active #1 indicates instance being used, 0 indicates instance not being used
 		self.start_time = start_time #Start time in seconds (units)
		self.end_time = end_time #End time in seconds (units)
		self.total_time = total_time #Subtraction of the above to attributes (gives answer in seconds) 
		self.total_time_computation = total_time_computation #Takes the migration penalty into account
		self.total_work = total_work #Total work done by the instance -- calculated on killing of instance
		self.avg_perf = avg_perf #Average performance of the instance -- calculated on killing of instance
		self.perf_array = perf_array # 'T' dimensional array where each element is the performance rate for each hour from 0...T-1
		self.perf_first = perf_array[0] #Stores perf for 1st quantum
	def __repr__(self):
		return 'Instance(id={}, type={}, active={}, start_time={},end_time={}, total_time={}, total_time_computation={}, total_work={}, avg_perf={}, perf_array={})'.format(
			self.id, self.type, self.active, self.start_time, self.end_time, self.total_time, self.total_time_computation, self.total_work, self.avg_perf,self.perf_array)

def gen_std_normal():
	return random.gauss(0,1)

def get_rand():
	return random.random()

'''
def get_rand():
	fp = open("/dev/urandom", "rb")
	return struct.unpack("I", fp.read(4))[0]
	fp.close()
def gen_std_normal():

  u1 = get_rand() / float(RAND_MAX)
  u2 = get_rand() / float(RAND_MAX)
  x = sqrt(-2 * log(u1)) * cos(2 * PI *u2)

  if(DEBUG == 1):
  	print("******** gen_std_normal O/P *********")
  	print("u1: "+str(u1))
  	print("u2: "+str(u2))
  	print("x: "+str(x))
  	print("*************************************")

  return x
'''

def log_event(instance_id, time_sec, event):
	if (DEBUG == 2):
		print(str(time_sec)+"\t\t\t"+str(instance_id)+"\t\t"+str(event))

#Could just be an array right?
strategies = {
	
	0 : "CPU", #Upfront A+B exploration, pick based on CPU type
	1 : "UPFRONT", #Upfront A+B exploration, pick based on first quantum perf
	2 : "UPFRONT_OPREP", #Upfront A+B exploration, pick based on first quantum perf, and do oportunistic replacement based on first quantum average
	3 : "CPU_OPREP" #Upfront A+B exploration, pick based on CPU type and do opportunistic replacement using predefined CPU averages to determine current instance's perf and average perf
}

class Customer:

	def __init__(self, config_filename):
		self.config_filename = config_filename #Name of config file
		self.instanceTypes = [] #Array to hold objs of clas Instance_type
		self.instances = [] #Array to hold objs of class Instance
		self.naive_instances = [] #Array to hold objs of class Instance and for naive strategy
		self.num_instance_types = 0 #Count for number of different instance types based on config file
		self.total_num_instances = 0 #Count total machines launched during entire run

		self.strategy = ""
		self.T = 0 #max number time quantum (aka hours)
		self.units = 0 #one quantum == 'units' seconds
		self.A = 0 #number of instances to keep running in quantums > 1
		self.B = 0 #number of exploratory instances to run in quantum 1
		self.m = 0 #migration penalty in seconds
		self.mu = 0 #expected number of remigrations (we can calculate this as well)

		self.config_loader()

	def config_loader(self):
		
		fp = open(self.config_filename,"r")
		lines = fp.read().split("\n")
		lines = [line for line in lines if line!=""]

		self.strategy, self.T, self.units, self.A, self.B, self.m, self.mu = [float(x) for x in lines[0].split(",")]
		self.T = int(self.T)
		self.A = int(self.A)
		self.B = int(self.B)

		self.strategy = strategies[int(self.strategy)] #Just getting the string name of strategy
		lines = lines[1:] #As parsed the first line

		rank_count = 0
		for line in lines:
			record = line.split(",") #Ignore processor which is nothing but record[0]
			record = [x for x in record if x!=""]
			instType_obj = Instance_type(rank_count, float(record[1]), float(record[2]), float(record[3]))
			self.instanceTypes.append(instType_obj)
			rank_count += 1
			self.num_instance_types += 1

		if (DEBUG == 1 or DEBUG == 2):
			print("********* Contents of Configuration File *********")
			print("Strategy: "+self.strategy)
			print("T: "+str(self.T))
			print("units: "+str(self.units))
			print("A: "+str(self.A))
			print("B: "+str(self.B))
			print("m: "+str(self.m))
			print("mu: "+str(self.mu))
			print("Number of instances: "+str(self.num_instance_types))
			for instance in self.instanceTypes:
				print instance
			print("**************************************************")

	def launch_instance(self,instance_id, time):
		
		self.total_num_instances += 1 #Increment total count 
		
		cumFrac = 0
		#ranFrac = (1 - float(get_rand()) / float(RAND_MAX)) #Get random fraction
		ranFrac = get_rand()
		print ranFrac
		for i in range(0,self.num_instance_types):
			cumFrac += self.instanceTypes[i].frac
			if (ranFrac <= cumFrac):
				whichRank = i #Decide which CPU/Processor type
				break

		perf_array = [] #Calculate perf array
		for i in range(0,self.T):
			perf_array.append((self.instanceTypes[whichRank].stddev + gen_std_normal()) + self.instanceTypes[whichRank].mean)

		if(DEBUG == 1):
			print("LAUNCHING Instance "+str(instance_id))+", type "+str(whichRank)+", perf "+str(perf_array) 
	
		log_event(instance_id, time/self.units, START_INSTANCE_EVENT_STR)

		instance_obj = Instance(instance_id, whichRank, 1, time,perf_array)
		self.instances.append(instance_obj)

	def kill_instance(self,instance_id, time, naive_instance = False):
		
		# ASSUMING index == instance_id ::::: Is it always true??
		if naive_instance == True:
			instance_obj = self.naive_instances[instance_id]
		else:
			instance_obj = self.instances[instance_id] #Getting a shallow copy
 		instance_obj.end_time = time
		instance_obj.total_time = instance_obj.end_time - instance_obj.start_time
		instance_obj.total_time_computation = instance_obj.total_time - self.m 
		instance_obj.active = 0
		instance_obj.total_work = 0

		#Logic to calculate work
		t = 0
		i = 0
		while(t < instance_obj.total_time_computation):

			if(t == 0):
				instance_obj.total_work += (self.units - self.m) * instance_obj.perf_array[i]
				t += self.units - self.m
			else:
				instance_obj.total_work += self.units * instance_obj.perf_array[i]
				t += self.units

			i += 1

		instance_obj.avg_perf = instance_obj.total_work / instance_obj.total_time
		log_event(instance_obj.id, time/self.units, KILL_INSTANCE_EVENT_STR)

	def simulate(self):
		#REMEMBER: To do GLOBAL for all variables above incase you want to modify them 
		print("Time(sec)\t\tID\t\tEvent")
		time = 0 #Running time in seconds
		whichType = 0 #Processor type
		i = 0 #Looper
		j = 0 #Looper
		num_instances = 0 #Total number of instances launched during runtime
		total_work = 0
		aggregate_perf = 0
		naive_total_work = 0
		naive_aggregate_perf = 0
		cur_perf = 0
		num_active = 0
		first_avg = 0
		stddev = 0
		delta = 0
		num_migrated = 0

		#Start with launching A+B instances and setting up the first average
		for i in range(0,self.A+self.B):
			self.launch_instance(i, time)
			num_instances += 1
			first_avg += self.instances[i].perf_array[0] #This is the first average for Performance based strategies

		if (self.strategy == "CPU_OPREP"):
			first_avg = 0
			for i in range(0,self.num_instance_types):
				first_avg += self.instanceTypes[i].mean #This is the first average for CPU based strategies
			first_avg = first_avg / self.num_instance_types
		else:
			first_avg = first_avg / (self.A+self.B)

		#Copy over first A units for Naive strategy
		self.naive_instances = copy.deepcopy(self.instances[:self.A])
		time += self.units

		#Up-front exploration ends
		if (self.T > 0 and self.B > 0):
			if (self.strategy == "CPU"):
				self.instances = sorted(self.instances, key = operator.attrgetter('type'), reverse = False)
			elif (self.strategy == "UPFRONT" or self.strategy == "UPFRONT_OPREP"):
				self.instances = sorted(self.instances, key = operator.attrgetter('perf_first'), reverse = True)

			#Kill B bad instances for all strategies
			for i in range(self.A,self.A+self.B):
				self.kill_instance(i, time)

		#Working with best A as of now, and do opportunistic replacements for *seemingly* bad ones
		if (self.strategy in ['CPU_OPREP', 'UPFRONT_OPREP']):
			#Quantums 2 and on, perform opportunistic replacement
			for i in range(1, self.T-1):
				time += self.units
				delta = self.mu * (self.m/float(self.units)) / (self.T - i)
				num_migrated = 0

				for j in range(0, num_instances):

					if (self.instances[j].active == 1):

						if(self.strategy == "CPU_OPREP"):
							cur_perf = self.instanceTypes[self.instances[j].type].mean
						else:
							cur_perf = self.instances[j].perf_array[i]

						if (first_avg - cur_perf > delta):
							#print ("MIGRATING type "+str(instances[j].type)+" because ("+str(first_avg)+" - "+str(cur_perf)+" > "+str(delta))
							log_event(self.instances[j].id, time/self.units, MIGRATED_EVENT_STR)
							self.launch_instance(num_instances + num_migrated, time)
							num_migrated += 1
							self.kill_instance(j, time)
				num_instances += num_migrated
			time += self.units
		else:
			time += self.units * (self.T - 1)

		for i in range(0, num_instances):
			if (self.instances[i].active == 1):
				self.kill_instance(i, time)
			total_work += self.instances[i].total_work

		print ("Done with current strategy, killing naive instances...")
		#Calculate total work done for naive instances
		time = self.units*self.T
		for i in range(0,self.A):
			self.kill_instance(i, time, True)
			naive_total_work += self.naive_instances[i].total_work

		aggregate_perf = total_work / float((self.A*self.T+self.B) * self.units)
		naive_aggregate_perf = naive_total_work / float((self.A*self.T) * self.units)

		print("Total Number of instances used: "+str(num_instances))
		print("Number of migrations: "+str(num_instances - self.A - self.B))
		print("Total work: "+str(total_work))
		print("Effective Perf Rate: "+str(aggregate_perf))
		print("Naive total work: "+str(naive_total_work))
		print("Naive effective rate: "+str(naive_aggregate_perf))

		speedup = aggregate_perf / naive_aggregate_perf
		print("Speedup: "+str(speedup))

		percentage_improvement = ((aggregate_perf/naive_aggregate_perf) - 1) * 100
		print("Percentage-Improvement: "+str(percentage_improvement))
		if(DEBUG == 1):
			print "Strategy is : "+strategy


if __name__ == "__main__":

	customer = Customer("ner1-config")
	customer.simulate()


