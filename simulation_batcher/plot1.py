import pandas as pd
import numpy as np
import datetime
from matplotlib.pyplot import boxplot, xticks, ylabel, title, show, xlabel, figure, subplot, hist, ylim, yticks, twinx
from matplotlib.pyplot import semilogx, loglog, subplots, scatter, figure, plot, grid, title, legend, xlabel, ylabel, show
import matplotlib.pyplot as plt
from pathlib import Path

# plt.rcParams.update(plt.rcParamsDefault)
# use LaTeX fonts in the plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

date = datetime.datetime.now().strftime("%Y_%m_%d")
filename = Path('C:/Users/Jensm/OneDrive - Danmarks Tekniske Universitet/9. semester/02223 - Model-Based Systems Engineering/git/simulation_batcher/droneDistance_nrDrones_customerDensity.csv')

df = pd.read_csv(filename)
df = df[['number_of_drones', 'customer_density',
         'moving_truck', 'Avg_dist_traveled']]

stationary_truck_df = df.loc[df['moving_truck'] == 0].reset_index(drop=True)
moving_truck_df = df.loc[df['moving_truck'] == 1].reset_index(drop=True)

truck_based_df = stationary_truck_df.join(
    moving_truck_df['Avg_dist_traveled'], rsuffix='moving').drop('moving_truck', axis=1)
truck_based_df['percentage_increase'] = 1 - (moving_truck_df['Avg_dist_traveled'] /
                                             stationary_truck_df['Avg_dist_traveled'])

print(truck_based_df.head())

# print(moving_truck_df.head())

# moving_truck_df = stationary_truck_df.loc[df['customer_density'] == 0.5].copy()

# print(moving_truck_df['percentage_increase'])

# moving_truck_df.plot(x='percentage_increase', y='number_of_drones')
