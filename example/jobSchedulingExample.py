from jacksonpy.data import *
from jacksonpy.JacksonAlgo import *
import json
import os.path

########################## Example using text file ##########################

# Reading and manipulating data
data_path = (
    "jackson_job_shop_scheduling/src/jacksonpy/input.txt"  # path to the data file
)
d = Data(data_path)  # create a Data object with the path to the data file
data = (
    d.get_job_durations()
)  # get the durations: list of list of integers [[J1, dur1, dur2, dur3], [J2, dur1, dur2, dur3] ...]

# Solving the problem
al = JackAlgo(data)  # create a JackAlgo object with the data

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
data_path = (
    "jackson_job_shop_scheduling/src/jacksonpy/input.json"  # path to the data file
)
d = Data(data_path)  # create a Data object with the path to the data file
data = (
    d.get_job_durations()
)  # get the durations: list of list of integers [[J1, dur1, dur2, dur3], [J2, dur1, dur2, dur3] ...]
print(data)  # print the data

# Solving the problem
al = JackAlgo(data)  # create a JackAlgo object with the data

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
al = JackAlgo(data)  # create a JackAlgo object with the data

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
data = data = {
    "Task 1": [3, 4, 6, 5],
    "Task 2": [2, 3, 6, 9],
    "Task 3": [8, 9, 2, 6],
    "Task 4": [7, 6, 3, 2],
    "Task 5": [3, 6, 4, 5],
    "Task 6": [5, 8, 7, 9],
}  # list of list of integers [[J1, dur1, dur2, dur3], [J2, dur1, dur2, dur3] ...]

# Solving the problem
al = JackAlgo(data)  # create a JackAlgo object with the data

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
