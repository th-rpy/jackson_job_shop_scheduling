"""Example of code."""

from utils import gant_list, create_dir, func_trait
import data 
import os
import shutil
import getpass
import hashlib
import sys
import io
import mimetypes
import smtplib
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
import csv
import operator


class JackAlgo():
    
    """
    
    """
    list_pre_cleaned = []
    list_cleaned = []
    list_cleaned_ = []
    
    def __init__(self, duration_data, output_dir = 'output'):
        
        """
        """
        self.duration_data = duration_data
        self.nb_jobs = len(self.duration_data)
        self.nb_machines = len(self.duration_data[0]) - 1
        self.output_dir = output_dir

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
        
        cmaxValue_list, job_sequence, flatten_result = [], [], []
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
                flatten_result.append(C[i][0])
            
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
            flatten_result.append(cmax_values[-1][1])
            
        return [flatten_result, [job_sequence[i:i+self.nb_jobs] for i in range(0, 
                                len(job_sequence), self.nb_jobs)], cmaxValue_list]
        
    def gant_data(self):

        global list_data_copy, gant_data, list_list_gant
        create_dir(self.output_dir)
        flatten_result = self.get_cmax_virtual()[0]
        list_data = []
        gant_data = []
        l_ = self.nb_jobs + 1
        klk, klks = {}, {}
        list_list_gant = []
        for i in range(len(flatten_result) // l_):
            list_data.append(flatten_result[i * l_:(i + 1) * l_])
        for p in range(len(list_data)):
            h, hc = [], []
            for i in range(len(list_data[p]) - 1):
                #print("{}".format(s[p][i]))
                h.append(list_data[p][i])
                fvg = str(list_data[p][i])+"=>"
                hc.append(fvg)
            db1, db3 = [], []
            list_excel = []
            #print(list_data[p])
            list_data_copy = list_data[p][:-1]
            gant_data = []
            # print(fl_1)
            for i in list_data_copy:
                gant_data.append(self.get_list()[i - 1])
            #print(gant_data)
            lc = []
            for j in gant_data:
                for i in range(1, len(gant_data[0]) - 1):
                    lc.append([j[0], j[i], j[i + 1]])

            # print(lc)
            b = len(self.get_list()[0]) - 2
            c = len(list_data_copy)
            lcf = []
            for j in range(0, b):
                x = b + j
                for i in range(0, c):
                    lcf.append(lc[x - b])
                    x += b

            cc = lcf[0:c]
            # print("rfrfr",cc)
            db1 = gant_list(cc)[0]
            db3 = gant_list(cc)[1]
            list_excel = [db1, db3]
            #print( db1 )
            #print( db3 )
            for i in range(1, b):
                cc1 = lcf[(c * i):c * (i + 1)]
                db4 = []
                db4.append([db3[0][1], db3[0][1] + cc1[0][2]])
                for i in range(1, len(db3)):
                    if db3[i][1] >= db4[i - 1][1]:
                        db4.append([db3[i][1], db3[i][1] + cc1[i][2]])
                    else:
                        db4.append([db4[i - 1][1], db4[i - 1][1] + cc1[i][2]])
                #print( db4 )
                db3 = db4
                list_excel.append(db4)
                #print(list_excel)
            list_list_gant.append(list_excel)
            
            txt_gant = open("output/TxtsOutput/gantt_file({0}).txt".format(p), "w")
            k = 0
            for i in list_excel:
                k += 1
                ch = "{0},".format(k)
                for j in i:
                    ch += "{0},{1},".format(j[0], j[1])
                ch1 = ch[:-1] + "\n"
                txt_gant.write(ch1)
            txt_gant.close()
            f = int(l_ / 2) + 1
            new = np.array(np.loadtxt("output/TxtsOutput/gantt_file({0}).txt".format(
                p), delimiter=",", unpack=True))
            #print(new)
            htl = []
            for j in range(1, new.shape[0]):
                htl.append(new[j][0])
            # print(htl)
            ht = list(set(htl))
            ht = sorted(ht)
            htt1 = [(ht[i] + ht[i + 1]) / 2 for i in range(len(ht) - 1)]
            # print(set(htl))
            htt = sorted(htt1)
            #print(htt)
            cmap = plt.get_cmap("gnuplot")
            colors = [cmap(i) for i in np.linspace(0, 1, 2 * l_)]
            for i in range(1, new.shape[0] - 1, 2):
                plt.hlines(new[0], new[i], new[i + 1], colors=colors[i], lw=28)
                plt.text(htt[int((i - 1) / 2)], 1, str(h[int(i / 2)]))
                cv = 0.0
                while cv < new[0][0]:
                    if cv == 0.0:
                        plt.text(new[i][0]-0.1/2, cv-0.25,
                                str(new[i][0]), color=colors[i])
                        plt.text(new[i+1][0]-0.1/2, cv-0.25,
                                str(new[i+1][0]), color=colors[i])
                    plt.text(new[i][0]-0.1, cv, "|", color=colors[i])
                    plt.text(new[i+1][0]-0.1, cv, "|", color=colors[i])
                    cv += 0.2
                plt.grid(True)
                
            for j in range(1, new.shape[1]):
                for o in range(1, new.shape[0]):
                    htl.append(new[o][0])
                ht = list(set(htl))
                htt = [(ht[i] + ht[i + 1]) / 2 for i in range(len(ht) - 1)]
                for i in range(1, new.shape[0] - 1, 2):
                    plt.hlines(new[0][j], new[i][j], new[i + 1]
                            [j], colors=colors[i], lw=28, )
                    plt.text((new[i + 1][j] + new[i][j]) / 2,
                            new[0][j], str(h[int(i / 2)]))
                    cv = 0.0
                    while cv < new[0][j]:
                        if cv == 0.0:
                            plt.text(new[i][j]-0.05, cv+(new[0][j]-1)
                                    * .1, str(new[i][j]), color=colors[i])
                            plt.text(new[i+1][j]-.05, cv+(new[0][j]-1)
                                    * .1, str(new[i+1][j]), color=colors[i])
                        plt.text(new[i][j]-0.1, cv, "|", color=colors[i])
                        plt.text(new[i+1][j]-0.1, cv, "|", color=colors[i])
                        cv += 0.2
                    plt.grid(True)
            
            plt.xlabel("time(j)")
            plt.title("Ordanncement FlowShop: {0} machines et {1} Taches".format(b + 1,
                                                                             l_ - 1) + "\n" + "\t" + "Diagramme de Gantt (seq ={0} avec Cmax({2})={1})".format(
            h, list_excel[-1][-1][-1], p))
            chh = ""
            for i in hc:
                chh += i
            chh = chh[:-2]
            klk[chh] = [list_data[p][l_-1], list_excel[-1][-1][-1]]
            klks[chh] = [list_excel[-1][-1][-1]]
            plt.ylim(0, b + 2)
            plt.xlim([0, list_excel[-1][-1][-1] + 2])
            plt.margins(0, 1)
            S = func_trait(list_excel[-1][-1][-1], b+1, 0, "|")
            plt.annotate("Cmax=" + str(list_excel[-1][-1][-1]), xy=(list_excel[-1][-1][-1], b+1), xytext=(
                0.75*list_excel[-1][-1][-1], b+1.6), arrowprops=dict(facecolor='green', shrink=0.05))
            plt.text( list_excel[-1][-1][-1], b + 1, S )
            manager = plt.get_current_fig_manager()
            plt.savefig("output/ImagesOutput/output_diagram_gantt({0}).png".format(p), bbox_inches='tight')
            
        return colors, list_list_gant, list_data, gant_data, self.nb_jobs, self.nb_machines
    
        '''def plot_gant(self):

        global list_data_copy, gant_data, list_list_gant
        flatten_result = self.get_cmax_virtual()[0]
        list_data = []
        l_ = self.nb_jobs + 1
        for i in range(len(flatten_result) // l_):
            list_data.append(flatten_result[i * l_:(i + 1) * l_])
        for p in range(len(list_data)):
            ded = open("output/TxtsOutput/gantt_file({0}).txt".format(p), "w")
            k = 0

            for i in self.gant_data()[0]:
                print(i)
                k += 1
                ch = "{0},".format(k)
                for j in i:
                    ch += "{0},{1},".format(j[0], j[1])
                ch1 = ch[:-1] + "\n"
            ded.write(ch1)
            ded.close()
            f = int(l_ / 2) + 1
            
        return ch1'''
            
    def __str__(self):
        return str(self.gant_data()[0])
    

data_path = 'jackson_job_shop_scheduling/jackson_job_shop_scheduling/input.txt'       
d = data.Data(data_path) 
data = d.get_job_durations()[1]
al = JackAlgo(data)
print(al)
