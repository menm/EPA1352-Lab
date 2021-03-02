import matplotlib.pyplot as plt
from model import *

import pandas as pd
"""
    Run simulation
    Print output at terminal
"""


# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60

# run time 1000 ticks
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

    results.loc[count] = ['scenario'+str(count), sim_model.break_down_prob[0], sim_model.break_down_prob[1],
                            sim_model.break_down_prob[2], sim_model.break_down_prob[3], average_total_driving_time]
    count += 1

results.to_csv('../data/scenarios_data')

# sim_model.datacollector.get_model_vars_dataframe().plot()
#
# print("Hello")
#
#
# fixed_params = {}
# # example_list = [0, 0, 5, 10]
# # example_list1 =
# variable_params = {'break_down_prob_A': [0,5],
#                    'break_down_prob_B': [0,5],
#                    'break_down_prob_C': [0,5],
#                    'break_down_prob_D': [0,5],
# }
#
# batch_run = BatchRunner(BangladeshModel, variable_params, fixed_params, iterations = 2, max_steps = 10,
#                         model_reporters={'average_total_driving_time': calculate_avg_driving_time})
#
# batch_run.run_all()
#
# results = batch_run.get_model_vars_dataframe()
# print(results)
#
# plt.grid(True)
# plt.show()