# The Adjacency Graphs Project
[![CircleCI](https://circleci.com/gh/msarahan/state-adjacency-graphs.svg?style=svg)](https://circleci.com/gh/msarahan/state-adjacency-graphs)
## About
This is a project for managing Adjacency Graphs in python. There are package components for **algorithms** to generate adjacency maps from shapefiles, make **plots** from the result and **export** graphs. Once the package is [installed](docs/install_and_faq.md), you can quickly build an adjacency graph with one of our built-in algorithms as follows:
```
from adjacency_graphs.algorithms import TwoStepGraph

shp_path = '/path/to/shape.shp'
geoid_column_name = 'column_name'

my_graph = TwoStepGraph(shp_path, geoid_column)
```
![Pennsylvania Graph](examples/penn.png)

## Quickstart

We recommend usage of Conda or virtualenv to work with this software. Directions
for setting up conda are at https://conda.io/docs/user-guide/install/index.html

We'll proceed here with directions for conda for the virtual environment, but
we'll use pip to install our packages.

We don't have this package on PyPI yet.  To install, download or clone the project:

```
git clone https://github.com/msarahan/state-adjacency-graphs
cd state-adjacency-graphs
```

We include the environment definition that conda should create in the
environment.yml file. That's why we ask you to download the source first.

```
conda env create 
source activate adj
```

Note: on Windows, omit "source" in the line above.


That will create the environment, including installing the `adjacency_graphs`
package and all of the dependencies. To see if the package has correctly
installed, run

```
cd examples
python example_pipeline.py
```

This will generate the example.png and example_graph.csv files, showing the
potential outputs of this program.

## Contributing

There is a [guide](docs/development_guide.md) for first time
contributors to this project. This project is a fork from
the
original
[state-adjacency-graphs](https://github.com/gerrymandr/state-adjacency-graphs) and
would not have been possible without contributions from
the
[Austin Gerrymandering Hackathon](https://www.ma.utexas.edu/users/blumberg/gerrymandering.html).
A full contributors list can be found
at [contributors.txt](docs/contributors.txt).

## Documentation ##
Please document future updates to this project in the [MGGG Software Guide](https://docs.google.com/document/d/1aEl7znLggJW95gRhnefzS3dVE8iE7NZa3VaXZNmok5g/edit?usp=sharing)
