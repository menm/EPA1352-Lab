from mesa.batchrunner import BatchRunner
from A3_model import BangladeshModel, driving_time

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

seed = 12345670

# Batch run the model, for the specified scenarios and number of iterations.
parameter_sweep = { 'Seed': range(10000, 10003), 'Scenario': range(1,3)}

num_iterations = 1
# num_steps = 5 * 24 * 60
num_steps = 200

batch_run = BatchRunner(BangladeshModel, variable_parameters=parameter_sweep,
                        display_progress=False, iterations=num_iterations, max_steps=num_steps,
                        model_reporters={"Average driving time": driving_time})

batch_run.run_all()

# Get agent variables from all simulations in a dataframe
df_batch = batch_run.get_model_vars_dataframe()

print(df_batch)

# TODO process output data


# TODO put output into different scenario files and vehicle data is empty now
for i in range(1,3):
   df_batch[df_batch['scenario']==i].to_csv('scenario'+str(i)+'.csv', index=False)

# # save every scenerio to seperate csv file
# start = 0
# end = iterations
#
# for scenario in range(len(parameter_list)):
#     run_data[start:end].to_csv('../data/experiment/scenario{}.csv'.format(scenario))
#     start += iterations
#     end += iterations