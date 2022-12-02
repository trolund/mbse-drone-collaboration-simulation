import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks, twinx
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
from pathlib import Path


date = datetime.datetime.now().strftime("%Y_%m_%d")
filename = Path('C:/Users/odaby/Desktop/MBSE_Project/MBSE-Drone-Collaboration/simulation_batcher/avgEnergyPrDrone_packageWeight_nrDrones.csv')

df = pd.read_csv(filename)
df = df[['number_of_drones', 'fixed_package_weight', 'Avg_Energy_consumption']]

df['fixed_package_weight'] = df['fixed_package_weight']/1000 
df['Avg_Energy_consumption'] = df['Avg_Energy_consumption']/1000 

id_list = df['number_of_drones'].unique()

fig, ax = plt.subplots()
#ax.legend(title='Number of Drones')
#plt.legend(loc='lower right')


for i in [1, 2, 3, 5, 7, 9, 12, 15]:
    ax = df.loc[(df['number_of_drones'] == i)].plot(
        y='Avg_Energy_consumption', x='fixed_package_weight', ax=ax, label=i, xlim=[0, 10], ylim=[0, 175])
    plt.title(i, fontsize=18)  # Labeling titel
    plt.xlabel('Package Weights [kg]', fontsize=12)  # Labeling x-axis
    plt.ylabel('Average Energy Consumption per Drone [kJ]',
               fontsize=12)  # Labeling y-axis
ax.legend(title='Number of Drones', loc=4)
plt.title('Energy Consumption of Drones')
plt.axhline(y=159.840, color='black', linestyle='--')
plt.grid(visible=None, which='major', axis='both', linestyle='--')
# truck_based_df.plot(x='percentage_increase', y='number_of_drones')
plt.show()
