"""Example of code."""

from jacksonpy.utils import (
    gant_list,
    create_dir,
    func_trait,
    create_pdf_file,
    add_table_to_pdf,
)
from jacksonpy.data import *
from tqdm import tqdm
import os
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
import csv
import operator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors as cl
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import warnings


class JackAlgo:

    """
    Class to solve job shop scheduling problem from  a list of lists of tasks.

    Args:
        duration_data: list of lists of tasks. Each task is a (job,machine) pair.
        output_dir: directory to save the output files: by default, the output files are saved in the current directory.
    Returns:
        PDF file with the results of the algorithm. The PDF file is saved in the output_dir directory.

    Examples:
        data_duration = {
            "Task 1": [3, 4, 6, 5],
            "Task 2": [2, 3, 6, 9],
            "Task 3": [8, 9, 2, 6],
            "Task 4": [7, 6, 3, 2],
            "Task 5": [3, 6, 4, 5],
            "Task 6": [5, 8, 7, 9],
        }  # dictionary of lists of integers {'Task 1': [3, 4, 6, 5], 'Task 2': [2, 3, 6, 9], ...}

        # Solving the problem
        al = JacksonAlgo.JackAlgo(data_duration)  # create a JackAlgo object with the data

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
    """

    list_pre_cleaned = []
    list_cleaned = []
    list_cleaned_ = []
    Algo_details = "This heuristic simply consists in generating m-1 sub-problems of the 2-machine flow-shop type, solving them and selecting the best solution. \
        The sub-problem k is defined by :\nProcessing time on the virtual machine 1 : pi1= the sum of pij (j in [1..k]) \nProcessing time on the virtual machine 2 : pi2= the sum of pij (j in [k+1 .. m]). \
        \n For each of these problems, the optimal order is calculated with the Johnson algorithm and this order is then applied to the basic problem to obtain the Cmax(k).\
        Then, it is enough to choose the best one on the whole Cmax(k)."
    nb_sec = 2
    p = 0
    warnings.filterwarnings("ignore", category=FutureWarning)

    def __init__(self, duration_data, output_dir="output"):

        """ """
        self.duration_data = duration_data
        if isinstance(self.duration_data, list):
            self.nb_machines = len(self.duration_data[0]) - 1
        elif isinstance(self.duration_data, dict):
            self.nb_machines = len(list(self.duration_data.values())[0])
            self.duration_data = [
                [k + 1] + list(map(int, v[1]))
                for k, v in enumerate(self.duration_data.items())
            ]
        self.nb_jobs = len(self.duration_data)
        self.output_dir = output_dir

    def get_list(self):

        assert self.duration_data is not None, "duration_data is None"
        assert self.duration_data[0] is not None, "duration_data[0] is None"
        assert (
            len(self.duration_data[0]) == self.nb_machines + 1
        ), "duration_data[0] is not of length {0}".format(self.nb_machines + 1)
        assert isinstance(self.duration_data, list), "duration_data is not a list"
        assert (
            len(self.duration_data) == self.nb_jobs
        ), "duration_data is not of length {0}".format(self.nb_jobs)
        assert isinstance(self.duration_data[0], list), "duration_data is not a list"

        list_ = []
        for n in range(len(sum(self.duration_data, [])) // (self.nb_machines + 1)):
            list_.append(
                sum(self.duration_data, [])[
                    n * (self.nb_machines + 1) : (n + 1) * (self.nb_machines + 1)
                ]
            )
        return list_

    def fun_calculate(self, k):
        list_2 = []
        list_dur = self.get_list()
        for n in range(len(list_dur)):
            list_2.append(
                [list_dur[n][0], sum(list_dur[n][1:k]), sum(list_dur[n][-1:-k:-1])]
            )
        return list_2

    def prepareData(self):
        warnings.filterwarnings("ignore", category=FutureWarning)
        r = [
            i + 2 for i in range(self.nb_machines + 1 - 2)
        ]  # create a list of integers

        for i in r:
            JackAlgo.list_pre_cleaned = self.fun_calculate(i)  # get the list of lists
            JackAlgo.list_cleaned.append(
                JackAlgo.list_pre_cleaned
            )  # add the list to the list of lists

        for i in range(len(JackAlgo.list_cleaned[0]) // (self.nb_jobs)):
            JackAlgo.list_cleaned_.append(
                JackAlgo.list_cleaned[0][i * (self.nb_jobs) : (i + 1) * (self.nb_jobs)]
            )

        return JackAlgo.list_cleaned  # return the cleaned list of lists

    def get_cmax_virtual(self, preparedData):
        warnings.filterwarnings("ignore", category=FutureWarning)
        cmaxValue_list, job_sequence, flatten_result = [], [], []
        for T in preparedData:
            sort_1 = sorted(T, key=operator.itemgetter(1))
            sort_2 = sorted(T, key=operator.itemgetter(2), reverse=True)

            A, B, C = [], [], []
            # append to A
            for j in range(len(sort_1)):
                if int(sort_1[j][1]) < int(sort_1[j][2]) or int(sort_1[j][1]) == int(
                    sort_1[j][2]
                ):
                    A.append(sort_1[j])

            # Append to B
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
                job_dur.append([job_dur[i - 1][1], job_dur[i - 1][1] + C[i][1]])
            cmax_values.append([job_dur[0][1], job_dur[0][1] + C[0][2]])
            for i in range(1, len(job_dur)):
                if job_dur[i][1] >= cmax_values[i - 1][1]:
                    cmax_values.append([job_dur[i][1], job_dur[i][1] + C[i][2]])
                else:
                    cmax_values.append(
                        [cmax_values[i - 1][1], cmax_values[i - 1][1] + C[i][2]]
                    )
            # Save the cmax value
            cmaxValue_list.append(cmax_values[-1][1])
            flatten_result.append(cmax_values[-1][1])

        return (
            flatten_result,
            [
                job_sequence[i : i + self.nb_jobs]
                for i in range(0, len(job_sequence), self.nb_jobs)
            ],
            cmaxValue_list,
        )

    def solve(self, flatten_result):

        global list_data_copy, gant_data, list_list_gant, nb_sec
        warnings.filterwarnings("ignore", category=FutureWarning)
        create_dir(self.output_dir)
        _, story = create_pdf_file()
        nb_sec = JackAlgo.nb_sec + 1
        story, nb_sec = self.add_section_to_pdf(
            story, "Algorithm:", JackAlgo.Algo_details, nb_sec
        )

        story, nb_sec = self.add_section_to_pdf(
            story, self.problem_details()[0], self.problem_details()[1], nb_sec
        )
        table = self.prepare_table()
        story = add_table_to_pdf(table, story)
        story = self.add_section_to_pdf(
            story, "Visualizing Results with Gantt Charts: ", "", nb_sec
        )
        # flatten_result = self.get_cmax_virtual()[0].copy()
        list_data = []
        list_data_copy = []
        gant_data = []
        p = JackAlgo.p
        l_ = self.nb_jobs + 1
        klk, klks = {}, {}
        list_list_gant = []
        print("Solving started... Please wait...\n")
        for i in range(len(flatten_result) // l_):
            list_data.append(flatten_result[i * l_ : (i + 1) * l_])
        with tqdm(
            total=100,
            desc="Solving Subproblem ... ",
            bar_format="{l_bar}{bar} [ time left: {remaining} ]",
        ) as pbar:
            for p in range(len(list_data)):

                h, hc = [], []
                for i in range(len(list_data[p]) - 1):
                    # print("{}".format(s[p][i]))
                    h.append(list_data[p][i])
                    fvg = str(list_data[p][i]) + "=>"
                    hc.append(fvg)
                db1, db3 = [], []
                list_excel = []
                # print(list_data[p])
                list_data_copy = list_data[p][:-1]
                gant_data = []
                # print(fl_1)
                for i in list_data_copy:
                    gant_data.append(self.get_list()[i - 1])
                # print(gant_data)
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
                # print( db1 )
                # print( db3 )
                for i in range(1, b):
                    cc1 = lcf[(c * i) : c * (i + 1)]
                    db4 = []
                    db4.append([db3[0][1], db3[0][1] + cc1[0][2]])
                    for i in range(1, len(db3)):
                        if db3[i][1] >= db4[i - 1][1]:
                            db4.append([db3[i][1], db3[i][1] + cc1[i][2]])
                        else:
                            db4.append([db4[i - 1][1], db4[i - 1][1] + cc1[i][2]])
                    # print( db4 )
                    db3 = db4
                    list_excel.append(db4)
                    # print(list_excel)
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
                new = np.array(
                    np.loadtxt(
                        "output/TxtsOutput/gantt_file({0}).txt".format(p),
                        delimiter=",",
                        unpack=True,
                    )
                )
                # print(new)
                htl = []
                for j in range(1, new.shape[0]):
                    htl.append(new[j][0])
                # print(htl)
                ht = list(set(htl))
                ht = sorted(ht)
                htt1 = [(ht[i] + ht[i + 1]) / 2 for i in range(len(ht) - 1)]
                # print(set(htl))
                htt = sorted(htt1)
                # print(htt)
                cmap = plt.get_cmap("gnuplot")
                colors = [cmap(i) for i in np.linspace(0, 1, 2 * l_)]
                for i in range(1, new.shape[0] - 1, 2):
                    plt.hlines(new[0], new[i], new[i + 1], colors=colors[i], lw=28)
                    plt.text(htt[int((i - 1) / 2)], 1, str(h[int(i / 2)]))
                    cv = 0.0
                    """while cv < new[0][0]:
                        if cv == 0.0:
                            plt.text(new[i][0]-0.1/2, cv-0.25,
                                    str(new[i][0]), color=colors[i])
                            plt.text(new[i+1][0]-0.1/2, cv-0.25,
                                    str(new[i+1][0]), color=colors[i])
                        #plt.text(new[i][0]-0.1, cv, "|", color=colors[i])
                        #plt.text(new[i+1][0]-0.1, cv, "|", color=colors[i])
                        cv += 0.2"""
                    plt.grid(True)

                for j in range(1, new.shape[1]):
                    for o in range(1, new.shape[0]):
                        htl.append(new[o][0])
                    ht = list(set(htl))
                    htt = [(ht[i] + ht[i + 1]) / 2 for i in range(len(ht) - 1)]
                    for i in range(1, new.shape[0] - 1, 2):
                        plt.hlines(
                            new[0][j],
                            new[i][j],
                            new[i + 1][j],
                            colors=colors[i],
                            lw=28,
                        )
                        plt.text(
                            (new[i + 1][j] + new[i][j]) / 2,
                            new[0][j],
                            str(h[int(i / 2)]),
                        )
                        cv = 0.0
                        """while cv < new[0][j]:
                            if cv == 0.0:
                                pass
                                #plt.text(new[i][j]-0.05, cv+(new[0][j]-1)
                                        #* .1, str(new[i][j]), color=colors[i])
                                #plt.text(new[i+1][j]-.05, cv+(new[0][j]-1)
                                        #* .1, str(new[i+1][j]), color=colors[i])
                            #plt.text(new[i][j]-0.1, cv, "|", color=colors[i])
                            #plt.text(new[i+1][j]-0.1, cv, "|", color=colors[i])
                            cv += 0.2"""
                        plt.grid(True)

                plt.xlabel("Time(j)")
                plt.ylabel("Machines")
                plt.title(
                    "Job Scheduling Problem: {1} Jobs through {0} Machines".format(
                        b + 1, l_ - 1
                    )
                    + "\n"
                    + "\t"
                    + "Gantt Chart (seq ={0} with Cmax_{2} = {1})".format(
                        h, list_excel[-1][-1][-1], p
                    )
                )
                chh = ""
                for i in hc:
                    chh += i
                chh = chh[:-2]
                klk[chh] = [list_data[p][l_ - 1], list_excel[-1][-1][-1]]
                klks[chh] = list_excel[-1][-1][-1]
                plt.yticks([i for i in range(1, b + 2)])
                plt.ylim(0, b + 2)
                plt.xticks([i for i in range(0, list_excel[-1][-1][-1] + 2, 4)])
                plt.xlim([0, list_excel[-1][-1][-1] + 2])
                plt.margins(0, 1)
                S = func_trait(list_excel[-1][-1][-1], b + 1, 0, "|")
                plt.annotate(
                    "Cmax = " + str(list_excel[-1][-1][-1]),
                    xy=(list_excel[-1][-1][-1], b + 1),
                    xytext=(0.75 * list_excel[-1][-1][-1], b + 1.6),
                    arrowprops=dict(facecolor="green", shrink=0.05),
                )
                plt.text(list_excel[-1][-1][-1], b + 1, S)
                manager = plt.get_current_fig_manager()
                plt.savefig(
                    "output/ImagesOutput/Gantt_Chart_virtual{0}_cmax_({1}).png".format(
                        p, list_excel[-1][-1][-1]
                    ),
                    bbox_inches="tight",
                )
                plt.clf()
                pbar.update(100 / (self.nb_machines - 1))
        print("\n Done ;) ... \n")
        print(
            "The Gantt Chart images are saved in "
            + os.getcwd()
            + "/output/ImagesOutput/"
        )
        return (
            story,
            list_data,
            dict(sorted(klks.items(), key=lambda item: item[1])),
            klk,
        )  # , list_list_gant, list_data, gant_data, self.nb_jobs,
        # self.nb_machines

    def add_virtual_results(self, lists):

        styles = getSampleStyleSheet()
        __, _, result_final, dict_results = lists
        Story = list(lists[0][0]).copy()
        result_final = sorted(result_final.items(), key=operator.itemgetter(1))
        nb_pb = 0
        paths = []
        for key, value in dict_results.items():

            nb_pb += 1
            ptext = "<font size=13 color=green>{0}) The result of subproblem number {0} solved by Johnson's algorithm is : </font>".format(
                nb_pb
            )
            Story.append(Paragraph(ptext, styles["Normal"]))
            Story.append(Spacer(1, 12))
            ptext = (
                "The optimal scheduling is therefore: {0}".format(key)
                + "with cmax value of the real problem in this case is {0}".format(
                    value[1]
                )
                + "\n "
            )
            ptext = ptext.replace(" ", "&nbsp;")
            ptext = ptext.replace("\n", "<br />")
            ptext = ptext.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
            Story.append(Paragraph(ptext, styles["Normal"]))
            Story.append(Spacer(1, 12))
            im = Image(
                "output/ImagesOutput/Gantt_Chart_virtual{0}_cmax_({1}).png".format(
                    nb_pb - 1, value[1]
                ),
                hAlign="LEFT",
            )
            paths.append(value[1])
            Story.append(im)
            if nb_pb == self.nb_machines - 1:
                break
        idx = paths.index(min(paths))
        Story.append(Spacer(1, 12))
        Story = self.add_section_to_pdf(
            Story,
            "Final Scheduling Result:",
            "To conclude, among the results of the subproblems, we retain the following optimal sequence solution :|| {0} || with a value of Cmax = {1} ".format(
                result_final[0][0], result_final[0][1]
            ),
            nb_sec,
        )[0]

        im_final = Image(
            "output/ImagesOutput/Gantt_Chart_virtual{0}_cmax_({1}).png".format(
                idx, min(paths)
            ),
            hAlign="LEFT",
        )
        Story.append(im_final)
        return Story

    def generate_pdf_file(self, results):
        print("Generating PDF file...\n")
        story = self.add_virtual_results(results)
        doc = create_pdf_file()[0]
        doc.build(story)
        print("Done ;) ... \n")
        print("The PDF file is saved in " + os.getcwd() + "/output/Algo_Cds_Output.pdf")

    def prepare_table(self):
        data = [i.copy() for i in self.duration_data]
        l1 = len(data)
        l0 = len(data[0])
        machines = ["Job / Machine"]
        machines.extend(["M " + str(i) for i in range(1, l0)])
        for i in range(l1):
            data[i][0] = "J " + str(data[i][0])
        data.insert(0, machines)
        return data

    def problem_details(self):
        cntx = "Your Problem Details:"
        details = "Your problem is a job scheduling problem with {0} jobs and {1} machines.\n This table resume the \
        tasks durations. Each task is a (job,machine) pair.".format(
            self.nb_jobs, self.nb_machines
        )
        return cntx, details

    def add_section_to_pdf(self, story, title, content, section_nb):

        styles = getSampleStyleSheet()
        story.append(
            Paragraph(
                "<font size=15 color=black>{}</font>".format(
                    str(section_nb) + ".   " + title
                ),
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 20))
        content = content.replace("\n", "<br />")
        story.append(Paragraph(content, styles["Normal"]))
        story.append(Spacer(1, 15))
        section_nb += 1

        return story, section_nb

    def __str__(self):
        return "Your problem is a Job Shop scheduling of {0} tasks through {1} machines.".format(
            self.nb_jobs, self.nb_machines
        )
