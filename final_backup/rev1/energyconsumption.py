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
tSummaryData4=EclSum('WIND+STORAGE_50MD'+'.UNSMRY')

afTime1=tSummaryData1.numpy_vector("TIME")
afTime1Diff=afTime1[1:]-afTime1[:-1]
afTime1Diff=np.insert(afTime1Diff,0,afTime1[0])

afTime2=tSummaryData2.numpy_vector("TIME")
afTime2Diff=afTime2[1:]-afTime2[:-1]
afTime2Diff=np.insert(afTime2Diff,0,afTime2[0])

afTime3=tSummaryData3.numpy_vector("TIME")
afTime3Diff=afTime3[1:]-afTime3[:-1]
afTime3Diff=np.insert(afTime3Diff,0,afTime3[0])

afTime4=tSummaryData4.numpy_vector("TIME")
afTime4Diff=afTime4[1:]-afTime4[:-1]
afTime4Diff=np.insert(afTime4Diff,0,afTime4[0])

WIR_constantinjection = tSummaryData1.numpy_vector("FWIR")
WIR_periodicinjection = tSummaryData2.numpy_vector("FWIR")
WIR_energystorage = tSummaryData3.numpy_vector("FWIR")

WIT_constantinjection = tSummaryData1.numpy_vector("FWIT")
WIT_periodicinjection = tSummaryData2.numpy_vector("FWIT")
WIT_energystorage = tSummaryData3.numpy_vector("FWIT")

BHP_constantinjection = tSummaryData1.numpy_vector("WBHP:INJ")
BHP_periodicinjection = tSummaryData2.numpy_vector("WBHP:INJ")
BHP_energystorage_out = tSummaryData3.numpy_vector("WBHP:I")
BHP_energystorage = tSummaryData3.numpy_vector("WBHP:INJ")
BHP_energystorage_out_50md = tSummaryData4.numpy_vector("WBHP:I")
BHP_energystorage_in = tSummaryData3.numpy_vector("WBHP:INJX")
BHP_energystorage_in_50md = tSummaryData4.numpy_vector("WBHP:INJX")
# BHP_energystorage_out = tSummaryData3.numpy_vector("CPR:INJX:1,1,3")
# BHP_energystorage_in = tSummaryData3.numpy_vector("CPR:INJX:1,1,3")
RPR = tSummaryData3.numpy_vector("RPR:2")
# Xflow = tSummaryData3.numpy_vector("CWFR:I:1,1,3")
XWrongWay = np.minimum(tSummaryData3.numpy_vector("CWFR:I:1,1,3"),0)
# print('all -', Xflow[0:20])
# print('below zero-', (XWrongWay[0:20]))
Xflow_inflow = tSummaryData3.numpy_vector("WWIR:INJX")
Xflow_inflow_50md = tSummaryData4.numpy_vector("WWIR:INJX")
Xflow_outflow = np.maximum(tSummaryData3.numpy_vector("CWFR:I:1,1,3"),0)
Xflow_outflow_50md = np.maximum(tSummaryData4.numpy_vector("CWFR:I:1,1,3"),0)
# Xflow_outflow[:6] = 0
# plt.plot(afTime3,Xflow_inflow, color='blue', label= 'inflow')
# plt.plot(afTime3,Xflow_outflow, color='red', label= 'outflow')
# plt.plot(afTime3,abs(XWrongWay), color='orange', label= 'wrongway')
# plt.legend()
# # plt.show()

# print('below zero-', Xflow_outflow[0:20])

FOPR_constantinjection = tSummaryData1.numpy_vector("FOPR")
FOPR_periodicinjection = tSummaryData2.numpy_vector("FOPR")
FOPR_energystorage = tSummaryData3.numpy_vector("FOPR")
FOPT_constantinjection = tSummaryData1.numpy_vector("FOPT")
FOPT_periodicinjection = tSummaryData2.numpy_vector("FOPT")
FOPT_energystorage = tSummaryData3.numpy_vector("FOPT")

