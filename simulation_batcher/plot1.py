import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks, twinx
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.ticker as mtick

# plt.rcParams.update(plt.rcParamsDefault)
# use LaTeX fonts in the plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

date = datetime.datetime.now().strftime("%Y_%m_%d")
filename = Path('C:/Users/odaby/Desktop/MBSE_Project/MBSE-Drone-Collaboration/simulation_batcher/droneDistance_nrDrones_customerDensity.csv')

df = pd.read_csv(filename)
df = df[['number_of_drones', 'customer_density',
         'moving_truck', 'Avg_dist_traveled']]

stationary_truck_df = df.loc[df['moving_truck'] == 0].reset_index(drop=True)
moving_truck_df = df.loc[df['moving_truck'] == 1].reset_index(drop=True)

truck_based_df = stationary_truck_df.join(
    moving_truck_df['Avg_dist_traveled'], rsuffix='moving').drop('moving_truck', axis=1)
# truck_based_df['percentage_increase'] = ((moving_truck_df['Avg_dist_traveled'] /
#                                          stationary_truck_df['Avg_dist_traveled']) - 1)*100
truck_based_df['percentage_increase'] = (1-(moving_truck_df['Avg_dist_traveled'] /
                                         stationary_truck_df['Avg_dist_traveled']))*100
# truck_based_df['percentage_increase'] = ((moving_truck_df['Avg_dist_traveled'] /
#                                          stationary_truck_df['Avg_dist_traveled']))*100


id_list = truck_based_df['customer_density'].unique()

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.legend(title='Customer density')

for i in id_list:
    ax = truck_based_df.loc[(truck_based_df['customer_density'] == i) & (truck_based_df['number_of_drones'] < 16)].plot(
        y='percentage_increase', x='number_of_drones', ax=ax, label=round(i, 1))
    plt.title(i, fontsize=18)  # Labeling titel
    plt.xlabel('Number of Drones', fontsize=12)  # Labeling x-axis
    plt.ylabel('Improvement',
               fontsize=12)  # Labeling y-axis
plt.title('Improvement in Average Distance Traveled per Drone \nMoving vs Stationary Truck')
plt.grid(visible=None, which='major', axis='both', linestyle='--')
# truck_based_df.plot(x='percentage_increase', y='number_of_drones')
#plt.savefig('improvement.pdf', format='pdf')
plt.show()
