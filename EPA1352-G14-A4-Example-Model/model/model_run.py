from model import BangladeshModel
from components import *
import pandas as pd

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 1000 # 5 * 24 * 60

# run time 1000 ticks
# run_length = 1000

seed = 1234567

sim_model = BangladeshModel(seed=seed)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()

results = pd.DataFrame(columns=["id", "condition", "lon", "lat", "average_delay"])
for agent in sim_model.schedule.agents:
    if isinstance(agent, Bridge):
        new_row = {'id': agent.unique_id, 'condition': agent.condition,
                   'lon': agent.x, 'lat': agent.y,
                   'average_delay': agent.cumulative_delay/agent.vehicles if agent.vehicles != 0 else 0}
        results = results.append(new_row, ignore_index=True)

print(results)
results.to_csv("../notebook/A4_results.csv", index=False)

#TODO include DataCollector/Batchrunner