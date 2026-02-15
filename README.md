# Challenge 1: Embedded Movie Search

## The Task

Your goal is to create a solution that can quickly find the top 3 movies from an `input.csv` file, closest embedded for each query point in a `query.csv` file. The output should be an `out.csv` file containing the `title` and `id` of the 3 movies closest in distance for each query point, as columns `top{i}_{title/id}`.


## Solutions

To create a new solution:

1.  Create a new directory for your solution under the `solutions/` directory, with the name of your solution (e.g., `solutions/frog/`).
2.  Inside your solution's directory, create a `Makefile` that defines the following targets:
    *   `setup`: To set up the environment for your solution.
    *   `preproc`: To preprocess the `input.csv`. At this point, your solution will have access to `input.csv`.
    *   `compute`: To perform the search on `query.csv` and generate `out.csv`. You will have access to `query.csv` at this point.
    *   `cleanup`: To clean up any files created by your solution.
3.  Add your solution's source code (e.g., `src.py`).
4.  You can test your solution using `python single_run.py your_solution_name`.
5.  You can run all solutions and generate a comparison table using `make run-all` and `make comp-table`. The results will be in `runs/README.md`.


## Evaluation

Solutions are evaluated based on correctness and performance. The performance is measured by the time it takes to run the compute stage. Correctness is verified by comparing your output with a benchmark solution.

## The Data

The dataset is a CSV file containing movie information, including `x` and `y` coordinates, `title`, and `imdb_id`. The `single_run.py` script will automatically download the data and create the `input.csv` and `query.csv` files for your solution.

## Example Solution

The `solutions/baboon` directory contains a simple, brute-force implementation that you can use as a starting point, and is the initial basis for evaluation.
