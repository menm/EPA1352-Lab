import matplotlib.pyplot as plt
from model import *
import pandas as pd
"""
    Run simulation
    Print output at terminal
"""


# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick = 1 minute
# run_length = 5 * 24 * 60

# hence run time
run_length = 7200

seed = 1234567

scenarios = [[0,0,0,0],[0,0,0,5], [0,0,0,10], [0,0,5,10], [0,0,10,20], [0,5,10,20],
             [0,10,20,40], [5,10,20,40], [10,20,40,80]]



results = pd.DataFrame(columns=['scenario', 'A', 'B', 'C', 'D', 'driving_time'])
count = 0
for break_down_prob in scenarios:
    sim_model = BangladeshModel(seed=seed, break_down_prob=break_down_prob)

    # Check if the seed is set
    print("SEED " + str(sim_model._seed))

    # One run with given steps
    for i in range(run_length):
        sim_model.step()

    if sim_model.total_removed_vehicles != 0:
        average_total_driving_time = sim_model.total_driving_time / sim_model.total_removed_vehicles
    else:
        average_total_driving_time = 0

    results.loc[count] = ['S'+str(count), sim_model.break_down_prob[0], sim_model.break_down_prob[1],
                            sim_model.break_down_prob[2], sim_model.break_down_prob[3], average_total_driving_time]
    count += 1

results.to_csv('../data/scenarios_data.csv', index=False)

results.plot(kind='bar',x='scenario',y='driving_time', legend=None, figsize=(12, 8))
plt.xlabel('scenario', fontsize=20)
plt.ylabel('driving time (min)', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.savefig('scenarios.png')
plt.show()
