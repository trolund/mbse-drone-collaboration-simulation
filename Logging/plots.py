import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
#plt.rcParams.update(plt.rcParamsDefault)
# use LaTeX fonts in the plot
#plt.rc('text', usetex=True)
plt.rc('font', family='serif')

date = datetime.datetime.now().strftime("%Y_%m_%d")
Filename = "Logging\Files\\" + "Summary_"+ date +".csv"

df = pd.read_csv(Filename)

cols= range(1,10)
data = df.values[:, cols]
attributeNames= np.asarray(df.columns[cols])

#no_drones vs avg_delivery_time
f = figure()
figsize=(12,8)
#plt.plot(data[:,0],data[:,6],'o-') #Avarage delivery time per drone with 100 packages
#plt.plot(data[:,0],data[:,3],'o-') #Avarage speed per drone with 100 packages
#plt.plot(data[:,0],data[:,8],'o-') #Avarage workingtime per drone with 100 packages

title('Number of drones vs. average delivery time')
xlabel('Number of drones')
ylabel('Average delivery time')  
# #plt.savefig('plot.pdf') 
#show()

#distribution of delivery times
#plt.hist(data[:,6])
#data[:,6].plot.kde()
show()


print(f"No_drones: {data[:,0]}")
print(f"Avg_delivery_time: {data[:,6]}")
print(f"packages: {data[:,1]}")
print(data[0:2,1])
print(data[0:2,6])
print(data[:,8])


print(attributeNames)



