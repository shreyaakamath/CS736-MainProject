import csv
import sys

strategies = {
    0 : "CPU", #Upfront A+B exploration, pick based on CPU type
    1 : "UPFRONT", #Upfront A+B exploration, pick based on first quantum perf
    2 : "UPFRONT_OPREP", #Upfront A+B exploration, pick based on first quantum perf, and do oportunistic replacement based on first quantum average
    3 : "CPU_OPREP" #Upfront A+B exploration, pick based on CPU type and do opportunistic replacement using predefined CPU averages to determine current instance's perf and average perf
}
   
   
if __name__ == "__main__":
    
    '''
    runParams will be first line of the config file
    format - strategy,time,quantum,A,B,migrationPenality,expectedNoOfReMig,alphaAgg,alphaServ, colProb, cu-maxNoofPremp, collSwitch
    sample - 2,24,3600,10,10,180,2,0,1,x,y
    '''
    T = 24
    quantum = 3600
    A_values = [10,20]
    B_values = [0,5,10,20,40,60,80,120]
    migrationPenalty = 180
    expectedMig = 2
    alphaAgg = 0
    alphaServ = 1 
    mean_good = 10
    stddev_good = float(0.05*mean_good)
    mean_bad = [9,8,7,6,5] #varying from 10% to 50% of mean_good
    #stddev_bad = [float(0.05*x) for x in mean_bad]
    #good and bad machines have equal distribution
    good_frac = 0.5 
    bad_frac = 0.5
    colProb = [float(0.5*good_frac),float(1.5*good_frac)]
    cu = [1,2,3,4,5,6,7,8,9,10]
    
    runParams = ""
    count = 0
    for strategy in strategies.iterkeys():
        if (strategy == 0):
            colSwitch = 'False'
            colProbVal = 0
            cuVal = 0
            for A in A_values:
                for B in B_values:
                    runParams = str(strategy) + "," + str(T) + "," + str(quantum) + "," + str(A) + "," + str(B) + "," + str(migrationPenalty) + "," + str(expectedMig) + "," + str(colProbVal) + "," + str(cuVal) + "," + str(colSwitch) + "\n"
                    good_line = "good" + "," + str(good_frac) + "," + str(mean_good) + "," + str(stddev_good) + "\n"
                    for mean_bad_value in mean_bad:
                        bad_line = "bad" + "," + str(bad_frac) + "," + str(mean_bad_value) + "," + str(float(0.05*mean_bad_value)) + "\n"
                        count += 1
                        output_file = open(str(count), 'w')
                        output_file.write(unicode(runParams))
                        output_file.write(unicode(good_line))
                        output_file.write(unicode(bad_line))
                        output_file.close()
                        
        elif (strategy == 1):
            colSwitch = 'False'
            colProbVal = 0
            cuVal = 0
            for A in A_values:
                for B in B_values:
                    runParams = str(strategy) + "," + str(T) + "," + str(quantum) + "," + str(A) + "," + str(B) + "," + str(migrationPenalty) + "," + str(expectedMig) + "," + str(colProbVal) + "," + str(cuVal) + "," + str(colSwitch) + "\n"
                    good_line = "good" + "," + str(good_frac) + "," + str(mean_good) + "," + str(stddev_good) + "\n"
                    for mean_bad_value in mean_bad:
                        bad_line = "bad" + "," + str(bad_frac) + "," + str(mean_bad_value) + "," + str(float(0.05*mean_bad_value)) + "\n"
                        count += 1
                        output_file = open(str(count), 'w')
                        output_file.write(unicode(runParams))
                        output_file.write(unicode(good_line))
                        output_file.write(unicode(bad_line))
                        output_file.close()

        elif (strategy == 2):#need to incorporate Collaborator(True,False) and c,cu values
            colSwitch = 'False'
            colProbVal = 0
            cuVal = 0
            for A in A_values:
                for B in B_values:
                    runParams = str(strategy) + "," + str(T) + "," + str(quantum) + "," + str(A) + "," + str(B) + "," + str(migrationPenalty) + "," + str(expectedMig) + "," + str(colProbVal) + "," + str(cuVal) + "," + str(colSwitch) + "\n"
                    good_line = "good" + "," + str(good_frac) + "," + str(mean_good) + "," + str(stddev_good) + "\n"
                    for mean_bad_value in mean_bad:
                        bad_line = "bad" + "," + str(bad_frac) + "," + str(mean_bad_value) + "," + str(float(0.05*mean_bad_value)) + "\n"
                        count += 1
                        output_file = open(str(count), 'w')
                        output_file.write(unicode(runParams))
                        output_file.write(unicode(good_line))
                        output_file.write(unicode(bad_line))
                        output_file.close()

            colSwitch = 'True'
            for A in A_values:
                for B in B_values:
                    for colProbVal in colProb:
                        for cuVal in cu:
                            runParams = str(strategy) + "," + str(T) + "," + str(quantum) + "," + str(A) + "," + str(B) + "," + str(migrationPenalty) + "," + str(expectedMig) + "," + str(colProbVal) + "," + str(cuVal) + "," + str(colSwitch) + "\n"
                            good_line = "good" + "," + str(good_frac) + "," + str(mean_good) + "," + str(stddev_good) + "\n"
                            for mean_bad_value in mean_bad:
                                bad_line = "bad" + "," + str(bad_frac) + "," + str(mean_bad_value) + "," + str(float(0.05*mean_bad_value)) + "\n"
                                count += 1
                                output_file = open(str(count), 'w')
                                output_file.write(unicode(runParams))
                                output_file.write(unicode(good_line))
                                output_file.write(unicode(bad_line))
                                output_file.close()

        elif (strategy == 3):#need to incorporate Collaborator(True,False) and c,cu values
            colSwitch = 'False'
            colProbVal = 0
            cuVal = 0
            for A in A_values:
                for B in B_values:
                    runParams = str(strategy) + "," + str(T) + "," + str(quantum) + "," + str(A) + "," + str(B) + "," + str(migrationPenalty) + "," + str(expectedMig) + "," + str(colProbVal) + "," + str(cuVal) + "," + str(colSwitch) + "\n"
                    good_line = "good" + "," + str(good_frac) + "," + str(mean_good) + "," + str(stddev_good) + "\n"
                    for mean_bad_value in mean_bad:
                        bad_line = "bad" + "," + str(bad_frac) + "," + str(mean_bad_value) + "," + str(float(0.05*mean_bad_value)) + "\n"
                        count += 1
                        output_file = open(str(count), 'w')
                        output_file.write(unicode(runParams))
                        output_file.write(unicode(good_line))
                        output_file.write(unicode(bad_line))
                        output_file.close()
                        
            colSwitch = 'True'
            for A in A_values:
                for B in B_values:
                    for colProbVal in colProb:
                        for cuVal in cu:
                            runParams = str(strategy) + "," + str(T) + "," + str(quantum) + "," + str(A) + "," + str(B) + "," + str(migrationPenalty) + "," + str(expectedMig) + "," + str(colProbVal) + "," + str(cuVal) + "," + str(colSwitch) + "\n"
                            good_line = "good" + "," + str(good_frac) + "," + str(mean_good) + "," + str(stddev_good) + "\n"
                            for mean_bad_value in mean_bad:
                                bad_line = "bad" + "," + str(bad_frac) + "," + str(mean_bad_value) + "," + str(float(0.05*mean_bad_value)) + "\n"
                                count += 1
                                output_file = open(str(count), 'w')
                                output_file.write(unicode(runParams))
                                output_file.write(unicode(good_line))
                                output_file.write(unicode(bad_line))
                                output_file.close()
                                
    print count