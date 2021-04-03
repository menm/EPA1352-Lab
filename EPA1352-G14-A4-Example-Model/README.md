# Vulnerability and criticality of the Bangladeshi road network (NetworkX and MESA)

Created by: EPA1352 Group 14

| Name    | Student Number |
|:-------:|:--------|
| Elias Bach  | 5379229 | 
| Lidha Hu | 4593979 |
| Ibrahim Jabri| 4291034  |
| Luca Ruijs | 5413370 |
| Pieter van Spaendonck |  4476697 |

## Introduction
For Assignment 4 of the EPA1352 Advanced Simulation course, a transport model of the road network in Bangladesh has been 
created. In this folder, a multilevel model integration consisting of a network (NetworkX) and ABM (MESA) model are used 
to analyze the vulnerability and criticality of the national roads of Bangladesh. This transport model runs based on a multiple files:

## Files 
The overall file is called "EPA1352-G14-A4", it contains four important folders:

The "model" folder with:
* A4_model.py, see EPA1352-G14-A4/model/A4_model.py, which takes fully_cleaned_data.csv as an input file that 
  specifies the infrastructure model components to be generated. 
* A4_model_run.py, see EPA1352-G14-A4/model/A4_model_run.py, which runs the model and the experiments.
* A4_components.py, see EPA1352-G14-A4/model/A4_components.py, which defines the various infrastructure components. 
* A4_model_viz.py, see EPA1352-G14-A4/model/A4_model_viz.py, which runs the model with visualization.
* ContinuousSpace folder, see EPA1352-G14-A4/model/ContinuousSpace

The "notebook" folder with:
* fully_cleaned_data.csv, which contains all roads and side roads of Bangladesh > 25km,
  see EPA1352-G14-A3/data/fully_cleaned_data.csv
* A3_scenarios.csv, which contains different sets (scenario's) of probabilities that a bridge breaks down specified for 
  bridge conditions. These on their end cause delays in travel times, see EPA1352-G14-A3/data/scenarios.csv
* A3_scenarios_data.csv, which contains the results of the experiments, see EPA1352-G14-A3/data/A3_scenarios_data.csv.

The "data" folder with:
* NEW_trafficinputdata_cleaned.csv, which contains all national roads and side roads of Bangladesh > 25km, and their
  corresponding traffic densities, see EPA1352-G14-A4/data/NEW_trafficinputdata_cleaned.csv
* A4_scenarios.csv, which contains different sets (scenarios) of probabilities that a bridge breaks down specified for 
  bridge conditions. These on their end cause delays in travel times, see EPA1352-G14-A4/data/A4_scenarios.csv

The "notebooks" folder with:
* A4_datacleaning.ipynb, which contains the data cleaning process and output, in this notebook the traffic densities for
  the road segments were calculated
* !!!
* These .ipynb files all require various input and give output files, which are documented in the notebooks themselves.

The "results" folder with: the results of the experiment. There are 25 files in total, five for each scenario, each of 
which have been run for five seeds. The results are saved as: A4_results_"experimentnumber"_"seed". 

## How to Use
The model can be executed by running either A4_model_run.py. For visualisation, A4_model_viz.py should be 
used. 

###A4_model_run.py 
is used to gather data. Several parameters can be adjusted before executing and gathering results.
* Seed (line 14): can be adjusted and used for a single run, to affect stochasticity, when doing multiple runs of the 
  same scenario.
* Scenarios to run (line 17): the A4_scenario.csv contains the breakdown probabilities of various scenarios
* for scenario in scenarios_list (line 21): run the experiments
* results.to_csv("../results/A4_results_"+str(scenario[0])+"_"+str(seed)+".csv", index=False) (line 44): saves the ouput to a csv. 
  This is used for analysing the effects of the different scenarios on travel times.
Please Note: the input file for model_run.py is fully_cleaned_data.csv placed in the data folder.
  
###A4_model_viz.py
is used to visualize the data. The visualization is currently based on a particular probability of the bridges breaking
down, if changed, the visualization will change as well. 
