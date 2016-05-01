import os

for index in range(0,100):
	os.system("python ml_correction_input_generator.py cleanedData2.0.csv "+str(index))
