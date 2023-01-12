# lca_graphic

## Description
This tool is designed to provide several easy-to-understand graphics for everyday LCA practionners to quickly analyze their LCA results in Brightway. 
Hello hello

The [utils.py](https://github.com/teolvs/lca_graphic/blob/main/utils.py) file gives useful tool for quickly LCA computations and analyse of the contributions.
The [dashboards.py](https://github.com/teolvs/lca_graphic/blob/main/dashboards.py) provides the methods to gather all the results into three dashboards :
1. to compare LCA results in different impact categories on the one hand,
2. to analyze the contributions of each activity in different impact categories on the other hand
3. to plot the variations of the contribution of the top processes (for the reference method) for each impact category to identify the impact transfers.


## Installation
Data used come from the open [US EEIO table](https://github.com/USEPA/USEEIO), and [available here (115MB download)](https://files.brightway.dev/visualization_example_data.zip). 
Note: any brightway2 LCA database may be used and would work.

The code to create the example data and how use the main methods is given in the notebook ``visualization_contest.ipynb``. To see the dashboards, the code should be executed on an Jupyter Notebook, since it does not appear on Github.

## Contribution


## License
BSD 2-Clause "Simplified" License <br>
https://github.com/teolvs/lca_graphic/blob/main/LICENSE.md
