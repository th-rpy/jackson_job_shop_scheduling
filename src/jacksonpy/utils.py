import os
import shutil
from random import randrange
import numpy as np
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


def gant_list(C):
    db1, db2 = [], []

    db1.append([0, C[0][1]])
    for i in range(1, len(C)):
        db1.append([db1[i - 1][1], db1[i - 1][1] + C[i][1]])
    db2.append([db1[0][1], db1[0][1] + C[0][2]])
    for i in range(1, len(db1)):
        if db1[i][1] >= db2[i - 1][1]:
            db2.append([db1[i][1], db1[i][1] + C[i][2]])
        else:
            db2.append([db2[i - 1][1], db2[i - 1][1] + C[i][2]])
    return db1, db2


def create_dir(path):
    dir = path
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

    os.makedirs(dir + "/ImagesOutput")
    # os.makedirs(dir + '/PdfsOutput')
    os.makedirs(dir + "/TxtsOutput")
    pdf_name = dir + "/PdfsOutput/Algo_Cds_Output.pdf"


def func_trait(x, y, h, s):
    S = ""
    j = y
    while j > h:
        j -= 0.5
        S += x * " " + s + "\n"
    return S


def create_pdf_file(pdf_name="output/Algo_Cds_Output.pdf"):

    doc = SimpleDocTemplate(
        pdf_name,
        pagesize=letter,
        rightMargin=15,
        leftMargin=15,
        topMargin=15,
        bottomMargin=20,
    )

    Story = []
    tit = "Job Shop Scheduling : N Tasks through M Machines"
    stit = "1.  Background"
    contexte = " A job shop consists of a set of distinct machines that process jobs. \
    Each job is a series of tasks that require use of particular machines for known durations, and which must be completed in specified order. \
    The job shop scheduling problem is to schedule the jobs on the machines to minimize the time necessary to process all jobs (i.e, the makespan) or some other metric of productivity. \
    Job shop scheduling is one of the classic problems in Operations Research. "
    contexte_2 = "Data consists of duration table.\
    Each task lists a job name, name of the required machine, and task duration. \
    This formulation is quite general, but can also specify situations with no feasible solutions."
    contexte_3 = " The minimization of Cmax in the general flow-shop case is an NP-hard problem in the strong sense (see Garey et al). \n Several heuristics have been proposed to solve it, and in particular the one of Campell Dudek and Smith (CDS) and the one of Nawaz, Enscore and Ham (NEH).\
    Each of these heuristics gives good results, but none of them guarantees the optimal solution.\
    Often, we will complement these algorithms with a 2-opt or a 3-opt."

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    ptext = "<font size=20 color=red>%s</font>" % tit
    stit = "<font size=15 color=black>%s</font>" % stit
    Story.append(Paragraph(ptext, styles["BodyText"]))
    Story.append(Spacer(5, 30))
    Story.append(Paragraph(stit, styles["BodyText"]))
    Story.append(Spacer(5, 15))
    Story.append(Paragraph(contexte, styles["BodyText"]))
    Story.append(Spacer(5, 10))
    Story.append(Paragraph(contexte_2, styles["BodyText"]))
    Story.append(Spacer(5, 10))
    Story.append(Paragraph(contexte_3, styles["BodyText"]))
    Story.append(Spacer(5, 15))
    ptext = "<font size=15 color = black>2.   Notation:</font>"
    Story.append(Paragraph(ptext, styles["BodyText"]))
    Story.append(Spacer(5, 15))
    ptext = "n: number of jobs. \nm: number of machines. \npij: processing time of job i on machine j"
    ptext = ptext.replace(" ", "&nbsp;")
    ptext = ptext.replace("\n", "<br />")
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 15))
    ptext = (
        "Example: n = 5 Tasks through m = 4 Machines. Above the duration table (pij) :"
    )
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 20))
    data = [
        ("Job / Machine", "M 1", "M 2", "M 3", "M4"),
        ("J 1", "5", "4", "7", "2"),
        ("J 2", "7", "8", "3", "4"),
        ("J 3", "6", "3", "4", "9"),
        ("J 4", "4", "6", "7", "6"),
        ("J 5", "9", "1", "2", "5"),
    ]
    Story = add_table_to_pdf(data, Story)
    # doc.build(Story)
    return doc, Story


def add_table_to_pdf(data, Story):
    table = Table(
        data,
        [0.9 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch],
        (len(data)) * [0.5 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("ALIGN", (2, 1), (2, -1), "LEFT"),
                ("FONT", (0, 0), (-1, 0), "Times-Bold"),
                ("BOX", (0, 0), (-1, -1), 0.25, "black"),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, "black"),
            ]
        )
    )
    Story.append(table)
    Story.append(Spacer(1, 15))
    return Story