GPR_constantinjection = tSummaryData1.numpy_vector("WGPR:PROD")
GPR_periodicinjection = tSummaryData2.numpy_vector("WGPR:PROD")
GPR_energystorage = tSummaryData3.numpy_vector("WGPR:PROD")
GPT_constantinjection = tSummaryData1.numpy_vector("WGPT:PROD")
GPT_periodicinjection = tSummaryData2.numpy_vector("WGPT:PROD")
GPT_energystorage = tSummaryData3.numpy_vector("WGPT:PROD")
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
EC_Xflow_inject = (BHP_energystorage_in*Xflow_inflow*afTime3Diff/36)
EC_Xflow_inject_50md = (BHP_energystorage_in_50md*Xflow_inflow_50md*afTime4Diff/36)
EC_wrongway = -(BHP_energystorage_out*XWrongWay*afTime3Diff/36)
EC_Xflow_in = EC_Xflow_inject #+EC_wrongway
EC_Xflow_in_50md = EC_Xflow_inject_50md
ECT_Xflow_in = np.cumsum(EC_Xflow_in)
ECT_Xflow_in_50md = np.cumsum(EC_Xflow_in_50md)
EC_Xflow_out = (BHP_energystorage_out*Xflow_outflow*afTime3Diff/36) # kwh
EC_Xflow_out_50md = (BHP_energystorage_out_50md*Xflow_outflow_50md*afTime4Diff/36) # kwh
ECT_Xflow_out = np.cumsum(EC_Xflow_out)
ECT_Xflow_out_50md = np.cumsum(EC_Xflow_out_50md)


def numpy_vector(identifier):
        parts = identifier.split(':')[1].split(',')
        return np.array([int(parts[0]), int(parts[1]), int(parts[2])]) 

P = []
for i in range(1, 11):
    for j in range(1, 11):
        identifier = f"BPR:{i},{j},3"
        P.append(tSummaryData3.numpy_vector(identifier))
# print(P[0])
# print(P[0][1])
# print(P[0][0])
#print(len(P))
total_deltaE = np.zeros_like(ECT_Xflow_in)
total_E = np.zeros_like(ECT_Xflow_in)
for j in range(0,len(P[0])):
    E = 0 
    for i in range(0,len(P)):
        # print(P[i][j])
        E += (Vb*ct/2)*(P[i][j]** 2 )/36
        #print(deltaE) 
    total_E[j] = E
# print('deltaET',total_E[0:5])
# deltaET =np.cumsum(total_deltaE)
#print(np.shape(P))
#for j in range(1,len(P[0])):
for j in range(1,np.shape(P)[1]):
    deltaE = 0 
#    for i in range(0,len(P)):
    for i in range(0,np.shape(P)[0]):
        # print(P[i][j])
        deltaE += (Vb*ct/2)*(P[i][j]**2 - P[i][j-1]**2)/36
    total_deltaE[j] = deltaE
#print('deltaE',total_deltaE[0:8]) 
# deltaET =total_deltaE
deltaET =np.cumsum(total_deltaE) #just just at 12:19 1st july
""" print(i)
    print(P[i])
    print(P[i][2]) """
    #print(deltaE)
    

E_p = (ECT_Xflow_out/ (ECT_Xflow_in))*100
E_p_50md = (ECT_Xflow_out_50md/ (ECT_Xflow_in_50md))*100
efficiency = ((ECT_Xflow_out+deltaET)/ (ECT_Xflow_in))*100   # 1st july
# efficiency = ((ECT_Xflow_out)/ (ECT_Xflow_in+deltaET))*100  
# efficiency = ((ECT_Xflow_out-deltaET)/ (ECT_Xflow_in))*100

def set_plot_params(ax):
    ax.tick_params(axis='both', length=5.0, width=1.5,labelsize=14)
    ax.tick_params(axis='both', which='minor', length=3.0, width=1.0)
    ax.grid(False)

# fig, ax = plt.subplots(figsize=(8,4))
# set_plot_params(ax)

# plt.plot(afTime3,total_E-total_E[0], label='current E', color ='black')       #1st july
# plt.plot(afTime3,deltaET, label='total ', color ='red')
# # plt.show()

