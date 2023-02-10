# lca_graphic

## Submitter
lca_graphic results from the union of the dataviz experience of Florent Blondin, 10 years on triing to crack the LCA datavizualisation challenge and the coding skills of Téo Lavisse, young and brilliant lca researcher at University of Grenoble.

## Description 
lca_graphic offers efficient charts for the daily life of a LCA practitionners in a single Brightway function to get a first overview of your LCA results.

The [utils.py](https://github.com/teolvs/lca_graphic/blob/main/utils.py) file gives useful tool for quickly LCA computations and analyse of the contributions.
The [dashboards.py](https://github.com/teolvs/lca_graphic/blob/main/dashboards.py) provides the methods to gather all the results into three dashboards :
1. ```compare``` to compare LCA results in different impact categories on the one hand,
2. ```impact_transfer``` to plot the variations of the contribution of the top processes (for the reference method) for each impact category to identify the impact transfers,
3. ```hotspots``` to analyze the contributions of each activity in different impact categories on the other hand.

All these methods are generated all at once in the method ```lca_graphic```


## Installation
Data used come from the open [US EEIO table](https://github.com/USEPA/USEEIO), and [available here (115MB download)](https://files.brightway.dev/visualization_example_data.zip). 
Note: any brightway2 LCA database may be used and would work.

The code to create the example data and how use the main methods is given in the notebook ``visualization_contest.ipynb``. To see the dashboards, the code should be executed on an Jupyter Notebook, since it does not appear on Github.

## Contribution
Do not hesitate to contribute to the improvements of this project.
A major improvement would be to adapt the functions to Ecoinvent. This would be easily done by updating the nomenclature of the activities and the methods

## Database(s) used
- [x] Used example data from the contest repository
- [ ] Used another database 👉 [used database name](url to the database)

## Links to the code and visualization

### Code
Please specify here the location of the code that produced the visualization submitted.

### Visualizations
Please specify here the location of the example visualizations produced with your code.

### Presentation video
Please put here the links to a video of maximum 4 minutes where you present your visualization.

## License
BSD 2-Clause "Simplified" License <br>
https://github.com/teolvs/lca_graphic/blob/main/LICENSE.md
