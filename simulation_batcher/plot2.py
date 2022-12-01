import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks, twinx
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
from pathlib import Path


date = datetime.datetime.now().strftime("%Y_%m_%d")
filename = Path('C:/Users/Jensm/OneDrive - Danmarks Tekniske Universitet/9. semester/02223 - Model-Based Systems Engineering/git/simulation_batcher/avgEnergyPrDrone_packageWeight_nrDrones.csv')

df = pd.read_csv(filename)
df = df[['number_of_drones', 'fixed_package_weight', 'Avg_Energy_consumption']]


id_list = df['number_of_drones'].unique()

fig, ax = plt.subplots()
ax.legend(title='Number of drones')

plt.rcParams.update(plt.rcParamsDefault)
# use LaTeX fonts in the plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

for i in [1, 2, 3, 5, 7, 9, 12, 15, 18, 20]:
    ax = df.loc[(df['number_of_drones'] == i)].plot(
        y='Avg_Energy_consumption', x='fixed_package_weight', ax=ax, label=i, xlim=[0, 25000], ylim=[0, 175000])
    plt.title(i, fontsize=18)  # Labeling titel
    plt.xlabel('Package weights [g]', fontsize=12)  # Labeling x-axis
    plt.ylabel('Average Energy consumption pr drone[J]',
               fontsize=12)  # Labeling y-axis
plt.title('Energy Consumption of drones')
plt.axhline(y=159840, color='black', linestyle='--')
# truck_based_df.plot(x='percentage_increase', y='number_of_drones')
plt.show()
