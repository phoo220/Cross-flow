import sys
from ecl.summary import EclSum
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


Vb =(100*100*50)*0.3
ct = 4.67e-5 + 4.84e-5
tSummaryData3=EclSum('TEST'+'.UNSMRY')
afTime3=tSummaryData3.numpy_vector("TIME")
afTime3Diff=afTime3[1:]-afTime3[:-1]
afTime3Diff=np.insert(afTime3Diff,0,afTime3[0])

#injection rates
WIR = tSummaryData3.numpy_vector("FWIR")
BHP = tSummaryData3.numpy_vector("WBHP:INJ")
E_Inj = (WIR*BHP*afTime3Diff/36)
E_Inj[0] = 0.0
ET_Inj = np.cumsum(E_Inj)

def numpy_vector(identifier):
        parts = identifier.split(':')[1].split(',')
        return np.array([int(parts[0]), int(parts[1]), int(parts[2])]) 

P = []
for i in range(1, 4):
    for j in range(1, 4):
        identifier = f"BPR:{i},{j},1"
        P.append(tSummaryData3.numpy_vector(identifier))
        
total_E = np.zeros_like(E_Inj)
for j in range(0,len(P[0])):
    E = 0 
    for i in range(0,len(P)):
        # print(P[i][j])
        E += (Vb*ct/2)*(P[i][j]** 2 )/36
        #print(deltaE) 
    total_E[j] = E
# deltaET =np.cumsum(total_deltaE)

deltaE = np.zeros_like(E_Inj)
for j in range(1,len(P[0])):
    delta_E = 0 
    for i in range(0,len(P)):
        # print(P[i][j])
        delta_E += (Vb*ct/2)*(P[i][j]** 2 - P[i][j-1]** 2)/36
        #print(deltaE) 
    deltaE[j] = delta_E
deltaET =np.cumsum(deltaE)

def set_plot_params(ax):
    ax.tick_params(axis='both', length=5.0, width=1.5)
    ax.tick_params(axis='both', which='minor', length=3.0, width=1.0)
    ax.grid(True)

fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.scatter(afTime3,deltaE, label='current delta E', color ='red')
plt.scatter(afTime3,E_Inj, label='Injected energy', color = 'blue')
plt.xlabel('Time [days]')
plt.ylabel('kWh')
plt.legend()
plt.show()

#Efficiency of storage layer
fig,ax = plt.subplots(figsize=(8,4))
set_plot_params(ax)
plt.plot(afTime3,ET_Inj, label='Total injected', color ='blue')
plt.plot(afTime3,deltaET, label='Total deltaE', color = 'red')
plt.xlabel('Time [days]')
plt.ylabel('kWh')
plt.legend()
plt.show()