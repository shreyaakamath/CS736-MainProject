import sys
import csv
from itertools import islice
#python secondLevel_instMix.py inst.csv coll_True_instVar.csv

if __name__ == "__main__":

	dataFile = csv.reader(open(sys.argv[1], "rb"))
	dataFile.next()
	
	output_file = open(sys.argv[2], 'w')
	count = 0
	count_file = 0
	dictMap = {'collaboratar_status' : '', 'strategy' : '', 'T' : 0.0, 'units' : 0.0, 'A' : 0.0, 'B' : 0.0, 'm' : 0.0, 'mu' : 0.0, 'c' : 0.0, 'cu' : 0.0, 'no_instances' : 0.0, 'good_rank' : 0.0, 'good_frac' : 0.0, 'good_mean' : 0.0, 'good_stddev' : 0.0, 'bad_rank' : 0.0, 'bad_frac' : 0.0, 'bad_mean' : 0.0, 'bad_stddev' : 0.0, 'Unnecessary_work' : 0.0, 'no_instances_used' : 0.0, 'no_migrations' : 0.0, 'no_collaboration_works' : 0.0, 'total_work' : 0.0, 'effective_perf_rate' : 0.0, 'naive_total_work' : 0.0, 'naive_effective_rate' : 0.0, 'speedup' : 0.0, 'percentage_improvement' : 0.0}
	
	for row in dataFile:
		if ("True" in row[0]) :
			if ((count % 10) == 0 and (count != 0)): #start of a new combo
				dictMap['collaboratar_status'] = str(row[0]) 
				dictMap['strategy'] = str(row[1])  
				dictMap['T'] /= float(10.0) 
				dictMap['units'] /= float(10.0) 
				dictMap['A'] /= float(10.0) 
				dictMap['B'] /= float(10.0) 
				dictMap['m'] /= float(10.0) 
				dictMap['mu'] /= float(10.0)
				dictMap['c'] /= float(10.0) 
				dictMap['cu'] /= float(10.0) 
				dictMap['no_instances'] /= float(10.0) 
				dictMap['good_rank'] /= float(10.0) 
				dictMap['good_frac'] /= float(10.0) 
				dictMap['good_mean'] /= float(10.0) 
				dictMap['good_stddev'] /= float(10.0)
				dictMap['bad_rank'] /= float(10.0) 
				dictMap['bad_frac'] /= float(10.0) 
				dictMap['bad_mean'] /= float(10.0) 
				dictMap['bad_stddev'] /= float(10.0) 
				dictMap['Unnecessary_work'] /= float(10.0) 
				dictMap['no_instances_used'] /= float(10.0)
				dictMap['no_migrations'] /= float(10.0) 
				dictMap['no_collaboration_works'] /= float(10.0) 
				dictMap['total_work'] /= float(10.0) 
				dictMap['effective_perf_rate'] /= float(10.0)
				dictMap['naive_total_work'] /= float(10.0) 
				dictMap['naive_effective_rate'] /= float(10.0) 
				dictMap['speedup'] /= float(10.0) 
				dictMap['percentage_improvement'] /= float(10.0) 
				csvString = str(dictMap['collaboratar_status'])  + ',' + str(dictMap['strategy'])  + ',' + str(dictMap['T'])  + ',' + str(dictMap['units'])  + ',' + str(dictMap['A'])  + ',' + str(dictMap['B'])  + ',' + str(dictMap['m'])  + ',' + str(dictMap['mu'])  + ',' + str(dictMap['c'])  + ',' + str(dictMap['cu'])  + ',' + str(dictMap['no_instances'])  + ',' + str(dictMap['good_rank'])  + ',' + str(dictMap['good_frac'])  + ',' + str(dictMap['good_mean'])  + ',' + str(dictMap['good_stddev'])  + ',' +str(dictMap['bad_rank'])  + ',' + str(dictMap['bad_frac'])  + ',' + str(dictMap['bad_mean'])  + ',' + str(dictMap['bad_stddev'])  + ',' + str(dictMap['Unnecessary_work'])  + ',' + str(dictMap['no_instances_used'])  + ',' + str(dictMap['no_migrations'])  + ',' + str(dictMap['no_collaboration_works'])  + ',' + str(dictMap['total_work'])  + ',' + str(dictMap['effective_perf_rate'])  + ',' + str(dictMap['naive_total_work'])  + ',' + str(dictMap['naive_effective_rate'])  + ',' + str(dictMap['speedup'])  + ',' + str(dictMap['percentage_improvement'])
				#print csvString
				output_file.write(csvString + '\n')
				#count_file += 1
				
				dictMap['collaboratar_status'] = row[0]
				dictMap['strategy'] = str(row[1]) 
				dictMap['T'] = float(row[2]) 
				dictMap['units'] = float(row[3])
				dictMap['A'] = float(row[4])
				dictMap['B'] = float(row[5])
				dictMap['m'] = float(row[6])
				dictMap['mu'] = float(row[7])
				dictMap['c'] = float(row[8])
				dictMap['cu'] = float(row[9])
				dictMap['no_instances'] = float(row[10])
				dictMap['good_rank'] = float(row[11])
				dictMap['good_frac'] = float(row[12])
				dictMap['good_mean'] = float(row[13])
				dictMap['good_stddev'] = float(row[14])
				dictMap['bad_rank'] = float(row[15])
				dictMap['bad_frac'] = float(row[16])
				dictMap['bad_mean'] = float(row[17])
				dictMap['bad_stddev'] = float(row[18])
				dictMap['Unnecessary_work'] = float(row[19])
				dictMap['no_instances_used'] = float(row[20])
				dictMap['no_migrations'] = float(row[21])
				dictMap['no_collaboration_works'] = float(row[22])
				dictMap['total_work'] = float(row[23])
				dictMap['effective_perf_rate'] = float(row[24])
				dictMap['naive_total_work'] = float(row[25])
				dictMap['naive_effective_rate'] = float(row[26])
				dictMap['speedup'] = float(row[27])
				dictMap['percentage_improvement'] = float(row[28])
				
				count += 1
				#print "In IF" + str(count)
			else :
				dictMap['collaboratar_status'] = row[0]
				dictMap['strategy'] = str(row[1]) 
				dictMap['T'] += float(row[2]) 
				dictMap['units'] += float(row[3])
				dictMap['A'] += float(row[4])
				dictMap['B'] += float(row[5])
				dictMap['m'] += float(row[6])
				dictMap['mu'] += float(row[7])
				dictMap['c'] += float(row[8])
				dictMap['cu'] += float(row[9])
				dictMap['no_instances'] += float(row[10])
				dictMap['good_rank'] += float(row[11])
				dictMap['good_frac'] += float(row[12])
				dictMap['good_mean'] += float(row[13])
				dictMap['good_stddev'] += float(row[14])
				dictMap['bad_rank'] += float(row[15])
				dictMap['bad_frac'] += float(row[16])
				dictMap['bad_mean'] += float(row[17])
				dictMap['bad_stddev'] += float(row[18])
				dictMap['Unnecessary_work'] += float(row[19])
				dictMap['no_instances_used'] += float(row[20])
				dictMap['no_migrations'] += float(row[21])
				dictMap['no_collaboration_works'] += float(row[22])
				dictMap['total_work'] += float(row[23])
				dictMap['effective_perf_rate'] += float(row[24])
				dictMap['naive_total_work'] += float(row[25])
				dictMap['naive_effective_rate'] += float(row[26])
				dictMap['speedup'] += float(row[27])
				dictMap['percentage_improvement'] += float(row[28])
				count += 1
			#print "In Else:" + str(count)
	#print "Count File:" + str(count_file)
	
	output_file.close()

