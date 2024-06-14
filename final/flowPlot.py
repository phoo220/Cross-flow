#!/usr/bin/env python3
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################
#
# A script to plot reservoir simulation results from the
# Flow reservoir simulator.
# Carl Fredrik Berg, carl.f.berg@ntnu.no, 2018
#
import sys
import argparse
from ecl.summary import EclSum
import numpy as np
import argparse
import math
import matplotlib.pyplot as plt

# ****************** INPUT *********************
parser = argparse.ArgumentParser(prog='flowPlot.py',description='A script to plot reservoir simulation results from the Flow reservoir simulator.')
parser.add_argument("models",nargs='+', help="Flow reservoir simulation results to read in.")
parser.add_argument("-v", type=str,help="List of vectors to plot.")
parser.add_argument("-xlog",action='store_true',help="Log-scale on x-axis.")
parser.add_argument("-ylog",action='store_true',help="Log-scale on y-axis.")
parser.add_argument("-save",type=str,help="Provide file name to save plot. If provided, then the script will not show a plot.")
parser.add_argument("-listvectors",action='store_true',help="List all available vectors.")

args = parser.parse_args()

try:
        args.models
except:
        print("You need to suply a model to be plotted.")

#Parameters to controll plot layout
params = {'legend.fontsize': 18,
          'legend.handlelength': 1}
plt.rcParams.update(params)
plt.rc('font',size=18)
fig,ax = plt.subplots(figsize=(16,8))
ax.tick_params(labelsize=18)
ax.tick_params(axis='both',length=5.0,width=1.5)
ax.tick_params(axis='both',which='minor',length=3.0,width=1.0)
ax.grid(True)


for strModel in args.models:
        if strModel.find('.')<0:
                strModelName=strModel
        else:
            strModelName=strModel.split(".")[:-1][0]
        try:
                tSummaryData=EclSum(strModelName+'.UNSMRY')
        except:
                print('Warning: Could not find the summary-file (*.UNSMRY) for flow case '+strModelName)
        if args.listvectors:
                print(tSummaryData.keys())
                sys.exit()
        else:
                if args.v:
                        strYLabel=''
                        tstrVectors=args.v.split(",")
                        for strVector in tstrVectors:
                                afTime=tSummaryData.numpy_vector("TIME")
                                afVector=tSummaryData.numpy_vector(strVector)
                                ax.plot(afTime,afVector,linewidth=2.0,label='%s, %s' % (strModelName,strVector))
                                strYLabel=strYLabel+', %s (%s)' % (strVector,tSummaryData.unit(strVector))
                else:
                        print("You need to suply a vector to plot.")
                        sys.exit()

if args.xlog:
    ax.set_xscale('log')
if args.ylog:
    ax.set_yscale('log')

ax.set_xlabel('TIME (%s)' % tSummaryData.unit("TIME"))
ax.set_ylabel(strYLabel[2:])
ax.legend(loc='best')

if args.save:
        fig.tight_layout()
        plt.savefig(args.save)
else:
        plt.show()
