import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks, twinx
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
#plt.rcParams.update(plt.rcParamsDefault)
# use LaTeX fonts in the plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

date = datetime.datetime.now().strftime("%Y_%m_%d")
Filename = r'G:\My Drive\DTU\Master\Semester_1\Model-Based Systems Engineering\Data_analysis\Summary_2022_11_24.csv'

df = pd.read_csv(Filename)

cols= range(0,10)
data = df.values[:, cols]
attributeNames= np.asarray(df.columns[cols])

#split data into optimal position and moving truck
data_opt = data
data_move = data
data_move = np.delete(data_move, list(range(0, data_move.shape[0], 2)), axis=0)
data_opt = np.delete(data_opt, list(range(1, data_opt.shape[0], 2)), axis=0)

'''no_drones vs avg_delivery_time'''
f = figure()
figsize=(12,8)
plt.plot(data_opt[:,0],data_opt[:,5],'o-', label="Stationary truck") #Avarage delivery time per drone with 100 packages
plt.plot(data_move[:,0],data_move[:,5],'o-', label="Moving truck")
title('Average Package Delivery Time')
xlabel('Number of drones')
ylabel('Average delivery time \n[relative]')  
legend(loc="upper right")
#plt.savefig('avg_delivery_time.pdf') 
plt.savefig('avg_delivery_time.png') 

'''no_drones vs avg_power'''
numbers = data_opt[9,8].split(",")
numbers2 = data_move[9,8].split(",")
for i in range(0,len(numbers)):
    numbers[i] = float(numbers[i])
    numbers2[i] = float(numbers2[i])

f = figure()
X_axis = np.arange(len(data_opt[:,0]))
 
plt.bar(X_axis - 0.2, numbers, 0.4, label = 'Stationary truck')
plt.bar(X_axis + 0.2, numbers2, 0.4, label = 'Moving truck')
  
plt.xticks(X_axis, data_opt[:,0])
plt.xlabel("Drone")
plt.ylabel("Energy consumption [J]")
plt.title("Energy consumption of each drone on one delivery task")
plt.legend()
#plt.savefig('energy.pdf') 
plt.show()