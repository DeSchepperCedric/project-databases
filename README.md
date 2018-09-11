# Project Databases
[![Build Status](https://travis-ci.org/sergiofenoll/project-databases.svg?branch=master)](https://travis-ci.org/sergiofenoll/project-databases)

### Goal
The goal of this project is to create a webapp that provides easy to use data management services.
Users can upload their data (from various file formats), share access and divide it into logical 'datasets'.
Furthermore, the app allows for data manipulation in order to turn raw data into usable information. Eventually, the idea is to provide sufficiently advanced data cleaning and analysis tools.

### Usage
*Requirements*
* pip
* virtualenv
* SQLite

To setup your work environment:

`python3 -m virtualenv env && . env/bin/activate && pip3 install -r  requirements.txt`

Install using `--user` if you're not using a virtual environment, though I don't recommend

To run the app, run:

`python3 run.py`

### Acknowledgements
This project is based on a team project made by [Cedric De Schepper](https://github.com/DeSchepperCedric), [Jonathan Meyer](https://github.com/MeyerJon), [Dawid Miroyan](https://github.com/DawidMiroyan) and myself for the course **Programming Project Databases** at the University of Antwerp.

Very little/possibly none of the original code is used in this project, but it can be found in [this branch](https://github.com/sergiofenoll/project-databases/tree/project-end-state).