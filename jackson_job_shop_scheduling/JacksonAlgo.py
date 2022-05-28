"""Example of code."""
import data 
import os
import shutil
import getpass
import hashlib
import sys
import io
import email.mime.application
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mimetypes
import smtplib
from random import randrange
import numpy as np
import csv
import operator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors as cl
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

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
    
    def get_cmax_virtual(self):
        
        cmaxValue_list, job_sequence = [], []
        for T in self.clean_data():
            sort_1 = sorted(T, key=operator.itemgetter(1))
            sort_2 = sorted(T, key=operator.itemgetter(2), reverse=True)
            
            A, B, C = [], [], []
            # append to A
            for j in range(len(sort_1)):
                if int(sort_1[j][1]) < int(sort_1[j][2]) or int(sort_1[j][1]) == int(sort_1[j][2]):
                    A.append(sort_1[j])
            
            #Append to B       
            l = len(sort_2)
            for j in range(l):
                if int(sort_2[j][1]) > int(sort_2[j][2]):
                    B.append(sort_2[j])
                
            # Extend A and B
            C = A + B 
            for i in range(len(C)):
                job_sequence.append(C[i][0])
            
            job_dur, cmax_values = [], []

            job_dur.append([0, C[0][1]])
            for i in range(1, len(C)):
                job_dur.append([job_dur[i-1][1], job_dur[i-1][1] + C[i][1]])
            cmax_values.append([job_dur[0][1], job_dur[0][1]+C[0][2]])
            for i in range(1, len(job_dur)):
                if job_dur[i][1] >= cmax_values[i-1][1]:
                    cmax_values.append([job_dur[i][1], job_dur[i][1]+C[i][2]])
                else:
                    cmax_values.append([cmax_values[i - 1][1], cmax_values[i-1][1] + C[i][2]])
            # Save the cmax value
            cmaxValue_list.append(cmax_values[-1][1])
            
        return [job_sequence[i:i+self.nb_jobs] for i in range(0, len(job_sequence), self.nb_jobs)], cmaxValue_list
            
              
    def __str__(self):

        return str(self.get_cmax_virtual())
    

data_path = 'jackson_job_shop_scheduling/jackson_job_shop_scheduling/input.txt'       
d = data.Data(data_path) 
data = d.get_job_durations()[1]
al = JackAlgo(data)
print(al)
