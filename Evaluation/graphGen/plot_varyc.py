import matplotlib.pyplot as plt
import csv
# radius = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# area = [3.14159, 12.56636, 28.27431, 50.26544, 78.53975, 113.09724]

c=[]
migrations=[]
collabs=[]
with open("varyc.csv",'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        c.append(float(row[0]))
        migrations.append(float(row[1]))
        collabs.append(float(row[2]))
plt.xlabel("Migration Probability")
plt.ylabel("Number of iterations")
plt.legend(loc="upper left")

plt.plot(c, migrations,'c',marker='o',label="No of Migrations", linestyle=':')
plt.plot(c, collabs,'m',marker='o',label="No of Collaborations", linestyle='-.')
# plt.xlim([0,max(trials)+5])
# plt.ylim([min(perf)-0.5, max(perf)+0.5])
plt.title("Number of migrations and collaborations")
plt.legend(loc="upper left")
plt.grid()
plt.savefig("varyc.eps", format='eps',dpi=300,bbox_inches='tight')

