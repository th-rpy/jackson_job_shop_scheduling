"""Example of code."""
import data 
import operator
import csv

class JackAlgo():
    
    """
    
    """
    list_pre_cleaned = []
    list_cleaned = []
    list_cleaned_ = []
    
    def __init__(self, duration_data):
        
        """
        """
        self.duration_data = duration_data
        self.nb_jobs = len(self.duration_data)
        self.nb_machines = len(self.duration_data[0]) - 1

    def get_list(self):
        list_ = []
        for n in range(len(sum(self.duration_data, [])) // (self.nb_machines + 1)):
            list_.append(sum(self.duration_data, [])[n * (self.nb_machines + 1):(n + 1) * (self.nb_machines + 1)])
        return list_
    
    def fun_calculate(self, k):
        list_2 = []
        list_dur = self.get_list()
        for n in range(len(list_dur)):
            list_2.append([list_dur[n][0], sum(list_dur[n][1:k]),
                           sum(list_dur[n][-1:-k:-1])])
        return (list_2)
    
    def clean_data(self):
        
        r = [i + 2 for i in range(self.nb_machines + 1 - 2)] # create a list of integers
        
        for i in r:
            JackAlgo.list_pre_cleaned = self.fun_calculate(i) # get the list of lists
            JackAlgo.list_cleaned.append(JackAlgo.list_pre_cleaned) # add the list to the list of lists
            
        for i in range(len(JackAlgo.list_cleaned[0]) // (self.nb_jobs)):
            JackAlgo.list_cleaned_.append(JackAlgo.list_cleaned[0][i * (self.nb_jobs):(i + 1) * (self.nb_jobs)])
            
        return JackAlgo.list_cleaned # return the cleaned list of lists
    
    def __str__(self):
        return str(self.clean_data())
    

data_path = 'jackson_job_shop_scheduling/jackson_job_shop_scheduling/input.txt'       
d = data.Data(data_path) 
data = d.get_job_durations()[1]
al = JackAlgo(data)
print(al)
