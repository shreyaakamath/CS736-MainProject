import numpy as np
import matplotlib.pyplot as plt
import sys


fp = open(sys.argv[1])

lines = fp.read().split("\r")
lines = [line.split(",") for line in lines if line!=""]
if len(lines) != 10:
	print("Wrong format of file !!")

number_of_bytes = []
shared_memory_time = []
pipe_time = []
sockets_time = []

for line in lines[1:]:
	number_of_bytes.append(line[0])
	shared_memory_time.append((float(line[1])*1.0)/1000.0)
	pipe_time.append((float(line[2])*1.0)/1000.0)
	sockets_time.append((float(line[3])*1.0)/1000.0)


number_of_bytes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

x_labels = ["4","8", "16","32", "64","128", "256","512", "1K","2K","4K","8K","16K","32K","64K","128K","256K","512K"]

params = {#'text.usetex': True,
    'font.size' : 24,
    'axes.labelsize': 24,
    'xtick.labelsize' : 20,
    'ytick.labelsize' : 20,
    #'legend.fontsize' : 'medium',
    'legend.fontsize' : '20',
    'lines.linewidth' : 3,
    'lines.markersize' : 5
}
plt.rcParams.update(params)
#plt.locator_params(axis = 'x', nbins = 10)

#plt.xlim([min(sorted_data_1[0],sorted_data_2[0],sorted_data_4[0],sorted_data_8[0],sorted_data_16[0]),max(sorted_data_1[-1],sorted_data_2[-1],sorted_data_4[-1],sorted_data_8[-1],sorted_data_16[-1])])
#plt.xlim([0.0000028,0.0006])

#plt.ylim([0.0,1.02])
#plt.yscale("log")
#plt.title("Impact of Batching on CDF for Per-Packet Processing Time - cloud.pcap")
#ax.set_yscale('log')
fig, ax = plt.subplots()
plt.xlabel("Message Size (B)")
plt.ylabel("Latency (us)")
plt.yscale("log")
plt.plot(number_of_bytes,shared_memory_time,'c',marker='o',label="Shared Memory", linestyle=':')
plt.plot(number_of_bytes,pipe_time,'m',marker='o',label="Pipe", linestyle='-.')
plt.plot(number_of_bytes,sockets_time,'y',marker='o',label="Socket", linestyle='-')

plt.xticks(number_of_bytes,x_labels,rotation="vertical")


plt.legend(loc="upper left")
#plt.legend(prop={'size':'small'}, fancybox=True, shadow=True,ncol = 3, bbox_to_anchor=(0.5, -0.2))
plt.grid()
#plt.savefig("latency.png", bbox_inches='tight')
plt.savefig(sys.argv[1].split(".")[0]+".eps", format='eps', dpi=300, bbox_inches='tight')
