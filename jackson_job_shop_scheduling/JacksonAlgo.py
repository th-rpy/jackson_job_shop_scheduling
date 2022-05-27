"""Example of code."""
import data 

class JackAlgo():
    
    """
    
    """
    
    def __init__(self, duration_data):
        
        """
        """
        self.duration_data = duration_data
        self.nb_jobs = len(self.duration_data[1])
        self.nb_machines = len(self.duration_data[0]) - 1

    def get_list(self):
        list_ = []
        for n in range(len(sum(self.duration_data, [])) // self.nb_jobs):
            list_.append(sum(self.duration_data, [])[n * self.nb_jobs:(n + 1) * self.nb_jobs])
        return list_[-1]
    
    def fun_calculate(self, k):
        list_2 = []
        list_dur = self.get_list()
        for n in range(len(list_dur)):
            list_2.append([list_dur[n][0], sum(list_dur[n][1:k]),
                           sum(list_dur[n][-1:-k:-1])])
        return list_2
    
    def __str__(self):
        r = [i + 2 for i in range(self.nb_jobs - 2)]
        # print(liste)

        """        for i in r:
            kk = self.fun_calculate(i)
            print(kk)
            
        lll = []
        for i in range(len(kk) // self.nb_jobs):
            lll.append(kk[i * self.nb_jobs:(i + 1) * self.nb_jobs])"""

        return '{}'.format(self.get_list())
    

data_path = 'jackson_job_shop_scheduling/jackson_job_shop_scheduling/input.txt'       
d = data.Data(data_path) 

al = JackAlgo(d.get_job_durations())
print(al)