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
run_length = 400

seed = 1234567

sim_model = BangladeshModel(seed=seed)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()

#CHANGED
print("HELLO")
fixed_params = {}
variable_params = {'break_down_prob': [0,0,5,10]}

batch_run = BatchRunner(BangladeshModel, variable_params, fixed_params,
                        iterations = 1, max_steps=400,
                        model_reporters={'average_total_driving_time': calculate_avg_driving_time})
print("sup")

batch_run.run_all()

results = batch_run.get_model_vars_dataframe()
print(results)

sim_model.datacollector.get_model_vars_dataframe().plot()
plt.grid(True)
plt.show()