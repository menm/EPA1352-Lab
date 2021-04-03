from A4_model import BangladeshModel
from A4_components import *
import pandas as pd

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# main parameters
run_length = 24*60*5
seed = 12121212

# read in scenarios with breakdown probabilities for bridges
scenarios_df = pd.read_csv("../data/A4_scenarios.csv")
scenarios_list = scenarios_df.values.tolist()

# run model for each scenario
for scenario in scenarios_list:
    bdp = scenario[1:]
    sim_model = BangladeshModel(seed=seed, bdp=bdp)

    # Check if the seed is set
    print("SEED " + str(sim_model._seed))

    # One run with given steps
    for i in range(run_length):
        sim_model.step()

    # initialize dataframe to collect results
    results = pd.DataFrame(columns=["id", "condition", "lon", "lat", "average_delay"])
    # after the model collect data on all the bridges in the scheduler
    for agent in sim_model.schedule.agents:
        if isinstance(agent, Bridge):
            new_row = {'id': agent.unique_id, 'condition': agent.condition,
                       'lon': agent.x, 'lat': agent.y,
                       'average_delay': agent.cumulative_delay/agent.vehicles if agent.vehicles != 0 else 0}
            results = results.append(new_row, ignore_index=True)

    # save results
    print(results)
    results.to_csv("../results/A4_results_"+str(scenario[0])+"_"+str(seed)+".csv", index=False)

# EOF -----------------------------------------------------------
