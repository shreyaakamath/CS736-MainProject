import json
import sys
import os
import time

if len(sys.argv) < 2:
        print "Usage : python "+sys.argv[0]+" <server_ip>"
        sys.exit()

server_ip = sys.argv[1]
iperf_command = "iperf3 -c "+server_ip+" -J > tmp.json"
while True:
        os.system(iperf_command)
        json_obj = json.load(open("tmp.json"))
        throughput = float(json_obj["end"]["sum_sent"]["bits_per_second"])/1000000000
        fp = open("iperf_results.csv","a")
        fp.write(str(throughput)+"\n")
        fp.close()