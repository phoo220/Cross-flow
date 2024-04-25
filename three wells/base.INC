RUNSPEC

TITLE
   Xflow-model

DIMENS
   10 10 3 /

EQLDIMS
/

TABDIMS
/

OIL 

WATER

GAS

DISGAS

METRIC

START
   1 'JAN' 2023 /

WELLDIMS
   4 5 3 4 /

UNIFIN
UNIFOUT

GRID

INIT

NOECHO

DX 
  300*100 /

DY	
	300*100 /

DZ
	100*40 100*5 100*30 /

TOPS
	100*3000 /

PORO
  300*0.3 /

PERMX
	100*500 100*0 100*500 /

PERMY
	100*500 100*0 100*500 /

PERMZ
	100*500 100*0 100*500 /

ECHO

PROPS
-------------------------------------------------------------------------
NOECHO

INCLUDE
'../PROPS.INC' / 

REGIONS 
-- ---------------------------------------------------------------------------
 EQUALS
--          I1  I2  J1  J2  K1  K2
 FIPNUM 1    1*  1*  1*  1*  1  1 / SET REGION 1
 FIPNUM 2    1*  1*  1*  1*  3  3 / SET REGION 1
/

SOLUTION
-- -------------------------------------------------------------------------

EQUIL
--datum press OWC WATCAP GOC GASCAP 
	3000 250 3042 0 3010 0 1 0 0 /

RPTSOL
FIP=2 SWAT /

RSVD
-- Depth    RS(dissolved gas)
3000 90
3035 90 /


SUMMARY
-- -------------------------------------------------------------------------	 

FOPR
FOPT
FLPR
FWPR
FWPT
FWIR
FWIT
FPR
FGOR

CWFR
	'INJ'  1 1 1  /
  'INJX' 1 1 3  /
	'I'    1 1 1  /
  'I'    1 1 3  /
/

CWIR
	'INJ'  1 1 1  /
  'INJX' 1 1 3  /
	'I'    1 1 1  /
  'I'    1 1 3  /
/

CWIT
	'INJ'  1 1 1  /
  'INJX' 1 1 3  /
	'I'    1 1 1  /
  'I'    1 1 3  /
/

WGOR
  'PROD'
/

BPR
1	  1 	1 /
1 	1 	3 / 
-- 2   2   1 /
-- 2   2   3 /
10 	10 	1 /
/

BGSAT
1 	1 	1 /
1 	1 	3 / 
10 	10 	1 /
/

-- In order to compare Eclipse with Flow:
WBHP
  'INJ'
  'PROD'
  'INJX'
  'I'
/
WGPR
  'PROD'
/
WGPT
  'PROD'
/
WOPR
  'PROD'
/
WOPT
  'PROD'
/
WWIR
  'INJ'
  'INJX'
  'I'
/
WWIT
  'INJ'
  'INJX'
  'I'
/
WWPR
  'PROD'
/
WWPT
  'PROD'
/
WBHP
  'PROD'
  'INJ'
  'INJX'
  'I'
/
