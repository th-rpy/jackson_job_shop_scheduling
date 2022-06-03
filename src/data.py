import csv
import os
import shutil
import getpass
import hashlib
import sys
import io
import operator


class Data():
    
    """
    Class to store the data of the job shop scheduling problem 
    
    Args: 
        path: path to the data file if you want to use a text file to store data
        
    Returns:
        durations_flatten: list of durations
        durations_sorted_int: list of lists of integers: 2d-array of durations
        
    Examples:
        >>> d = Data("data.txt")
        >>> d.get_job_durations() # get the durations: list of list of integers [[J1, dur1, dur2, dur3], [J2, dur1, dur2, dur3] ...]
        >>> print(d) 
           Job i	dur J/M1	dur J/M2	dur J/M3
            [	1	,	 	7	,	 	1	,	 	6	]
            [	2	,	 	4	,	 	3	,	 	2	]
            [	3	,	 	3	,	 	2	,	 	4	]
            [	4	,	 	8	,	 	2	,	 	1	]
            [	5	,	 	5	,	 	1	,	 	3	] 

    """
    
    def __init__(self, path):
        
        """
        path: path to the data file if you want 
            to use a text file to store data;
        """
        self.path = path 
        
    def get_job_durations(self):
        
        global file 
        
        try:
            file = open(self.path, 'r') # open the file
            Csv = csv.reader(file, delimiter=',') # read the file
            durations_sorted = sorted(Csv, key=operator.itemgetter(0)) # sort the file by job number
            nb_jobs = len(durations_sorted) # get the number of jobs
            durations_sorted = sorted(durations_sorted, key=lambda x: int(x[0])) # sort the file by job number
            durations_sorted_int = [[int(i) for i in lj] for lj in durations_sorted] # convert to a list of lists of integers
            durations_flatten = [] # create a list to store the durations
            for i in range(len(durations_sorted)):
                for j in range(len(durations_sorted[i])):
                    durations_flatten.append(durations_sorted_int[i][j]) # add the durations to the list
                    
        except FileNotFoundError:
            print("File name not found") # if the file is not found
            
        except IOError:
            print("Open file error") # if the file is not open

        return durations_sorted_int #durations_flatten #
    
    def get_jobs_nb(self):
        return len(self.get_job_durations()[1])
    
    def get_machines_nb(self):
        return len(self.get_job_durations()[1][0]) - 1 
    
    def __str__(self):
        
        durations = self.get_job_durations()[1] # get the durations
        list_jobs  = ["Job i"] # create a list to store the jobs
        for i in range(1, len(durations[0])):
            list_jobs.append("dur J/M{0}".format(i)) # add the jobs to the list

        data = [] # create a list to store the data
        data.append(list_jobs) # add the jobs to the list
        for i in durations:
            data.append(str(i)) # add the durations to the list

        return "Job Shop scheduling with {} jobs and {} machines. \nThe durations data: \n".format(
            self.get_jobs_nb(), self.get_machines_nb()) + "\n".join(["\t".join(i) for i in data]) # print the data
