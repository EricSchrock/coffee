# Coffee

## Goals

Answer the following questions:

1. What was the price of a cup of coffee in the state of New York between 1900 and 1909?
2. How much does data cleaning on the source dataset change the answer to the first question?

## Dataset

### Summary

[What’s on the Menu?](https://menus.nypl.org/) is a project to transcribe The New York Public Library’s restaurant menu collection. The collection contains menus from around the world, stretching from the 1850s to the 2000s.

### Tables

The dataset contains four tables with the following relationships.

![entity relationship diagram](doc/entity-relationship-diagram.png)

Credit: @monsieur-le-git

### Exploration

The first target question is tuned to the data available in the dataset.

![menu bar chart](doc/menu-bar-chart.png)

## Workflow


## Cleaning


## Results


## Running the Project

```sh
conda env create -f environment.yml
conda activate coffee
python src/explore.py /path/to/dataset
```
