from mesa.batchrunner import BatchRunner

from A3_model import BangladeshModel

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 10

# run time 1000 ticks
# run_length = 1000

seed = 12345670

# Batch run the model, for the specified scenarios and number of iterations.
parameter_sweep = {'scenario': range(1, 3), 'seed': range(10000, 10003)}

num_iterations = 1
# num_steps = 5 * 24 * 60
num_steps = 5
# agent reporters:
agent_reporter_dict = {'vehicle_data': 'removed_vehicles'}

batch_run = BatchRunner(BangladeshModel, variable_parameters=parameter_sweep,
                        display_progress=False, iterations=num_iterations, max_steps=num_steps,
                        agent_reporters=agent_reporter_dict)

batch_run.run_all()

# Get agent variables from all simulations in a dataframe
df_batch = batch_run.get_agent_vars_dataframe()

print(df_batch)

# TODO process output data
#

# TODO put output into different scenario files and vehicle data is empty now
for i in range(1,3):
   df_batch[df_batch['scenario']==i].to_csv('scenario'+str(i)+'.csv', index=False)


# Old stuff
# sim_model = BangladeshModel(seed=seed)
#
# # Check if the seed is set
# print("SEED " + str(sim_model._seed))
#
# # One run with given steps
# for i in range(run_length):
#     sim_model.step()
