# jackson_job_shop_scheduling

<div align="center">

[![Build status](https://github.com/th-rpy/jackson_job_shop_scheduling/workflows/build/badge.svg?branch=master&event=push)](https://github.com/th-rpy/jackson_job_shop_scheduling/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/jackson_job_shop_scheduling.svg)](https://pypi.org/project/jackson_job_shop_scheduling/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/th-rpy/jackson_job_shop_scheduling/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/th-rpy/jackson_job_shop_scheduling/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/th-rpy/jackson_job_shop_scheduling/releases)
[![License](https://img.shields.io/github/license/th-rpy/jackson_job_shop_scheduling)](https://github.com/th-rpy/jackson_job_shop_scheduling/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

Implementation of a mathematical model in Python to solve an assignment problem in Job Shop environments. With its respective Gantt chart. 
A job shop consists of a set of distinct machines that process jobs. Each job is a series of tasks that require use of particular machines for known durations, and which must be completed in specified order. The job shop scheduling problem is to schedule the jobs on the machines to minimize the time necessary to process all jobs (i.e, the makespan) or some other metric of productivity. Job shop scheduling is one of the classic problems in Operations Research.

</div>

## Very first steps

First of all, you need to install a few dependencies.

- [Reportlab](https://pypi.org/project/reportlab/) : for generation PDF file.
- [numpy](https://pypi.org/project/numpy/) : for matrix operations.
- [pandas](https://pypi.org/project/pandas/) : for data manipulating.
- [matplotlib](https://pypi.org/project/matplotlib/) : for plotting Gantt Chart. 

## 🚀 Features
- Worked with multiple data formats: CSV, JSON and TEXT files. 
- Plotting Gantt Chart for each solution found for all sub-problems(Virtual).
- Generate a PDF file with the Gantt Charts for each solution found for all sub-problems(Virtual) and the optimal solution as well.

## Installation

```bash
pip install -i https://test.pypi.org/simple/ PyJackson==1.3.0
```

## Usage

```python
from jacksonpy import JacksonAlgo

########################## Example using text file ##########################

# Reading and manipulating data
data_path = "YOUR_PATH/input.txt"  # path to the data file
d = JacksonAlgo.Data(data_path)  # create a Data object with the path to the data file
data = (
    d.get_job_durations()
)  # get the durations: list of list of integers [[J1, dur1, dur2, dur3], [J2, dur1, dur2, dur3] ...]

# Solving the problem
al = JacksonAlgo.JackAlgo(data)  # create a JackAlgo object with the data

print(al)  # print the problem details

preparedData = al.prepareData()  # prepare the data for the algorithm
cmaxVirtual, _, __ = al.get_cmax_virtual(
    preparedData
)  # get the cmaxVirtual result of the virtual sub-problems
result = al.solve(
    cmaxVirtual
)  # solve the problem and save the result in the result variable
al.generate_pdf_file(
    results=result
)  # generate a pdf file with the result of the problem


########################## Example using Json file ##########################

# Reading and manipulating data
data_path = "YOUR_PATH//input.json"  # path to the data file
d = JacksonAlgo.Data(data_path)  # create a Data object with the path to the data file
data = (
    d.get_job_durations()
)  # get the durations: list of list of integers [[J1, dur1, dur2, dur3], [J2, dur1, dur2, dur3] ...]
print(data)  # print the data

# Solving the problem
al = JacksonAlgo.JackAlgo(data)  # create a JackAlgo object with the data

print(al)  # print the problem details

preparedData = al.prepareData()  # prepare the data for the algorithm
cmaxVirtual, _, __ = al.get_cmax_virtual(
    preparedData
)  # get the cmaxVirtual result of the virtual sub-problems
result = al.solve(
    cmaxVirtual
)  # solve the problem and save the result in the result variable
al.generate_pdf_file(
    results=result
)  # generate a pdf file with the result of the problem

########################## Example using 2d array ##########################

# Reading and manipulating data (defined as a lis of lists of integers)
data = [
    [1, 7, 5, 6, 9, 10],
    [2, 4, 6, 5, 8, 1],
    [3, 8, 2, 4, 3, 7],
    [4, 6, 3, 9, 7, 5],
    [5, 5, 7, 3, 5, 9],
]  # list of list of integers [[J1, dur1, dur2, dur3], [J2, dur1, dur2, dur3] ...]

# Solving the problem
al = JacksonAlgo.JackAlgo(data)  # create a JackAlgo object with the data

print(al)  # print the problem details

preparedData = al.prepareData()  # prepare the data for the algorithm
cmaxVirtual, _, __ = al.get_cmax_virtual(
    preparedData
)  # get the cmaxVirtual result of the virtual sub-problems
result = al.solve(
    cmaxVirtual
)  # solve the problem and save the result in the result variable
al.generate_pdf_file(
    results=result
)  # generate a pdf file with the result of the problem

########################## Example using dictionary ##########################

# Reading and manipulating data (defined as a lis of lists of integers)
data = {
    "Task 1": [3, 4, 6, 5],
    "Task 2": [2, 3, 6, 9],
    "Task 3": [8, 9, 2, 6],
    "Task 4": [7, 6, 3, 2],
    "Task 5": [3, 6, 4, 5],
    "Task 6": [5, 8, 7, 9],
}  # dictionary of lists of integers {'Task 1': [3, 4, 6, 5], 'Task 2': [2, 3, 6, 9], ...}

# Solving the problem
al = JacksonAlgo.JackAlgo(data)  # create a JackAlgo object with the data

print(al)  # print the problem details

preparedData = al.prepareData()  # prepare the data for the algorithm
cmaxVirtual, _, __ = al.get_cmax_virtual(
    preparedData
)  # get the cmaxVirtual result of the virtual sub-problems
result = al.solve(
    cmaxVirtual
)  # solve the problem and save the result in the result variable
al.generate_pdf_file(
    results=result
)  # generate a pdf file with the result of the problem
```
## Results

- ![Gantt Chart Output](https://github.com/th-rpy/jackson_job_shop_scheduling/blob/main/example/output/ImagesOutput/Gantt_Chart_virtual1_cmax_47.png) 

- ![PDF file Generated](https://github.com/th-rpy/jackson_job_shop_scheduling/blob/main/example/output/Algo_Cds_Output.pdf)

## 🛡 License

[![License](https://img.shields.io/github/license/th-rpy/jackson_job_shop_scheduling)](https://github.com/th-rpy/jackson_job_shop_scheduling/blob/master/LICENSE)

This project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/th-rpy/jackson_job_shop_scheduling/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{jackson_job_shop_scheduling,
  author = {PolyMtl},
  title = {Implementation of a mathematical model in Python to solve an assignment problem in Job Shop environments. With its respective Gantt chart.},
  year = {2022},
  publisher = {S.Thamer},
  journal = {Research Report},
  howpublished = {\url{https://github.com/th-rpy/jackson_job_shop_scheduling}}
}
```
