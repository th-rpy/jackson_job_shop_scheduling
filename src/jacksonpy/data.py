import csv
import json
import os


class Data:

    """
    Class to store the data of the job shop scheduling problem

    Args:
        path: path to the data file if you want to use a text/Json/Csv file to store data

    Returns:
        durations_flatten: list of durations
        durations_sorted_int: list of lists of integers: 2d-array of durations

    Examples:
        >>> d = Data("data.txt") # data.json or data.csv
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
        self.path = path
        self._job_durations = None

    def read_json(self):
        with open(self.path) as f:
            data = json.load(f)
        return [[k + 1] + list(map(int, v[1])) for k, v in enumerate(data.items())]

    def read_csv_or_txt(self):
        with open(self.path, "r") as file:
            if self.path.endswith('.csv'):
                reader = csv.reader(file)
            else:
                reader = (line.split() for line in file)
            return sorted([[int(j) for j in i] for i in reader], key=lambda x: x[0])

    def get_job_durations(self):
        if self._job_durations is not None:
            return self._job_durations
        extension = os.path.splitext(self.path)[1]
        if extension == ".json":
            self._job_durations = self.read_json()
        elif extension in [".csv", ".txt"]:
            self._job_durations = self.read_csv_or_txt()
        else:
            raise ValueError("Unsupported file extension.")
        return self._job_durations

    def get_jobs_nb(self):
        return len(self.get_job_durations())

    def get_machines_nb(self):
        return len(self.get_job_durations()[0]) - 1

    def __str__(self):
        durations = self.get_job_durations()
        header = ["Job i"] + [f"dur J/M{i}" for i in range(1, len(durations[0]))]
        data = [header] + [list(map(str, job)) for job in durations]
        description = f"Job Shop scheduling with {self.get_jobs_nb()} jobs and {self.get_machines_nb()} machines. \nThe durations data:\n"
        return description + "\n".join("\t".join(line) for line in data)