fig, ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)

# plt.scatter(afTime3,EC_Xflow_in, label='Inj', color ='black')
# plt.scatter(afTime3,total_deltaE, label='deltaE ', color ='red')
# # plt.show()

#Efficiency of storage layer
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime3,E_p, label=r'$\eta_a$ 500mD', color='blue', zorder= 1)
plt.plot(afTime4,E_p_50md, label=r'$\eta_a$ 50mD', color='red', zorder= 2)
# plt.plot(afTime3,efficiency, label=r'Efficiency of the storage layer', zorder=0)
# plt.axhline(y=100, color='black', linestyle='--', label='100% Efficiency')
# plt.plot(afTime3,total_E, label='current E', color ='black')
#plt.title('Efficiency of the storage layer over time')
plt.xlabel(r'Time [days]',fontsize=14)
plt.ylabel(r'Apparent efficiency [%]',fontsize=14)
ax.set_ylim(0,100)
plt.legend(fontsize=14)
plt.savefig('./Figures/EfficiencyOfStorage_rev.pdf',bbox_inches='tight')
# plt.show()
# plt.clf()

RPR_Pascal = RPR*100000
#Efficiency of storage layer
fig,ax1 = plt.subplots(figsize=(8,4))
set_plot_params(ax1)
ax1.plot(afTime3, ECT_Xflow_in, color='black', label=r'$E_i^s(t)$',zorder=4)
ax1.plot(afTime3, ECT_Xflow_out, color='black', linestyle='dashed', label=r'$E_p^s(t)$',zorder=3)
ax1.plot(afTime3,deltaET,color='red',label=r'$\Delta E^s$',zorder=2)
ax1.set_ylabel(r'Energy [kWh]', color='black',fontsize=14)
ax1.set_xlabel(r'Time [days]',fontsize=14)
ax1.tick_params('y')
#ax1.set_ylim(0, 100)
ax2 = ax1.twinx()
ax2.plot(afTime3, RPR_Pascal, color='orange', linestyle = 'dashed', label='$P_s$',zorder=1)
ax2.set_ylabel(r'$P_s$ [Pa]',fontsize=14)
ax2.set_xlabel(r'Time [days]',fontsize=14)
ax2.tick_params('y', colors='black')
ax2.set_ylim(2E7,3.6E7)
lines_1, labels_1 = ax2.get_legend_handles_labels()
lines_2, labels_2 = ax1.get_legend_handles_labels()
ax1.legend(lines_2+lines_1, labels_2+labels_1, loc='upper left',fontsize=14)
plt.savefig('./Figures/EnergyIn&Out_rev.pdf',bbox_inches='tight')
plt.show()
plt.clf()

# #Total Consumption
# plt.plot(afTime1,ECT_constantinjection,color='black',label=r'HYBRID ENERGY')
# plt.plot(afTime2,ECT_periodicinjection,color='black',linestyle='dashed', label=r'WIND POWERED')
# plt.plot(afTime3,ECT_energystorage,color='green',label=r'WIND & STORAGE')
# plt.title('Total Energy Consumption During Water Injection')
# plt.xlabel('Time [days]')
# plt.ylabel('Energy [kWh]')
# plt.legend()
# plt.savefig('./Figures/TotalConsumption_rev.pdf',bbox_inches='tight')
# plt.clf()

# # Total Consumption per oil
# fig,ax = plt.subplots(figsize=(8,4))
# set_plot_params(ax)
# plt.plot(afTime1,ECT_oil_CI,color='tab:blue', label=r'HYBRID ENERGY')
# plt.plot(afTime2,ECT_oil_PI,color='orange',label=r'WIND POWERED')
# plt.plot(afTime3,ECT_oil_ES,color='green',label=r'WIND+STORAGE')
# #plt.title('Total Energy Consumption Per Produced Oil')
# plt.xlabel('Time [days]')
# plt.ylabel('Energy [kWh/sm3]')
# plt.legend()
# plt.savefig('./Figures/TotalConsumptionPerOil_rev.pdf',bbox_inches='tight')
# plt.clf()

