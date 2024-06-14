import sys
from ecl.summary import EclSum
from ecl.eclfile import EclFile
from ecl.grid import EclGrid
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

#tInit = EclFile('WIND+STORAGE'+'.INIT')
#print(tInit.keys())
V = (1000*1000*40)*0.3
Vb =(100*100*40)*0.3
ct = 4.67e-5 + 4.84e-5
tSummaryData1=EclSum('HYBRID_ENERGY'+'.UNSMRY')
tSummaryData2=EclSum('WIND_POWERED'+'.UNSMRY')
tSummaryData3=EclSum('WIND+STORAGE'+'.UNSMRY')
tSumData3=EclFile('WIND+STORAGE'+'.UNRST')
#BlockP = tSumData3.numpy_vector('PRESSURE')
#print(BlockP)
#print(tSumData3.keys())

afTime1=tSummaryData1.numpy_vector("TIME")
afTime1Diff=afTime1[1:]-afTime1[:-1]
afTime1Diff=np.insert(afTime1Diff,0,afTime1[0])

afTime2=tSummaryData2.numpy_vector("TIME")
afTime2Diff=afTime2[1:]-afTime2[:-1]
afTime2Diff=np.insert(afTime2Diff,0,afTime2[0])

afTime3=tSummaryData3.numpy_vector("TIME")
afTime3Diff=afTime3[1:]-afTime3[:-1]
afTime3Diff=np.insert(afTime3Diff,0,afTime3[0])
#print(afTime1Diff)
#print(afTimes)
#print(tSummaryData3.keys())
#injection rates
WIR_constantinjection = tSummaryData1.numpy_vector("FWIR")
WIR_periodicinjection = tSummaryData2.numpy_vector("FWIR")
WIR_energystorage = tSummaryData3.numpy_vector("FWIR")

BHP_constantinjection = tSummaryData1.numpy_vector("WBHP:INJ")
BHP_periodicinjection = tSummaryData2.numpy_vector("WBHP:INJ")
BHP_energystorage_out = tSummaryData3.numpy_vector("WBHP:I")
BHP_energystorage_in = tSummaryData3.numpy_vector("WBHP:INJX")
RPR = tSummaryData3.numpy_vector("RPR:2")
Xflow_outflow = np.maximum(tSummaryData3.numpy_vector("CWFR:I:1,1,3"),0)
Xflow_inflow = tSummaryData3.numpy_vector("WWIR:INJX")
FOPR_constantinjection = tSummaryData1.numpy_vector("FOPR")
FOPR_periodicinjection = tSummaryData2.numpy_vector("FOPR")
FOPR_energystorage = tSummaryData3.numpy_vector("FOPR")
FOPT_constantinjection = tSummaryData1.numpy_vector("FOPT")
FOPT_periodicinjection = tSummaryData2.numpy_vector("FOPT")
FOPT_energystorage = tSummaryData3.numpy_vector("FOPT")

# Consumption for each case
EC_constantinjection = (WIR_constantinjection*BHP_constantinjection*afTime1Diff/36) #kwh
ECT_constantinjection = np.cumsum(EC_constantinjection)
EC_periodicinjection = (WIR_periodicinjection*BHP_periodicinjection*afTime2Diff/36) #kwh
ECT_periodicinjection = np.cumsum(EC_periodicinjection)
EC_energystorage = (((WIR_energystorage/86400)*(BHP_energystorage_in*100000))/1000)*afTime3Diff*24 #kwh
ECT_energystorage = np.cumsum(EC_energystorage) 

# Consumption per oil produced
ECT_oil_CI = ECT_constantinjection / FOPT_constantinjection # kwh/m3
ECT_oil_PI = ECT_periodicinjection / FOPT_periodicinjection #kwh/m3
ECT_oil_ES = ECT_energystorage / FOPT_energystorage #kwh/m3

# Bottom layer 
#EC_Xflow_in = (((Xflow_inflow/86400)*(RPR*100000))/1000)*afTime3Diff*24 #kwh
EC_Xflow_in = (BHP_energystorage_in*Xflow_inflow*afTime3Diff/36)
ECT_Xflow_in = np.cumsum(EC_Xflow_in)
EC_Xflow_out = (BHP_energystorage_out*Xflow_outflow*afTime3Diff/36) # kwh
ECT_Xflow_out = np.cumsum(EC_Xflow_out)
#print(afTime3Diff[0:3])
#print(RPR[0:3])
deltaT = []
X =[]
for i in range(len(RPR)):
    if i == 0:
        delta = ((RPR[i]- RPR[i])**2*(V/2)*(4.67E-5+4.84E-5)/36)
        xi = RPR[i] - RPR[i]
    else:
        delta = ((RPR[i]**2 - RPR[i-1]**2)*(V/2)*(4.67E-5+4.84E-5)/36) #+(V*(RPR[i] - RPR[i-1]))/36)
        #delta = (100*(RPR[i]**2 - RPR[i-1]**2)*(V/2)*(4.67E-5+4.84E-5))/(afTime3Diff*3600) #+(V*(RPR[i] - RPR[i-1]))/36)
        xi = RPR[i] - RPR[i-1]
    deltaT.append(delta)
    X.append(xi)
deltaT = np.array(deltaT) #kwh

tSummaryData3 = EclSum('WIND+STORAGE.UNSMRY')
def numpy_vector(identifier):
        parts = identifier.split(':')[1].split(',')
        return np.array([int(parts[0]), int(parts[1]), int(parts[2])]) 


P = []
for i in range(1, 10):
    for j in range(1, 10):
        identifier = f"BPR:{i},{j},3"
        P.append(tSummaryData3.numpy_vector(identifier))
