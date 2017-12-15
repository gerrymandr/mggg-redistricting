# Census Data Mapping Project
The code used in this project was used to create adjacency graphs and other data structures to model relationships between congressional districts, census tracts, and other census units and subunits. The main functions which can be executed using the code in this project are: creating adjacency graphs & matrices, visualizing these data structures, and computing compactness scores and other measures using member and border nodes. The code is also specifically adapted to working with census data and includes ways of labeling and identifying entries based on GEOIDs. The main and most useful functions have been formalized and documented in district_node_computation_library.py

## Getting Started
These instructions will get you a copy of project code up and running on your machine for development, data analysis, and testing purposes. 

### Prerequisites
The following software needs to be installed on your machine. Instructions for installation are included and/or linked to in this section.

#### Python 3.5.x or greater and Anaconda 4.4+ 
![Python 3.5.3 :: Anaconda 4.4.0](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Python3-powered_hello-world.svg/2000px-Python3-powered_hello-world.svg.png)
Instructions on installing conda can be found here:
https://conda.io/docs/user-guide/install/index.html

#### Packages
You will also need to install the following packages to run the code in this project:

- PySAL
- PyLAB
- Glob
- Collections
- shapely

The recommended method of installation is using Python pip. For instructions on installing python packages using pip, see the instructions linked to below.

Installing pip: https://pip.pypa.io/en/stable/installing/

Installing packages using pip: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

Installing PySAL and PySAL documentation: http://pysal.readthedocs.io/en/latest/users/installation.html

## Usage
This section describes the code included in this project and possible uses. The code described is in the 'adjacency_graphs_all' folder of the repository.

### Adjacency Graphs and Visualization
![Adjacency graph for the TX tracts](../data/adjacency_graphs/adjacency_graph_48.png)
The above image is a visualization for the adjacency graphs of the tracts within the states of Texas.

### Membership Computations