# #Total Consumption of storage layer
# fig,ax = plt.subplots(figsize=(8,4))
# set_plot_params(ax)
# plt.plot(afTime3,ECT_Xflow_in,color='black', label=r'Injected Energy')
# plt.plot(afTime3,ECT_Xflow_out,color='black',linestyle='dashed',label=r'Produced energy')
# plt.plot(afTime3,deltaET,color='orange',label=r'Energy changed in the storage layaer')
# #plt.plot(afTime3,deltaT,color='black')
# plt.xlabel('Time [days]')
# plt.ylabel('Energy [kWh]')
# plt.savefig('./Figures/TotalConsumption_storagelayer_rev.pdf',bbox_inches='tight')
# plt.legend()
# # plt.show()
# plt.clf()

# #Consumption per day
# fig,ax = plt.subplots(figsize=(8,4))
# set_plot_params(ax)
# plt.plot(afTime1,EC_constantinjection,label=r'HYBRID ENERGY')
# plt.plot(afTime2,EC_periodicinjection,label=r'WIND POWERED')
# #plt.title('Energy Consumption During Water Injection')
# plt.xlabel('Time [days]')
# plt.ylabel('Energy [kWh]')
# plt.legend()
# plt.savefig('./Figures/ConsumptionPerDayPI_rev.pdf',bbox_inches='tight')
# plt.clf()

# #Consumption per day
# fig,ax = plt.subplots(figsize=(8,4))
# set_plot_params(ax)
# plt.plot(afTime1,EC_constantinjection,label=r'HYBRID ENERGY')
# plt.plot(afTime3,EC_energystorage,label=r'WIND & STORAGE')
# #plt.title('Energy Consumption During Water Injection')
# plt.xlabel('Time [days]')
# plt.ylabel('Energy [kWh]')
# plt.legend()
# plt.savefig('./Figures/ConsumptionPerDayES_rev.pdf',bbox_inches='tight')
# plt.clf()

#cross flow rate
#Xflow_inflow_neg = -1 * Xflow_inflow
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,BHP_constantinjection*100000,color='blue', label=r'Hybrid energy')
plt.xlabel('Time [days]')
plt.ylabel('Injection Pressure [Pa]')
plt.legend()
plt.savefig('./Figures/INJ_Hybrid_rev.pdf',bbox_inches='tight')
plt.clf()

fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime2,BHP_periodicinjection*100000,color='orange', label=r'Wind powered')
plt.xlabel('Time [days]')
plt.ylabel('Injection Pressure [Pa]')
plt.legend()
plt.savefig('./Figures/INJ_Periodic_rev.pdf',bbox_inches='tight')
plt.clf()

fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime3,BHP_energystorage*100000,color='green', label=r'Wind power & storage')
plt.xlabel('Time [days]')
plt.ylabel('Injection Pressure [Pa]')
plt.legend()
plt.savefig('./Figures/INJ_ES_rev.pdf',bbox_inches='tight')
plt.clf()

excel_file = '../Book_day.xlsx'
df = pd.read_excel(excel_file)
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(df['Day'], df['Normalized average power'], color='steelblue', label=r'Daily Wind Power')
plt.xlabel(r'Time [days]',fontsize=14)
plt.ylabel(r'Normalized average wind power',fontsize=14)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.legend(fontsize=14)
plt.savefig('./Figures/windpower_rev.pdf',bbox_inches='tight')
plt.clf()

fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,FOPR_constantinjection,color='blue', label=r'Hybrid energy')
plt.plot(afTime2,FOPR_periodicinjection,color ='orange',label=r'Wind powered')
plt.plot(afTime3,FOPR_energystorage,color ='green',label=r'Wind power & storage')
plt.xlabel(r'Time [days]', fontsize=14)
plt.ylabel(r'Oil production rate [m$^3$/day]', fontsize=14)
plt.legend(fontsize=14)
plt.savefig('./Figures/FOPR_rev.png',bbox_inches='tight')

fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,WIR_constantinjection,color='blue', label=r'Hybrid energy',zorder=3)
plt.plot(afTime2,WIR_periodicinjection,color ='orange',label=r'Wind powered',zorder=2)
plt.plot(afTime3,WIR_energystorage,color ='green',label=r'Wind power & storage',zorder=1)
plt.xlabel(r'Time [days]',fontsize=14)
plt.ylabel(r'Water injection rate [m$^3$/day]',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('./Figures/WIR_rev.pdf',bbox_inches='tight')
#plt.show()

fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,GPR_constantinjection,color='blue', label=r'Hybrid energy')
plt.plot(afTime2,GPR_periodicinjection,color ='orange',label=r'Wind powered')
plt.plot(afTime3,GPR_energystorage,color ='green',label=r'Wind power & storage')
plt.xlabel(r'Time [days]',fontsize=14)
plt.ylabel(r'Gas production rate [m$^3$/day]',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('./Figures/GPR_rev.pdf',bbox_inches='tight')

fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,GPT_constantinjection,color='blue', label=r'Hybrid energy')
plt.plot(afTime2,GPT_periodicinjection,color ='orange',label=r'Wind powered')
plt.plot(afTime3,GPT_energystorage,color ='green',label=r'Wind power & storage')
plt.xlabel(r'Time [days]',fontsize=14)
plt.ylabel(r'Gas production total [m$^3$]',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('./Figures/GPT_rev.pdf',bbox_inches='tight')

Percent_change_oil_ES = ((FOPT_constantinjection[-1]-FOPT_energystorage[-1])/FOPT_constantinjection[-1])*100
Percent_change_oil_PI = ((FOPT_constantinjection[-1]-FOPT_periodicinjection[-1])/FOPT_constantinjection[-1])*100
print('Percent change ES', Percent_change_oil_ES)
print('Percent change PI', Percent_change_oil_PI)

percent_change_gas_ES = ((GPT_constantinjection[-1]-GPT_energystorage[-1])/GPT_constantinjection[-1])*100
percent_change_gas_PI = ((GPT_constantinjection[-1]-GPT_periodicinjection[-1])/GPT_constantinjection[-1])*100
print('Percent change gas ES', percent_change_gas_ES)
print('Percent change gas PI', percent_change_gas_PI)

percent_diff_oil_ES_PI = ((FOPT_energystorage[-1]-FOPT_periodicinjection[-1])/FOPT_energystorage[-1])*100
print('Percent difference oil ES & PI', percent_diff_oil_ES_PI)
percent_diff_oil_ES_Constant = ((FOPT_energystorage[-1]-FOPT_constantinjection[-1])/FOPT_energystorage[-1])*100
print('Percent difference oil ES & Constant', percent_diff_oil_ES_Constant)
fig,ax = plt.subplots(figsize=(8,4)) 
set_plot_params(ax)
plt.plot(afTime1,FOPT_constantinjection,color='blue', label=r'Hybrid energy')
plt.plot(afTime2,FOPT_periodicinjection,color ='orange',label=r'Wind powered')
plt.plot(afTime3,FOPT_energystorage,color ='green',label=r'Wind power & storage')
plt.xlabel(r'Time [days]',fontsize=14)
plt.ylabel(r'Cumulative oil production [m$^3$]',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('./Figures/FOPT_rev.png',bbox_inches='tight')



fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime1,WIT_constantinjection,color='blue', label=r'Hybrid energy')
plt.plot(afTime2,WIT_periodicinjection,color ='orange',label=r'Wind powered')
plt.plot(afTime3,WIT_energystorage,color ='green',label=r'Wind power & storage')
plt.xlabel(r'Time [days]',fontsize=14)
plt.ylabel(r'Cumulative water injection [m$^3$]',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('./Figures/FWIT_rev.png',bbox_inches='tight')

percent_change_water_ES = ((WIT_constantinjection[-1]-WIT_energystorage[-1])/WIT_constantinjection[-1])*100
percent_change_water_PI = ((WIT_constantinjection[-1]-WIT_periodicinjection[-1])/WIT_constantinjection[-1])*100
print('Percent change water ES', percent_change_water_ES)
print('Percent change water PI', percent_change_water_PI)
