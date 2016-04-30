import os 

for file in os.listdir("confFiles"):
				for i in range(0,10):
								outFile=file.split(".conf")[0]+"-trial-"+str(i)+".out"
								command="python simulator_withFamily_withColl.py confFiles/"+file+" >> output/"+outFile
								print command
								os.system(command)

