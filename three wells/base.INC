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
	100*40 100*5 100*40 /

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
	3000 200 3042 0 3010 0 1 0 0 /

RPTSOL
FIP=2 SWAT /

RSVD
-- Depth    RS(dissolved gas)
3000 90
3042 90 /


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
RPR
/
-- FGOR

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

-- WGOR
--   'PROD'
-- /

BPR
1	  1 	1/
1 	1 	3/ 
1 	2 	3/
1 	3 	3/
1 	4 	3/ 
1 	5 	3/
1 	6 	3/
1 	7 	3/ 
1 	8 	3/
1 	9 	3/
1 	10 	3/
2 	1 	3/ 
2 	2 	3/
2 	3 	3/
2 	4 	3/ 
2 	5 	3/
2 	6 	3/
2 	7 	3/ 
2 	8 	3/
2 	9 	3/
2 	10 	3/
3 	1 	3/ 
3 	2 	3/
3 	3 	3/
3 	4 	3/ 
3 	5 	3/
3 	6 	3/
3 	7 	3/ 
3 	8 	3/
3 	9 	3/
3 	10 	3/
4 	1 	3/
4 	2 	3/
4 	3 	3/
4 	4 	3/
4 	5 	3/
4 	6 	3/
4 	7 	3/
4 	8 	3/
4 	9 	3/
4 	10 	3/
5 	1 	3/
5 	2 	3/
5 	3 	3/
5 	4 	3/ 
5 	5 	3/
5 	6 	3/
5 	7 	3/
5 	8 	3/
5 	9 	3/
5 	10 	3/
6 	1 	3/
6 	2 	3/
6 	3 	3/
6 	4 	3/
6 	5 	3/
6 	6 	3/
6 	7 	3/ 
6 	8 	3/
6 	9 	3/
6 	10 	3/
7 	1 	3/
7 	2 	3/
7 	3 	3/
7 	4 	3/
7 	5 	3/
7 	6 	3/
7 	7 	3/
7 	8 	3/
7 	9 	3/
7 	10 	3/
8 	1 	3/
8 	2 	3/
8 	3 	3/
8 	4 	3/
8 	5 	3/
8 	6 	3/
8 	7 	3/
8 	8 	3/
8 	9 	3/
8 	10 	3/
9 	1 	3/
9 	2 	3/
9 	3 	3/
9 	4 	3/
9 	5 	3/
9 	6 	3/
9 	7 	3/
9 	8 	3/
9 	9 	3/
9 	10 	3/
10 	1 	3/
10 	2 	3/
10 	3 	3/
10 	4 	3/
10 	5 	3/
10 	6 	3/
10 	7 	3/
10 	8 	3/
10 	9 	3/
10 	10 	3/
10 	10 	1/
/

BGSAT
1 	1 	1 /
1 	1 	3 / 
10 	10 	1 /
/

WBHP
  'INJ'
  'PROD'
  'INJX'
  'I'
/

-- WGPR
--   'PROD'
-- /
-- WGPT
--   'PROD'
-- /

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
