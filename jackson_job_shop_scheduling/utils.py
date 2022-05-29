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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors as cl
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
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

    os.makedirs(dir + '/ImagesOutput')
    os.makedirs(dir + '/PdfsOutput')
    os.makedirs(dir + '/TxtsOutput')
    pdf_name = dir + "/PdfsOutput/Algo_Cds_Output.pdf"
    
def func_trait(x, y, h, s):
    S = ""
    j = y
    while j > h:
        j -= 0.5
        S += x * " " + s + "\n"
    return S

def create_pdf_file(story, pdf_name = 'Algo_Cds_Output.pdf'): 

    doc = SimpleDocTemplate(pdf_name, pagesize=letter,
                            rightMargin=15, leftMargin=15,
                            topMargin=15, bottomMargin=20)
    
    Story = []
    tit = "Job Shop Scheduling : N Tasks through M Machines"
    stit = "1.  Background"
    contexte = " A job shop consists of a set of distinct machines that process jobs. \
    Each job is a series of tasks that require use of particular machines for known durations, and which must be completed in specified order. \
    The job shop scheduling problem is to schedule the jobs on the machines to minimize the time necessary to process all jobs (i.e, the makespan) or some other metric of productivity. \
    Job shop scheduling is one of the classic problems in Operations Research. "
    contexte_2 = "Data consists of two tables. The first table is decomposition of the jobs into a series of tasks. \
    ach task lists a job name, name of the required machine, and task duration. \
    The second table list task pairs where the first task must be completed before the second task can be started. \
    This formulation is quite general, but can also specify situations with no feasible solutions."
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size=20 color=red>%s</font>' % tit
    stit = '<font size=15 color=black>%s</font>' % stit
    Story.append(Paragraph(ptext, styles["BodyText"]))
    Story.append(Spacer(5, 30))
    Story.append(Paragraph(stit, styles["BodyText"]))
    Story.append(Spacer(5, 15))
    Story.append(Paragraph(contexte, styles["BodyText"]))
    Story.append(Spacer(5, 10))
    Story.append(Paragraph(contexte_2, styles["BodyText"]))
    doc.build(Story)
    
create_pdf_file('story','Algo_Cds_Output.pdf')