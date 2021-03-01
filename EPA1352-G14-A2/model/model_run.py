import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
from model import *

"""
    Run simulation
    Print output at terminal
"""
#test for push
# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60

# run time 1000 ticks
run_length = 10

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
# variable_params = [{'break_down_prob_A': 0 ,'break_down_prob_B': 0, 'break_down_prob_C': 0, 'break_down_prob_D': 0},
#                    {'break_down_prob_A': 0, 'break_down_prob_B': 0 , 'break_down_prob_C': 0, 'break_down_prob_D': 5}]

                                            # ''
                                            # '5,10]}, {'break_down_prob_B': [0,0,5,10]}, {'break_down_prob_C': [0,0,5,10]}, {'break_down_prob_D': [0,0,5,10],}
variable_params = {'break_down_prob_A': [0, 5] ,
                   'break_down_prob_B': [0, 5],
                   'break_down_prob_C': [0, 5],
                   'break_down_prob_D': [0, 5]}

batch_run = BatchRunner(BangladeshModel, variable_params, fixed_params, iterations = 1, max_steps=10,
                        model_reporters={'average_total_driving_time': calculate_avg_driving_time})

batch_run.run_all()
print("before")
results = batch_run.get_model_vars_dataframe()
print("after")

for scerio_run in range(len(variable_params)):
    results

results.head()

# if __name__ = "__main__":
#     batch_run.run_all()
#     batch_run_df = batch_run.get_model_vars_dataframe()
#     batch_run_step_data = pd.DataFrame()
#     for i in range(len(batch_run_df["Data Collector"])):
#         if istinatance(batch_run_df["Data Collector"][i],DataCollector):
#             i_run_data = batch_run_df["Data Collector"][i].get_model_vars_dataframe()
#             batch_run_step_data = batch_run_step_data.append()
plt.grid(True)
plt.show()