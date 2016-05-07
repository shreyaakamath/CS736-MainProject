import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o

import numpy as np

outerArray=[]
with open("arch3.csv") as f:
     for line in f:
         innerArray=[]
         list=line.split(",")
         innerArray.append(list[0].strip())
         innerArray.append(float(list[1]))
         innerArray.append(float(list[4]))
         #std=(float(list[3])-float(list[2]))/4
         #std=2
         innerArray.append(float(list[5]))
         outerArray.append(innerArray)
    
# print outerArray    
dpoints= np.array(outerArray)
# dpoints = np.array([['rosetta', '1gid', 9.97],
#            ['rosetta', '1gid', 27.31],
#            ['rosetta', '1y26', 5.77],
#            ['rnacomposer', '1mfq', 5.55],
#            ['rnacomposer', '1gid', 37.74],
#            ['rnacomposer', '1y26', 5.77],
#            ['random', '1mfq', 10.32],
#            ['random', '1gid', 31.46],
#            ['random', '1y26', 18.16]])

fig = plt.figure()
ax = fig.add_subplot(111)

def barplot(ax, dpoints):
    '''
    Create a barchart for data across different categories with
    multiple conditions for each category.
    
    @param ax: The plotting axes from matplotlib.
    @param dpoints: The data set as an (n, 3) numpy array
    '''
    
    # Aggregate the conditions and the categories according to their
    # mean values
    conditions = [(c, np.mean(dpoints[dpoints[:,0] == c][:,2].astype(float))) 
                  for c in np.unique(dpoints[:,0])]
    categories = [(c, np.mean(dpoints[dpoints[:,1] == c][:,2].astype(float))) 
                  for c in np.unique(dpoints[:,1])]
    
    # sort the conditions, categories and data so that the bars in
    # the plot will be ordered by category and condition
    conditions = [c[0] for c in sorted(conditions, key=o.itemgetter(1))]
    print conditions
#     categories = [c[0] for c in sorted(categories, key=o.itemgetter(1))]
#     print conditions
#     print categories
    conditions=['CPU','UPFRONT','CPU_OPREP','UPFRONT_OPREP','CPU_OPREP_COLLABORATOR','UPFRONT_OPREP_COLLABORATOR']
    categories=['5.0','6.0','7.0','8.0','9.0']
#     print conditions
#     print categories
    dpoints = np.array(sorted(dpoints, key=lambda x: categories.index(x[1])))
    print dpoints
    # the space between each set of bars
    space = 0.3
    n = len(conditions)
    width = (1 - space) / (len(conditions))
    
    # Create a set of bars at each position
    for i,cond in enumerate(conditions):
        indeces = range(1, len(categories)+1)
        vals = dpoints[dpoints[:,0] == cond][:,2].astype(np.float)
        stds = dpoints[dpoints[:,0] == cond][:,3].astype(np.float)
        pos = [j - (1 - space) / 2. + i * width for j in indeces]
        ax.bar(pos, vals, width=width, label=cond,yerr=stds,ecolor='k',color=cm.Accent(float(i) / n))
    
    # Set the x-axis tick labels to be equal to the categories
    ax.set_xticks(indeces)
    ax.set_xticklabels(categories)
    plt.setp(plt.xticks()[1], rotation=90)
    
    # Add the axis labels
    ax.set_ylabel("RMSD")
    ax.set_xlabel("Structure")
    
    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc="lower left")
        
barplot(ax, dpoints)
plt.savefig('trial.eps',format='eps',dpi=300,bbox_inches='tight')
# plt.show()