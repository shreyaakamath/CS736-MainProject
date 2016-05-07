import numpy as np
import matplotlib.pyplot as pyplot

menMeans = (20, 35, 30, 35, 27)
menStd = (2, 3, 4, 1, 2)
womenMeans = (25, 32, 34, 20, 25)
womenStd = (3, 5, 2, 3, 3)
men1Means = (20, 35, 30, 35, 27)
men1Std = (2, 3, 4, 1, 2)
women1Means = (25, 32, 34, 20, 25)
women1Std = (3, 5, 2, 3, 3)



N = len(menMeans)               # number of data entries
ind = np.arange(N)              # the x locations for the groups
width = 0.35                    # bar width
fig, ax = pyplot.subplots()
rects1 = ax.bar(ind, menMeans,                  # data
                width,                          # bar width
                color='MediumSlateBlue',        # bar colour
                yerr=menStd,                  # data for error bars
                error_kw={'ecolor':'Tomato',    # error-bars colour
                          'linewidth':2})       # error-bar width

rects2 = ax.bar(ind + width, womenMeans, 
                width, 
                color='Tomato', 
                yerr=womenStd, 
                error_kw={'ecolor':'MediumSlateBlue',
                          'linewidth':2})
rects3 = ax.bar(ind, men1Means,                  # data
                width,                          # bar width
                color='MediumSlateBlue',        # bar colour
                yerr=men1Std,                  # data for error bars
                error_kw={'ecolor':'Tomato',    # error-bars colour
                          'linewidth':2})       # error-bar width

rects4 = ax.bar(ind + width, women1Means, 
                width, 
                color='Tomato', 
                yerr=women1Std, 
                error_kw={'ecolor':'MediumSlateBlue',
                          'linewidth':2})

axes = pyplot.gca()
axes.set_ylim([0, 41])             # y-axis bounds

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center',            # vertical alignment
                va='bottom'             # horizontal alignment
                )

autolabel(rects1)
autolabel(rects2)

pyplot.show()                              # render the plot