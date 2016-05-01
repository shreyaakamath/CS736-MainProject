#!/usr/python
import csv
import os
import io
import sys

if __name__ == '__main__':
    
    directory = sys.argv[1] + '/' 
    #print directory
    list_of_files = os.listdir(directory)
    count=0
    output_file = io.open(sys.argv[2], 'a')
    csvString = "filename" + "," + "server" + "," + "serverIP" + "," + "doclength" + "," + "concurrency" + "," + "time" + "," + "compreq" + "," + "failreq" + "," + "tottran" + "," + "htmltran" + "," + "reqpersec" + "," + "timeperreqall" + "," + "timeperreq" + "," + "transrate" + "," + "type" + "\n"
    output_file.write(unicode(csvString))
    try :
        for eachFile in list_of_files:
            count += 1
            csvString = eachFile + ","
            #print eachFile       
            filename = directory + str(eachFile)
            with open(filename, 'r') as f:
                flavour = eachFile.split('_')[0]
                #print flavour
                for line in f:
                    #print line
		    line = line.replace('\n', '')
                    if (line is '\n' or line is ' '):
                        continue
                    if ("Version" in line) :
                        continue
                    elif ("Copyright" in line) :
                        continue
                    elif ("Foundation" in line) :
                        continue
                    elif (("Benchmarking " in line) and ("Total" in line)) :
                        continue
                        #temp = line.strip("Benchmarking ")
                        #temp1 = temp[:temp.index('(be ')].strip(' ')
                        #print "Test machine is:" + temp1
                    elif ("Server Software" in line) :
                        server = line.strip('Server Software:        ')
                        csvString += server + ","
                        #print "Server is: " + server
                        continue
                    elif ("Hostname" in line):
                        serverIp = line.strip('Server Hostname:        ')
                        csvString += serverIp + ","
                        #print "Server Host IP is: " + serverIP
                        continue
                    elif ("Server Hostname" in line):
                        continue
                    elif("Server Port" in line):
                        continue
                    elif("Document Path" in line):
                        continue
                    elif("Document Length" in line):
                        docLen = line.strip('Document Length:        ').replace(' bytes', '')
                        csvString += docLen + ","
                        #print "Document Length: " + docLen
                        continue
                    elif("Concurrency Level" in line):
                        concurrency = line.strip('Concurrency Level:      ')
                        csvString += concurrency + ","
                        #print "Concurrency Level is: " + concurrency
                        continue
                    elif("Time taken" in line):
                        time = line.strip('Time taken for tests:   ').replace(' second', '')
                        csvString += time + ","
                        #print "Time taken is: " + time
                        continue 
                    elif("Complete requests" in line):
                        compReq = line.strip('Complete requests:      ')
                        csvString += compReq + ","
                        #print "No of Complete Requests is: " + compReq
                        continue
                    elif("Failed requests" in line):
                        failReq = line.strip('Failed requests:        ')
                        csvString += failReq + ","
                        #print "No of Failed Requests is: " + failReq
                        continue
                    elif("Total transferred" in line):
                        totTran = line.strip(' bytes').replace('Total transferred:      ','')
                        csvString += totTran + ","
                        #print "Total transferred is: " + totTran
                        continue
                    elif("HTML transferred" in line):
                        htmlTran = line.strip(' bytes').replace('HTML transferred:       ', '')
                        csvString += htmlTran + ","
                        #print "HTML transferred is: " + htmlTran
                        continue
                    elif("Requests per second" in line):
                        reqPerSec = line.strip('Requests per second:    ').replace(' [#/sec] (mean)','')
                        csvString += reqPerSec + ","
                        #print "Requests per second is: " + reqPerSec
                        continue
                    elif("Time per request" in line and "across all concurrent requests" in line):
                        timePerReqAcrossConcurrentClients = line.strip("Time per request:       ").replace(' [ms] (mean, across all concurrent requests)', '')
                        csvString += timePerReqAcrossConcurrentClients + ","
                        #print "Time per Request across all Concurrent requests is: " + timePerReqAcrossConcurrentClients
                        continue
                    elif("Time per request" in line):
                        timePerReq = line.strip('Time per request:       ').replace(' [ms] (mean)', '')
                        csvString += timePerReq + ","
                        #print "Time per Request is: " + timePerReq
                        continue
                    elif("Transfer rate" in line):
                        transferRate = line.strip('Transfer rate:          ').replace(' [Kbytes/sec] received', '')
                        csvString += transferRate + ","
                        #print "Transfer rate is: " + transferRate
                        #continue
                    #csvString += "\n"
            #print csvString + '\n'
            csvString += flavour
            #if(len(csvString)<100):
		#csvString = ""
		#continue
	    output_file.write(unicode(csvString + "\n"))
            csvString = ""
            #break
        output_file.close()            

    except Exception,e:
        print e    
            
