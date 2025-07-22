""" import sys
from ecl.summary import EclSum
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

# Constants and volume calculation
V = (1000 * 1000 * 40) * 0.3

# Load summary data
tSummaryData1 = EclSum('HYBRID_ENERGY.UNSMRY')
tSummaryData2 = EclSum('WIND_POWERED.UNSMRY')
tSummaryData3 = EclSum('WIND+STORAGE.UNSMRY')

# Time vectors and their differences
def get_time_diff(summary_data):
    time_vector = summary_data.numpy_vector("TIME")
    time_diff = np.diff(time_vector, prepend=time_vector[0])
    return time_vector, time_diff

afTime1, afTime1Diff = get_time_diff(tSummaryData1)
afTime2, afTime2Diff = get_time_diff(tSummaryData2)
afTime3, afTime3Diff = get_time_diff(tSummaryData3)

# Injection rates and pressures
WIR_constantinjection = tSummaryData1.numpy_vector("FWIR")
WIR_periodicinjection = tSummaryData2.numpy_vector("FWIR")
WIR_energystorage = tSummaryData3.numpy_vector("FWIR")

BHP_constantinjection = tSummaryData1.numpy_vector("WBHP:INJ")
BHP_periodicinjection = tSummaryData2.numpy_vector("WBHP:INJ")
BHP_energystorage_out = tSummaryData3.numpy_vector("WBHP:I")
BHP_energystorage_in = tSummaryData3.numpy_vector("WBHP:INJX")
RPR = tSummaryData3.numpy_vector("RPR:2")
Xflow_outflow = tSummaryData3.numpy_vector("CWFR:I:1,1,3")
Xflow_outflow = np.maximum(Xflow_outflow, 0)
Xflow_inflow = tSummaryData3.numpy_vector("WWIR:INJX")
FOPR_constantinjection = tSummaryData1.numpy_vector("FOPR")
FOPR_periodicinjection = tSummaryData2.numpy_vector("FOPR")
FOPR_energystorage = tSummaryData3.numpy_vector("FOPR")
FOPT_constantinjection = tSummaryData1.numpy_vector("FOPT")
FOPT_periodicinjection = tSummaryData2.numpy_vector("FOPT")
FOPT_energystorage = tSummaryData3.numpy_vector("FOPT")

# Energy consumption calculations
def calculate_energy_consumption(WIR, BHP, time_diff):
    EC = ((WIR / 86400) * (BHP * 100000)) / 1000000
    ECT = np.cumsum(EC * time_diff)
    return EC, ECT

EC_constantinjection, ECT_constantinjection = calculate_energy_consumption(WIR_constantinjection, BHP_constantinjection, afTime1Diff)
EC_periodicinjection, ECT_periodicinjection = calculate_energy_consumption(WIR_periodicinjection, BHP_periodicinjection, afTime2Diff)
EC_energystorage, ECT_energystorage = calculate_energy_consumption(WIR_energystorage, BHP_energystorage_in, afTime3Diff)

# Energy consumption per oil produced
def calculate_energy_per_oil(ECT, FOPT):
    return ECT * 1000 / FOPT

ECT_oil_CI = calculate_energy_per_oil(ECT_constantinjection, FOPT_constantinjection)
ECT_oil_PI = calculate_energy_per_oil(ECT_periodicinjection, FOPT_periodicinjection)
ECT_oil_ES = calculate_energy_per_oil(ECT_energystorage, FOPT_energystorage)

# Energy flow calculations for storage layer
def calculate_xflow_energy(Xflow, RPR, time_diff):
    EC_Xflow = (((Xflow / 86400) * (RPR * 100000)) / 1000000)
    ECT_Xflow = np.cumsum(EC_Xflow * time_diff)
    return ECT_Xflow
ECT_Xflow_in= calculate_xflow_energy(Xflow_inflow, RPR, afTime3Diff)
ECT_Xflow_out = calculate_xflow_energy(Xflow_outflow, RPR, afTime3Diff)
deltaE = []
for i in range(len(RPR)):
    if i == 0:
        delta = (RPR[i]**2 - RPR[i]**2)*(V/2)*4.84E-5
    else:
        delta = (RPR[i]**2 - RPR[i-1]**2)*(V/2)*4.84E-5
    deltaE.append(delta)
deltaE = np.array(deltaE)
#ECT_Xflow_out = np.maximum(ECT_Xflow_out, 0)
print(ECT_Xflow_in)

# Efficiency calculation
efficiency = (ECT_Xflow_out / (ECT_Xflow_in - deltaE)) * 100

# Plotting functions
def set_plot_params(ax):
    ax.tick_params(axis='both', length=5.0, width=1.5)
    ax.tick_params(axis='both', which='minor', length=3.0, width=1.0)
    ax.grid(True)

# Total Energy Consumption
plt.plot(afTime1,ECT_constantinjection,color='blue',label=r'HYBRID ENERGY')
plt.plot(afTime2,ECT_periodicinjection,color='orange',linestyle='dashed', label=r'WIND POWERED')
plt.plot(afTime3,ECT_energystorage,color='green',label=r'WIND & STORAGE')
plt.xlabel('Time [days]')
plt.ylabel('Energy [MWh]')
plt.legend()
plt.savefig('TotalConsumption.pdf',bbox_inches='tight')
plt.show()
plt.clf()


## Total Energy Consumption per Oil Produced
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,ECT_oil_CI,color='black', label=r'HYBRID ENERGY')
plt.plot(afTime2,ECT_oil_PI,color='black',linestyle='dashed',label=r'WIND POWERED')
plt.plot(afTime3,ECT_oil_ES,color='green',label=r'WIND & STORAGE')
plt.xlabel('Time [days]')
plt.ylabel('Energy [kWh/sm3]')
plt.legend()
plt.savefig('TotalConsumptionPerOil.pdf',bbox_inches='tight')
plt.clf()

## Energy In and Out of Storage Layer
fig, ax1 = plt.subplots(figsize=(8,4))
set_plot_params(ax1)
ax1.plot(afTime3, ECT_Xflow_in, label='Energy injected into storage layer', color='black')
ax1.plot(afTime3, ECT_Xflow_out, label='Energy discharged from storage layer', linestyle='dashed', color='black')
ax1.set_xlabel('Time [days]')
ax1.set_ylabel('Energy [MWh]', color='black')
ax1.tick_params('y')
ax1.set_ylim(0, 100)
ax2 = ax1.twinx()
ax2.plot(afTime3, RPR, label='BHP of storage layer', linestyle='dashed', color='orange')
ax2.set_ylabel('Bottom Hole Pressure (bar)')
ax2.set_xlabel('Time [days]')
ax2.tick_params('y', colors='black')
ax2.set_ylim(200, 240)
lines_1, labels_1 = ax2.get_legend_handles_labels()
lines_2, labels_2 = ax1.get_legend_handles_labels()
ax1.legend(lines_2 + lines_1, labels_2 + labels_1, loc='upper left')
plt.savefig('EnergyIn&Out.pdf', bbox_inches='tight')
plt.clf()

# Efficiency of Storage Layer
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime3,efficiency, label=r'Efficiency of the storage layer')
plt.axhline(y=100, color='black', linestyle='--', label='100% Efficiency')
plt.xlabel('Time [days]')
plt.ylabel('Percentage [%]')
plt.legend()
plt.savefig('EfficiencyOfStorage.pdf',bbox_inches='tight')
plt.clf()


## Cross Flow Rate
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime3,Xflow_outflow,color='black',linestyle='dashed', label=r'Outflow rate')
plt.plot(afTime3,Xflow_inflow,color ='black',label=r'Inflow rate')
plt.xlabel('Time [days]')
plt.ylabel('Flow rate [sm3/day]')
plt.legend()
plt.savefig('XflowRate.pdf',bbox_inches='tight')
plt.clf()

# Wind Power Data
excel_file = '../Book_day.xlsx'
df = pd.read_excel(excel_file)
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(df['Day'], df['Normalized average power'], color='steelblue', label=r'Daily Wind Power')
plt.xlabel('Time [days]')
plt.ylabel('Normalized average wind power')
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend()
plt.savefig('windpower.pdf',bbox_inches='tight')
plt.clf()
 """
 
import sys
from ecl.summary import EclSum
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

tSummaryData3 = EclSum('WIND+STORAGE.UNSMRY')
def numpy_vector(identifier):
        parts = identifier.split(':')[1].split(',')
        return np.array([int(parts[0]), int(parts[1]), int(parts[2])]) 

# Retrieve each set of values
P = []
for i in range(1, 11):
    for j in range(1, 11):
        identifier = f"BPR:{i},{j},3"
        P.append(tSummaryData3.numpy_vector(identifier))

V = 100*100*40*0.3
ct = 4.67e-5 + 4.84e-5

total_deltaE = []
for i in range(len(P)):
    for j in range(i + 1, len(P)):
        deltaE = ((P[i]** 2 - P[j]** 2)  * (V / 2) * ct/36).sum()
        total_deltaE.append(deltaE)

total_deltaE
print(total_deltaE)
