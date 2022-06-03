"""Tests for hello function."""
#import pytest

"""data_path = 'jackson_job_shop_scheduling/src/jacksonpy/input.txt'       
d = Data(data_path) 
data = d.get_job_durations()
al = JackAlgo([[1, 7, 5, 6,9,10], [2, 4, 6, 5, 8,1], [3, 8, 2, 4,3,7], [4, 6, 3, 9,7,5], [5, 5, 7, 3,5,9]])
print(al)"""
import json
import os.path

data_path = 'jackson_job_shop_scheduling/tests/test_example/input.json'
extension = os.path.splitext(data_path)[1]

if extension == '.json':
    with open(data_path) as f:
        data = json.load(f)
        print(data)

data = {
    "Task 1": [3,4,6,5],
    "Task 2": [2,3,6,9],
    "Task 3": [8,9,2,6],
    "Task 4": [7,6,3,2],
    "Task 5": [3,6,4,5],
    "Task 6": [5,8,7,9]
}

dur = [[k+1] + list(map(int, v[1])) for k, v in enumerate(data.items())]
print(dur)

al = JackAlgo({
    "Task 1": [3,4,6,5],
    "Task 2": [2,3,6,9],
    "Task 3": [8,9,2,6],
    "Task 4": [7,6,3,2],
    "Task 5": [3,6,4,5],
    "Task 6": [5,8,7,9]
})
al.solve()