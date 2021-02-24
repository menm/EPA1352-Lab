# Bangladesh N1 road and bridges model
EPA-1351 Advanced Discrete Event Simulation
Group 13
Sybe Andringa  	4558448
Marceau Mertens 	4236343
Wessel Groot 		4243714
Kim van Vliet 		5185114

This is a simio (version 11.189.18749) model of the Bangladesh N1 road, including its bridges in Bangladesh. Trucks are generated at LRPs every 5 minutes and have a speed of random triangular (46,48,50) km/hr by which they travel from roadpoint to roadpoint. Bridges that are not broken down have a processing time of 0. A percentage of all bridges of a given condition may be broken down (see experiment VaryingBridgeBreakdown), which causes delays at the bridges depending on the bridge's length (as has been hard-coded in the data).