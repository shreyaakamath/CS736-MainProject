import json
import sys
import os
import time

if len(sys.argv) < 3:
	print "Usage : python "+sys.argv[0]+" <binary_file> <board_size>"
	sys.exit()	

binary_file = sys.argv[1]
board_size = sys.argv[2]
nqueens_command = "./"+binary_file+" "+board_size+" > tmp.txt"
while True:
	os.system(nqueens_command)
	fp = open("tmp.txt","r");
	execution_time = fp.read().split("\n")[0]
	fp = open("nqueens_results.csv","a")
	fp.write(str(execution_time)+"\n")
	fp.close()
	
