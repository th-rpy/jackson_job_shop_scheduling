import operator
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Image,
)
from tqdm import tqdm

from jacksonpy.utils import gant_list, create_dir, func_trait, create_pdf_file, add_table_to_pdf


def add_section_to_pdf(story, title, content, section_nb):

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


class JobShopScheduler:
    """
    Handles the scheduling for job shop problems using a heuristic based on sub-problems.

    Attributes:
        duration_data (list): A list of job durations.
        nb_jobs (int): Number of jobs.
        nb_machines (int): Number of machines per job.
        output_dir (str): Directory path for outputs.
    """

    nb_sec = 2
    p = 0

    def __init__(self, duration_data, output_dir='output'):
        """
        Initializes the JobShopScheduler with job duration data and output directory.

        Args:
            duration_data (list or dict): Job duration data. If dict, format should map job to durations.
            output_dir (str): Path to the output directory.
        """
        self.list_cleaned = None
        self.nb_machines = None
        self.nb_jobs = None
        if isinstance(duration_data, dict):
            # Convert dict to list format
            duration_data = [[k + 1] + list(v) for k, v in enumerate(duration_data.values())]

        self.duration_data = duration_data
        self.output_dir = output_dir
        self.validate_data()

    def validate_data(self):
        """
        Validates the input duration_data to ensure all entries are correctly formatted.

        Raises:
            ValueError: If duration_data is empty, not a list, or inconsistent in lengths.
        """
        if not self.duration_data:
            raise ValueError("duration_data is empty")

        if not isinstance(self.duration_data, list):
            raise ValueError("duration_data must be a list")

        length = len(self.duration_data[0])
        for job in self.duration_data:
            if not isinstance(job, list) or len(job) != length:
                raise ValueError("All jobs must have the same number of machine durations including the job ID")

        self.nb_jobs = len(self.duration_data)
        self.nb_machines = length - 1  # Assuming first element is the job id

    def problem_details(self):
        """
        Constructs a summary of the job scheduling problem context.

        Returns:
            tuple: Contains two strings, the first is a header message and the second is a detailed
                   description of the problem including the number of jobs and machines, and
                   a note about the tasks' durations representation.
        """
        # Context message
        context = "Your Problem Details:"

        # Formatting the details message
        details = f"Your problem is a job scheduling problem with {self.nb_jobs} jobs and {self.nb_machines} machines.\n" \
                  "This table resumes the tasks' durations. Each task is a (job, machine) pair."

        return context, details

    def get_job_durations(self):
        # Validate the structure and content of duration_data
        assert isinstance(self.duration_data, list), "duration_data is not a list"
        assert self.duration_data is not None, "duration_data is None"
        assert all(isinstance(job, list) for job in self.duration_data), "Not all elements in duration_data are lists"
        assert len(
            self.duration_data) == self.nb_jobs, f"Expected {self.nb_jobs} jobs, but found {len(self.duration_data)}"
        assert all(len(job) == self.nb_machines + 1 for job in self.duration_data), \
            f"Each job should have {self.nb_machines + 1} durations"

        # Flattening the list of job durations just once
        flat_durations = sum(self.duration_data, [])

        # Calculate job durations based on the number of machines
        job_durations = [
            flat_durations[i * (self.nb_machines + 1): (i + 1) * (self.nb_machines + 1)]
            for i in range(len(flat_durations) // (self.nb_machines + 1))
        ]

        return job_durations

    def display_job_durations(self):
        """
        Prints the job durations in a formatted table.
        """
        header = ["Job ID"] + [f"M {i + 1}" for i in range(self.nb_machines)]
        print("\t".join(header))
        for job in self.duration_data:
            print("\t".join(map(str, job)))

    def calculate_aggregated_durations(self, k):
        """
        Aggregates the machine durations for each job up to index `k` and from the end backwards to `k`.

        Args:
            k (int): The pivot index to calculate the sum up to (exclusive) and from the end to.

        Returns:
            list: A modified list where each job now includes its ID and two summed durations.
        """
        aggregated_durations = []
        job_durations = self.get_job_durations()

        for job in job_durations:
            if k >= len(job):
                raise ValueError("k is out of the valid range for job durations")
            # Calculate sum from start up to k (exclusive) and from end to k (exclusive)
            sum_first_k = sum(job[1:k+1])  # sum from first duration to kth duration (inclusive)
            sum_last_k = sum(job[-k:]) if k != 0 else 0  # sum last k durations, handle k=0 case
            aggregated_durations.append([job[0], sum_first_k, sum_last_k])

        return aggregated_durations

    def prepare_data(self):
        """
        Prepares data by aggregating job durations for each machine and then transposing the result.
        This transformation makes the data structured by jobs rather than by machines.

        Returns:
            list of list: A list where each sub-list contains aggregated job durations for each machine,
                          restructured to group by jobs across machines.
        """
        # Using a list comprehension to generate and aggregate durations more concisely
        aggregated_durations = [self.calculate_aggregated_durations(i) for i in range(2, self.nb_machines + 1)]

        # Transposing the matrix to group by jobs instead of machines
        # The use of zip with list unpacking (*) efficiently handles the transposition
        transposed_list = list(map(list, zip(*aggregated_durations)))

        # Storing the result in an instance variable, though consider if this is necessary
        # as the data is also returned by the function. If not used elsewhere, this line can be omitted.
        self.list_cleaned = transposed_list

        return transposed_list

    def get_cmax_virtual(self, prepared_data):
        """
        Calculates the cumulative maximum completion time (cmax) for job sequences on various machines.
        This function organizes jobs into optimal sequences based on their processing times and priorities,
        then computes the cmax for each sequence.

        Args:
            prepared_data (list): List of job data where each element contains tuples of (job_id, first_duration, s
            econd_duration).

        Returns:
            tuple: Contains flattened result of job sequences, job sequences per machine, and list of cmax values for
            each machine.
        """
        warnings.filterwarnings("ignore", category=FutureWarning)
        all_cmax_values, all_job_sequences, overall_job_results = [], [], []

        for jobs in prepared_data:
            # Sort jobs by their first and second durations to prioritize processing
            jobs_sorted_by_first = sorted(jobs, key=lambda x: x[1])
            jobs_sorted_by_second = sorted(jobs, key=lambda x: x[2], reverse=True)

            # Create sequences based on duration comparisons
            sequence_a = [job for job in jobs_sorted_by_first if job[1] <= job[2]]
            sequence_b = [job for job in jobs_sorted_by_second if job[1] > job[2]]

            # Final job sequence is A followed by B
            final_sequence = sequence_a + sequence_b
            job_ids_sequence = [job[0] for job in final_sequence]
            all_job_sequences.extend(job_ids_sequence)

            # Compute start and end times for each job in the final sequence
            start_times, cmax_intervals = [0], []
            for index, job in enumerate(final_sequence):
                start_time = start_times[-1] if index == 0 else start_times[-1] + final_sequence[index - 1][1]
                start_times.append(start_time)
                completion_time = start_time + job[2]
                cmax_intervals.append(completion_time)

            # The last completion time in cmax_intervals is the cmax for this sequence
            all_cmax_values.append(cmax_intervals[-1])
            overall_job_results.extend(job_ids_sequence)
            overall_job_results.append(cmax_intervals[-1])

        job_sequences_per_machine = [
            all_job_sequences[i: i + self.nb_jobs]
            for i in range(0, len(all_job_sequences), self.nb_jobs)
        ]

        return overall_job_results, job_sequences_per_machine, all_cmax_values

    def solve(self, flatten_result):

        global list_data_copy, gant_data, list_list_gant, nb_sec
        warnings.filterwarnings("ignore", category=FutureWarning)
        create_dir(self.output_dir)
        _, story = create_pdf_file()
        nb_sec = JobShopScheduler.nb_sec + 1
        story, nb_sec = add_section_to_pdf(
            story, self.problem_details()[0], self.problem_details()[1], nb_sec
        )
        table = self.prepare_table()
        story = add_table_to_pdf(table, story)
        story = add_section_to_pdf(
            story, "Visualizing Results with Gantt Charts: ", "", nb_sec
        )
        # flatten_result = self.get_cmax_virtual()[0].copy()
        list_data = []
        list_data_copy = []
        gant_data = []
        p = JobShopScheduler.p
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
                print(list_data_copy)
                for idx, i in enumerate(list_data_copy):
                    gant_data.append(self.get_job_durations()[idx])
                # print(gant_data)
                lc = []
                for j in gant_data:
                    for i in range(1, len(gant_data[0]) - 1):
                        lc.append([j[0], j[i], j[i + 1]])

                # print(lc)
                b = len(self.get_job_durations()[0]) - 2
                c = len(list_data_copy)
                lcf = []
                for j in range(0, b):
                    x = b + j
                    for i in range(0, c):
                        lcf.append(lc[x - b])
                        x += b

                cc = lcf[0:c]
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
        Story = add_section_to_pdf(
            Story,
            "Final Scheduling Result:",
            "To conclude, among the results of the subproblems, we retain the following optimal sequence solution :|| "
            "{0} || with a value of Cmax = {1} ".format(
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

    def __str__(self):
        return "Your problem is a Job Shop scheduling of {0} tasks through {1} machines.".format(
            self.nb_jobs, self.nb_machines
        )
