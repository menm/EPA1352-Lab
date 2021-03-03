# README File Assignment 2

Created by: EPA1352 Group 14

| Name    | Student Number |
|:-------:|:--------|
| Elias Bach  | 5379229 | 
| Lidha Hu | 4593979 |
| Ibrahim Jabri| 4291034  |
| Luca Ruijs | 5413370 |
| Pieter van Spaendonck |  4476697 |


## Introduction
For Assignment 2 of the EPA1352 Advanced Simulation course, a transport model demo has been created to analyze the 
economic vital N1 road from Chittagong to Dhaka in Bangladesh. This transport model runs
based on a multiple files:

## Files 
The overall file is called "EPA1352-G14-A2", it must contain 2 folders:

The "model" folder with:
* model.py, see EPA1352-G14-A2/model/model.py, which takes N1_infrastructure.csv as an input file that specifies the infrastructure model components to be generated. 
* model_run.py, see EPA1352-G14-A2/model/model_run.py, which runs the model and the experiments.
* components.py, see EPA1352-G14-A2/model/components.py, which defines the various infrastructure components. 
* model_viz.py, see EPA1352-G14-A2/model/model_viz.py, which runs the model with visualization.
* ContinuousSpace folder, see EPA1352-G14-A2/model/ContinuousSpace

The "data" folder with:
* N1_infrastructre.csv, see EPA1352-G14-A2/data/N1_infrastructre.csv

## How to Use
The model can be executed by running either model_run.py and model_viz.py.

###model_run.py 
is used to gather data. Several parameters can be adjusted before executing and gathering results.

* Run_length (line 16): run length can be adjusted to determine how many ticks the model will take for each scenario
* Seed (line 17): can be adjusted in line 17, to affect stochasticity, when doing multiple runs of the same scenario
* Scenarios (line 20): can be adjusted to determine which break_down_probabilities will be assigned to category A, B, C, D 
bridges respectively in each scenario.

###model_viz.py
is used to visualize the data.
It runs indefinitely and the user can decide how long to simulate.
It only simulates one scenario at a time. If a new scenario is to be simulated, one must changed the default value
for break_down_prob in model.py (line 87)

Please Note: the input file N1_infrastructre.csv, was cleaning using a Jupyter notebook A2_datacleaning.ipynb
It used 2 input files BMMS_overview.xlsx. & _roads3.csv. These 3 files are placed in "data_cleaning" folder, under
"EPA1352-G14-A2". Make sure that BMMS is in excel format and roads in CSV format.
