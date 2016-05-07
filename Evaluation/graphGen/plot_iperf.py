import matplotlib.pyplot as plt
import csv
# radius = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# area = [3.14159, 12.56636, 28.27431, 50.26544, 78.53975, 113.09724]

trials=[]
perf=[]
with open("iperf.csv",'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        trials.append(float(row[0]))
        perf.append(float(row[1]))
plt.xlabel("Trials")
plt.ylabel("Performance")
plt.legend(loc="upper left")

plt.plot(trials, perf,'b',label='...')
plt.xlim([0,max(trials)+5])
plt.ylim([min(perf)-0.5, max(perf)+0.5])
plt.title("Iperf Performance Variation")
plt.grid()
plt.savefig("iperf.eps", format='eps',dpi=300,bbox_inches='tight')

