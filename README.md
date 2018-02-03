# The Adjacency Graphs Project
[![CircleCI](https://circleci.com/gh/msarahan/state-adjacency-graphs.svg?style=svg)](https://circleci.com/gh/msarahan/state-adjacency-graphs)

## About
This is a project for managing Adjacency Graphs in python. There are package components for **algorithms** to generate adjacency maps from shapefiles, make **plots** from the result and **export** graphs. Once the package is [installed](##Quickstart), you can quickly build an adjacency graph with one of our built-in algorithms as follows:
```
from adjacency_graphs.algorithms import TwoStepGraph

shp_path = '/path/to/shape.shp'
geoid_column_name = 'column_name'

my_graph = TwoStepGraph(shp_path, geoid_column)
```


## Quickstart

To install first download the project
from
[this](https://github.com/msarahan/state-adjacency-graphs)
github repository. Then, open a terminal and navigate to the folder by running
```
cd /path/to/state-adjacency-graphs
```
The python package can then be installed by running the command
```
pip install .
```
That will install the `adjacency_graphs` package and all of the dependencies. To see if the package has correctly installed, run
```
python examples/example_pipeline.py
```

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
