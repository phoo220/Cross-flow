import os
from ecl.summary import EclSum
import numpy as np
from datetime import date, datetime, timedelta
import sys

def main(args):
   filename = args[0]
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
   afOilProd=tSummaryData.numpy_vector("FOPR")
   #afGasProd=tSummaryData.numpy_vector("FGPR")
   afWaterProd=tSummaryData.numpy_vector("FWPR")
   afWaterInj=tSummaryData.numpy_vector("FWIR")
   # aBHPProd=tSummaryData.numpy_vector("WBHP:PROD")
   # aBHPInj=tSummaryData.numpy_vector("WBHP:INJ")
   # afGasInj=tSummaryData.numpy_vector("WGIR:INJ")
   # afGasLift=tSummaryData.numpy_vector("WGIR:PROD")
   # afBPR_highperm=tSummaryData.numpy_vector("BPR:1,1,1")
   # afBPR_lowperm=tSummaryData.numpy_vector("BPR:1,1,3")
   strHeader='Dates, OIL_PROD, WATER_PROD, WATER_INJ, GAS_INJ, GAS_LIFT, BHP_PROD, BHP_INJ, Pr(High), Pr(Low) \n #, Sm3/d, Sm3/d, m3/d, m3/d, Sm3/d, Sm3/d, kPa, kPa \n'
   extractdata = filename+".csv"
   outFile=open(extractdata, 'w')
   outFile.write(strHeader)
   for ii in range(len(afTimeNP)):
      outFile.write(str(afTimeNP[ii])+', '+str(afOilProd[ii])+', '+str(afWaterProd[ii])+', '+str(afWaterInj[ii])+'\n')
   # for ii in range(len(afTimeNP)):
   #  outFile.write(str(afTimeNP[ii])+', '+str(afOilProd[ii])+', '+str(afGasProd[ii])+', '+str(afWaterProd[ii])+', '+str(afWaterInj[ii])+', '+str(afGasInj[ii])+', '+str(afGasLift[ii])+', '+str(aBHPProd[ii])+', '+str(aBHPInj[ii])+', '+str(afBPR_highperm[ii])+', '+str(afBPR_lowperm[ii])+'\n')

if __name__ == '__main__':
   # print(sys.argv)
   main(sys.argv[1:])