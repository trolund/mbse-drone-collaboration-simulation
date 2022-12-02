import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks, twinx
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
from pathlib import Path

# use LaTeX fonts in the plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

date = datetime.datetime.now().strftime("%Y_%m_%d")
filename = Path('C:/Users/odaby/Desktop/MBSE_Project/MBSE-Drone-Collaboration/simulation_batcher/all_the_params.csv')


df = pd.read_csv(filename)
df = df[['number_of_tasks', 'number_of_drones', 'drone_speed',
         'truck_speed', 'Avg_Energy_consumption', 'Total_time']]
df['total_energy'] = df['Avg_Energy_consumption'] * df['number_of_drones']
# df = df[['number_of_tasks', 'number_of_drones',
#          'Avg_Energy_consumption', 'Total_time']]
# df['total_energy'] = df['Avg_Energy_consumption'] * df['number_of_drones']


df = df.loc[(
    df["number_of_drones"] == 11) & (df["number_of_tasks"] == 201)]


id_list = df['truck_speed'].unique()

fig, ax = plt.subplots()
ax.legend(title='Truck speed')


for i in id_list:
    ax = df.loc[(df['truck_speed'] == i)].plot(
        y='Total_time', x='drone_speed', ax=ax, label=i)
    # plt.title(i, fontsize=18)  # Labeling titel
    # plt.xlabel('Package weights [g]', fontsize=12)  # Labeling x-axis
    # plt.ylabel('Average Energy consumption pr drone[J]',
    #            fontsize=12)  # Labeling y-axis
plt.title('Energy Consumption of drones')
plt.xlabel('Drone Speed (relative)', fontsize=12)  # x-axis
plt.ylabel('Delivery Time (relative)', fontsize=12)#yaxis
plt.title('Delivery Time with Respect to Truck and Drone Speed')
plt.grid(visible=None, which='major', axis='both', linestyle='--')
plt.show()
