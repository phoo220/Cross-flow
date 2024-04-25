import pandas as pd
import os
 
# Read Excel file
excel_file = 'Book_day.xlsx'
df = pd.read_excel(excel_file)
PBHP = 180
IBHP = 260
TSTEP = 1
limit = 1000
 
# To delete the existing one
output_file = 'Wind_Daily.INC'
if os.path.exists(output_file):
    os.remove(output_file)
 
initial_lines = (f"-- Production well controls (all start producing at day 1)\n\n")
 
# Write content to the file
with open(output_file, 'w') as file:
    file.write(initial_lines)
    for day, rate in enumerate(df['rate'], start=1):
        file.write(f"WCONPROD\n\t'PROD'\t'OPEN'\t'BHP'\t1500  1* 1* 1* 1*\t{PBHP}  /\n/\nWCONINJE\n\t'INJ'\tWATER\t'OPEN'\tRATE\t{rate}\t1*\t{IBHP}\t/\n/\nTSTEP\n {TSTEP} /--{day} \n\n")
 