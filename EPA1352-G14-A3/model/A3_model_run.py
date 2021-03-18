from mesa.batchrunner import BatchRunner
from A3_model import BangladeshModel, driving_time

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

seed = 12345670

# Batch run the model, for the specified scenarios and number of iterations.
parameter_sweep = {'seed': range(88888888, 88888891), 'scenario': range(1,6)}

num_iterations = 10
num_steps = 5 * 24 * 60

batch_run = BatchRunner(BangladeshModel, variable_parameters=parameter_sweep,
                        display_progress=False, iterations=num_iterations, max_steps=num_steps,
                        model_reporters={"Average driving time": driving_time})

batch_run.run_all()

# Get agent variables from all simulations in a dataframe
df_batch = batch_run.get_model_vars_dataframe()

print(df_batch)

df_batch.to_csv('../data/A3_results.csv', index=False)
