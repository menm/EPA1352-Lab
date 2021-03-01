import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
from model import *

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60

# run time 1000 ticks
run_length = 1

seed = 1234567

sim_model = BangladeshModel(seed=seed)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()

sim_model.datacollector.get_model_vars_dataframe().plot()

print("Hello")


fixed_params = {}
# example_list = [0, 0, 5, 10]
# example_list1 =
variable_params = {'break_down_prob': ([0,0,5,10],[0,3,6,9])}

batch_run = BatchRunner(BangladeshModel, variable_params, fixed_params, iterations = 1, max_steps=10,
                        model_reporters={'average_total_driving_time': calculate_avg_driving_time})

batch_run.run_all()

results = batch_run.get_model_vars_dataframe()
print(results)

plt.grid(True)
plt.show()