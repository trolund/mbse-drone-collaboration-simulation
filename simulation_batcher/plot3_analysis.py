import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks, twinx
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
from pathlib import Path


date = datetime.datetime.now().strftime("%Y_%m_%d")
# filename = Path('C:/Users/Jensm/OneDrive - Danmarks Tekniske Universitet/9. semester/02223 - Model-Based Systems Engineering/git/simulation_batcher/all_the_params.csv')
filename = Path('C:/Users/Jensm/OneDrive - Danmarks Tekniske Universitet/9. semester/02223 - Model-Based Systems Engineering/git/simulation_batcher/simulationDuration_numberOfDrones_nrOfTasks.csv')

df = pd.read_csv(filename)
# df = df[['number_of_tasks', 'number_of_drones', 'drone_speed',
#          'truck_speed', 'Avg_Energy_consumption', 'Total_time']]
# df['total_energy'] = df['Avg_Energy_consumption'] * df['number_of_drones']
df = df[['number_of_tasks', 'number_of_drones',
         'Avg_Energy_consumption', 'Total_time']]
df['total_energy'] = df['Avg_Energy_consumption'] * df['number_of_drones']


# df = df.loc[(
#     df["drone_speed"] == 200) & (df["truck_speed"] == 150)]


id_list = df['number_of_tasks'].unique()

fig, ax = plt.subplots()
ax.legend(title='Number of tasks')


for i in id_list:
    ax = df.loc[(df['number_of_tasks'] == i)].plot(
        y='Total_time', x='number_of_drones', ax=ax, label=i)
    # plt.title(i, fontsize=18)  # Labeling titel
    # plt.xlabel('Package weights [g]', fontsize=12)  # Labeling x-axis
    # plt.ylabel('Average Energy consumption pr drone[J]',
    #            fontsize=12)  # Labeling y-axis
# plt.title('Energy Consumption of drones')
plt.show()
