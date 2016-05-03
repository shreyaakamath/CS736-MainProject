import os  
import sys

folder=sys.argv[1]
results=sys.argv[2]
for file in os.listdir(folder):
				if file.endswith("py"):
								continue
				for i in range(0,10):
								#outFile=file.split(".conf")[0]+"-trial-"+str(i)+".out"
								command="python modifiedSimulator.py "+folder+"/"+file+" >>"+results
								print command
								os.system(command)

