
import os
import sys

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