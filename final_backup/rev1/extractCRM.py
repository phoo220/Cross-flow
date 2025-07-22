import os
from ecl.summary import EclSum
import numpy as np
from datetime import date, datetime, timedelta
import sys
import csv


filename = "BASECASE_MODIFIED_NORNE"
if os.path.exists(filename+'.csv'):
   os.remove(filename+'.csv')
strModelName=filename
tSummaryData=EclSum(strModelName+'.UNSMRY')
# print(tSummaryData.keys())
afTime=tSummaryData.numpy_vector("TIME")
year = '2023'
strt_date = date(int(year),1,1)
afTimeD = [strt_date + timedelta(days=diff -1) for diff in afTime]
afTimeNP = np.array(afTimeD, dtype='datetime64[s]')
wopr_data = {
     #"B-1H": tSummaryData.numpy_vector("WOPR:B-1H"),
     #"B-2H": tSummaryData.numpy_vector("WOPR:B-2H"),
     #"B-3H": tSummaryData.numpy_vector("WOPR:B-3H"),
     #"B-4BH": tSummaryData.numpy_vector("WOPR:B-4BH"),
     "D-1CH": tSummaryData.numpy_vector("WOPR:D-1CH"),
     "D-2H": tSummaryData.numpy_vector("WOPR:D-2H"),
     "D-3AH": tSummaryData.numpy_vector("WOPR:D-3AH"),
     "D-4H": tSummaryData.numpy_vector("WOPR:D-4H"),
     #"E-1H": tSummaryData.numpy_vector("WOPR:E-1H"),
     #"E-2H": tSummaryData.numpy_vector("WOPR:E-2H"),
     #"E-3H": tSummaryData.numpy_vector("WOPR:E-3H")
 }
wwir_data = {
     "C-1H": tSummaryData.numpy_vector("WWIR:C-1H"),
     "C-2H": tSummaryData.numpy_vector("WWIR:C-2H"),
     "C-3H": tSummaryData.numpy_vector("WWIR:C-3H"),
     "C-4H": tSummaryData.numpy_vector("WWIR:C-4H"),
     #"F-1H": tSummaryData.numpy_vector("WWIR:F-1H"),
     #"F-2H": tSummaryData.numpy_vector("WWIR:F-2H"),
     #"F-3H": tSummaryData.numpy_vector("WWIR:F-3H")
 }
wbhp_data = {
     "C-1H": tSummaryData.numpy_vector("WBHP:C-1H"),
     "C-2H": tSummaryData.numpy_vector("WBHP:C-2H"),
     "C-3H": tSummaryData.numpy_vector("WBHP:C-3H"),
     "C-4H": tSummaryData.numpy_vector("WBHP:C-4H"),
     #"F-1H": tSummaryData.numpy_vector("WBHP:F-1H"),
     #"F-2H": tSummaryData.numpy_vector("WBHP:F-2H"),
     #"F-3H": tSummaryData.numpy_vector("WBHP:F-3H")
     #"B-1H": tSummaryData.numpy_vector("WBHP:B-1H"),
     #"B-2H": tSummaryData.numpy_vector("WBHP:B-2H"),
     #"B-3H": tSummaryData.numpy_vector("WBHP:B-3H"),
     #"B-4BH": tSummaryData.numpy_vector("WBHP:B-4BH"),
     "D-1CH": tSummaryData.numpy_vector("WBHP:D-1CH"),
     "D-2H": tSummaryData.numpy_vector("WBHP:D-2H"),
     "D-3AH": tSummaryData.numpy_vector("WBHP:D-3AH"),
     "D-4H": tSummaryData.numpy_vector("WBHP:D-4H"),
     #"E-1H": tSummaryData.numpy_vector("WBHP:E-1H"),
     #"E-2H": tSummaryData.numpy_vector("WBHP:E-2H"),
     #"E-3H": tSummaryData.numpy_vector("WBHP:E-3H"),
 }

def write_csv(file_name, data):
     with open(file_name, 'w', newline='') as csvfile:
         writer = csv.writer(csvfile)
         #writer.writerow(["Time"] + list(data.keys()))  # Header row
         for i, time in enumerate(afTime):
             writer.writerow([data[key][i] for key in data.keys()])
 
write_csv("../CRM/production_norne.csv", wopr_data)
write_csv("../CRM/injection_norne.csv", wwir_data)
write_csv("../CRM/pressure_norne.csv", wbhp_data)
# Write time data to times.csv
with open("../CRM/time_norne.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time"])
    for time in afTime:
        writer.writerow([time])
