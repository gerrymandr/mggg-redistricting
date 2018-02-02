[![CircleCI](https://circleci.com/gh/msarahan/state-adjacency-graphs.svg?style=svg)](https://circleci.com/gh/msarahan/state-adjacency-graphs)

## About

Given a shape file (for districts, vtd's, etc.) and a geo ID, returns a graph representation of the shape file
that can be input to other projects that use graph representation as their input.

Input expected:
 1. shp_path (shape file path)
 2. column ID of unique boundary (e.g. district ID, geo ID in the .dbf file)
 
Output returned: TBD


## How to Install

pip intstall . ### !needs to be completed! ###


## How to Run

### CLI Instructions ###

Default CLI command: TBD

Optional CLI arguments: TBD

### Python Script Instructions ###

Sample Script:

 from adjacency_graphs.algorithms import TwoStepGraph

 shp_path = ‘tests/shapefiles/testershape.shp’ # desired shape file path
 geoid_column = ‘id’                           # desired geo ID from .dbf
 my_graph = TwoStepGraph(shp_dir, geoid_column)
 
(also see example_pipeline.py)


## What's in the package

Algorithms
 1. twostep.py
Plots
 1. mpl.py (see:[matplotlib](https://matplotlib.org/))
 

## Authors ##

Austin Hackathon Participants
### ! Add names if desired! ###
Nel Abdiel
Mary Barker
Sarah Hager
Anne Hanna
Allan Peng
Seth Rothschild
Michael Sarahan

with acknowledgment to Duke Hackathon Participants and others:
Sarah Von Ahn
Richard Barnes
Mira Bernstein
Moon Duchin
Gabriel Ramirez
Ria Das
Justin Solomon
Alejandro Velez
