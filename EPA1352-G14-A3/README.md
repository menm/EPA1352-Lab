# Multi-level model roadnetwork Bangladesh (NetworkX and MESA)

Created by: EPA1352 Group 14

| Name    | Student Number |
|:-------:|:--------|
| Elias Bach  | 5379229 | 
| Lidha Hu | 4593979 |
| Ibrahim Jabri| 4291034  |
| Luca Ruijs | 5413370 |
| Pieter van Spaendonck |  4476697 |


## Introduction
For Assignment 3 of the EPA1352 Advanced Simulation course, a transport model of the road network in Bangladesh has been 
created. In this folder, a multilevel model integration consisting of a network (NetworkX) and ABM (MESA) model simulate 
the effects of bridges breaking down on all roads in Bangladesh > 25km. 
This transport model runs based on a multiple files:


## Files 
The overall file is called "EPA1352-G14-A3", it must contain 3 folders:

The "model" folder with:
* A3_model.py, see EPA1352-G14-A3/model/A3_model.py, which takes roads_data_processed_1503.csv as an input file that 
  specifies the infrastructure model components to be generated. 
* A3_model_run.py, see EPA1352-G14-A3/model/A3_model_run.py, which runs the model and the experiments.
* components.py, see EPA1352-G14-A3/model/components.py, which defines the various infrastructure components. 
* model_viz.py, see EPA1352-G14-A3/model/model_viz.py, which runs the model with visualization.
* ContinuousSpace folder, see EPA1352-G14-A3/model/ContinuousSpace

The "data" folder with:
* A3_datacleaning.ipynb, which contains the data cleaning process and output, see EPA1352-G14-A3/data/A3_datacleaning.ipynb
* roads_data_processed_1503.csv, which contains all roads and side roads of Bangladesh > 25km,
  see EPA1352-G14-A3/data/roads_data_processed_1503.csv
* A3_networkx_analysis.ipynb, which contains the analysis of the network, see EPA1352-G14-A3/data/A3_networkx_analysis.ipynb
* A3_scenarios.csv, which contains different sets (scenario's) of probabilities that a bridge breaks down specified for 
  bridge conditions. These on their end cause delays in travel times, see EPA1352-G14-A3/data/scenarios.csv
* A3_scenario_data.csv, which contains the results of the experiments, see EPA1352-G14-A3/data/A3_scenario_data.csv.
* A3_dataanalysis.ipynb, which contains the analysis of results of the experiments, see EPA1352-G14-A3/data/A3_dataanalysis.ipynb

## How to Use
The model can be executed by running either A3_model_run.py. For visualisation, model_viz.py should be 
used. However, it is not recommended for the current model setting as it will take enormous computational power. 
If the setting are edited to less model runs, model_viz.py may be run.

###A3_model_run.py 
is used to gather data. Several parameters can be adjusted before executing and gathering results.
* Seed (line 10): can be adjusted and used for a single run, to affect stochasticity, when doing multiple runs of the 
  same scenario.
* num_steps (line 16): run length can be adjusted to determine how many ticks the model will take for each scenario
* parameter_sweep (line 13): the range of seeds and selection of scenarios is set here and may be adjusted. This 
  overwrites the seed which is set in line 10.
* df_batch.to_csv('../data/A3_scenario_data.csv', index=False) (line  34): saves the ouput to a csv. 
  This is used for analysing the effects of the different scenarios on travel times.

###model_viz.py
is used to visualize the data.


Please Note: the input file roads_data_processed_1503.csv, was cleaned using a Jupyter notebook A3_datacleaning.ipynb
It used two input files BMMS_overview.xlsx. & _roads3.csv. These 3 files are placed in "data_cleaning" folder, under
"EPA1352-G14-32". Make sure that BMMS is in excel format and roads in CSV format.