#print(len(P))
total_deltaE = np.zeros(1096)
for j in range(1,len(P[0])):
    deltaE = 0 
    for i in range(0,len(P)):
        deltaE += (Vb*ct/2)*(P[i][j]** 2 - P[i][j-1]** 2)/36 
    total_deltaE[j] = deltaE
deltaET =np.cumsum(total_deltaE)
""" print(i)
    print(P[i])
    print(P[i][2]) """
    #print(deltaE)
        
#print(total_deltaE)
#print(len(total_deltaE))
#print(len(deltaE))


#print(EC_Xflow_out)
plt.plot(afTime3,EC_Xflow_in,color='red')
plt.plot(afTime3,EC_Xflow_out,color='blue')
plt.plot(afTime3,total_deltaE,color='orange')
#plt.plot(afTime3,deltaT,color='black')
plt.xlabel('Time [days]')
plt.ylabel('Energy [kWh]')
#plt.legend()
plt.show()

E_p = (ECT_Xflow_out/ (ECT_Xflow_in))*100
efficiency = ((ECT_Xflow_out)/ (ECT_Xflow_in-deltaT))*100

def set_plot_params(ax):
    ax.tick_params(axis='both', length=5.0, width=1.5)
    ax.tick_params(axis='both', which='minor', length=3.0, width=1.0)
    ax.grid(True)

fig, ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)

#Total Consumption
plt.plot(afTime1,ECT_constantinjection,color='black',label=r'HYBRID ENERGY')
plt.plot(afTime2,ECT_periodicinjection,color='black',linestyle='dashed', label=r'WIND POWERED')
plt.plot(afTime3,ECT_energystorage,color='green',label=r'WIND & STORAGE')
plt.title('Total Energy Consumption During Water Injection')
plt.xlabel('Time [days]')
plt.ylabel('Energy [kWh]')
plt.legend()
plt.savefig('TotalConsumption.pdf',bbox_inches='tight')
plt.clf()

# Total Consumption per oil
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,ECT_oil_CI,color='tab:blue', label=r'HYBRID ENERGY')
plt.plot(afTime2,ECT_oil_PI,color='orange',label=r'WIND POWERED')
plt.plot(afTime3,ECT_oil_ES,color='green',label=r'WIND+STORAGE')
#plt.title('Total Energy Consumption Per Produced Oil')
plt.xlabel('Time [days]')
plt.ylabel('Energy [kWh/sm3]')
plt.legend()
plt.savefig('TotalConsumptionPerOil.pdf',bbox_inches='tight')
plt.clf()

#Efficiency of storage layer
fig,ax1 = plt.subplots(figsize=(8,4))
set_plot_params(ax1)
ax1.plot(afTime3, ECT_Xflow_in, color='black', label='Total energy injected into storage layer',zorder=10)
ax1.plot(afTime3, ECT_Xflow_out, color='black', linestyle='dashed', label='Total energy discharged from storage layer',zorder=10)
ax1.set_ylabel('Energy [kWh]', color='black')
ax1.set_xlabel('Time [days]')
ax1.tick_params('y')
#ax1.set_ylim(0, 100)

ax2 = ax1.twinx()
ax2.plot(afTime3, RPR, color='orange', linestyle = 'dashed', label='BHP of storage layer',zorder=0)
ax2.set_ylabel('Bottom Hole Pressure (bar)')
ax2.set_xlabel('Time [days]')
ax2.tick_params('y', colors='black')
ax2.set_ylim(200,240)
lines_1, labels_1 = ax2.get_legend_handles_labels()
lines_2, labels_2 = ax1.get_legend_handles_labels()
ax1.legend(lines_2+lines_1, labels_2+labels_1, loc='upper left')
plt.savefig('EnergyIn&Out.pdf',bbox_inches='tight')
plt.clf()

##########################

##########################

#Efficiency of storage layer
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime3,E_p, label=r'Apparent Efficiency', color='black', zorder= 1)
plt.plot(afTime3,efficiency, label=r'Efficiency of the storage layer', zorder=0)
plt.axhline(y=100, color='black', linestyle='--', label='100% Efficiency')
#plt.title('Efficiency of the storage layer over time')
plt.xlabel('Time [days]')
plt.ylabel('Percentage [%]')
plt.legend()
plt.savefig('EfficiencyOfStorage.pdf',bbox_inches='tight')
plt.show()
plt.clf()

#Consumption per day
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,EC_constantinjection,label=r'HYBRID ENERGY')
plt.plot(afTime2,EC_periodicinjection,label=r'WIND POWERED')
#plt.title('Energy Consumption During Water Injection')
plt.xlabel('Time [days]')
plt.ylabel('Energy [kWh]')
plt.legend()
plt.savefig('ConsumptionPerDayPI.pdf',bbox_inches='tight')
plt.clf()

#Consumption per day
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,EC_constantinjection,label=r'HYBRID ENERGY')
plt.plot(afTime3,EC_energystorage,label=r'WIND & STORAGE')
#plt.title('Energy Consumption During Water Injection')
plt.xlabel('Time [days]')
plt.ylabel('Energy [kWh]')
plt.legend()
plt.savefig('ConsumptionPerDayES.pdf',bbox_inches='tight')
plt.clf()

#cross flow rate
Xflow_inflow_neg = -1 * Xflow_inflow
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime3,Xflow_outflow,color='black',linestyle='dashed', label=r'Outflow rate')
plt.plot(afTime3,Xflow_inflow_neg,color ='black',label=r'Inflow rate')
plt.xlabel('Time [days]')
plt.ylabel('Flow rate [sm3/day]')
plt.legend()
plt.savefig('XflowRate.pdf',bbox_inches='tight')
plt.clf()

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
