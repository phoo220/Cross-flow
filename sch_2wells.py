import pandas as pd
import os
 
# Read Excel file
excel_file = 'Book_day.xlsx'
df = pd.read_excel(excel_file)
PBHP = 180
IBHP = 250
GCRL = 2
TSTEP = 1
limit = 1000
 
# To delete the existing one
output_file = '2wells/Wind_Daily250.INC'
if os.path.exists(output_file):
    os.remove(output_file)
 
initial_lines = (f"-- Production well controls (all start producing at day 1)\n\n")
 
# Write content to the file
with open(output_file, 'w') as file:
    file.write(initial_lines)
    for day, rate in enumerate(df['rate'], start=1):
        if rate < limit:
            file.write(f"WCONPROD\n\t'PROD'\t'OPEN'\t'BHP'\t1*  1* 1* 1* 1*\t{PBHP}  /\n/\nWCONINJE\n\t'INJ'\tWATER\t'OPEN'\tRATE\t{rate}\t1*\t{IBHP}\t/\n \t'INJX' \t'WAT' \t'OPEN' \tRATE \t0 \t1* \t{IBHP} \t/\n \t'I' \t'WAT' \t'STOP'\tRATE \t{limit} \t1* \t{IBHP}\t/\n/\nWGRUPCON\n\t'INJ'\tYes \t {GCRL} \tRAT \t 1 \t / \n\t'INJX'\tYes \t {GCRL} \tRAT \t 1 \t / \n/ \n \nTSTEP\n {TSTEP} /--{day} \n\n")
        else:
            file.write(f"WCONPROD\n\t'PROD'\t'OPEN'\t'BHP'\t1*  1* 1* 1* 1*\t{PBHP}  /\n/\nWCONINJE\n\t'INJ' \t'WAT' \t'OPEN' \tRATE \t{limit} \t1* \t{IBHP} \t/\n\t'INJX' \t'WAT' \t'OPEN' \tRATE \t{rate-limit} \t1* \t{IBHP} \t/\n\t'I' \t'WAT'\t'STOP'\tRATE \t{limit} \t1* \t{IBHP}\t/\n/\nWGRUPCON\n\t'INJ'\tYes \t {GCRL} \tRAT \t 1 \t / \n\t'INJX'\tYes \t {GCRL} \tRAT \t 1 \t /\n/ \n \nTSTEP\n {TSTEP} /--{day}\n\n")
 
 