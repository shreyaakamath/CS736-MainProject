#!/usr/python
import csv
import os
import io
import sys

if __name__ == '__main__':
    
    input_file = sys.argv[1]
    output_file = io.open(sys.argv[2],'a')			
    try :
            with open(input_file, 'r') as csvfile:
                for eachRow in csvfile:
		    row = eachRow.split(',')
		    if(len(row) == 15):
			#print row
			csvString = ', '.join(row)
			output_file.write(unicode(csvString))
	    output_file.close()		    
    except Exception,e:
        print e    
            
