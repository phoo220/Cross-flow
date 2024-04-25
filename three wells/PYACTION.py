import datetime

def run(ecl_state, schedule, report_step, summary_state, actionx_callback):
    if (not 'act01_executed' in globals()):
        globals()["act01_executed"] = False
        globals()["act02_executed"]= False
        
    current_time = schedule.start + datetime.timedelta(seconds=summary_state.elapsed())
    
    BHP_TOP = summary_state.well_var("INJ","WBHP")
    BHP_BOT = summary_state.well_var("INJX","WBHP")
    DeltaP = BHP_BOT - BHP_TOP
    
    if (DeltaP <= 0 and current_time.day > 0 and current_time.month >= 1 and current_time.year >= 2023 and not globals()["act01_executed"]):
        print("Bottom layer close at {}\n".format(current_time))
        kw = """
        WCONINJE
        'INJ' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	260	/
	    'INJX' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	265 	/
	    'I' 	    'WAT'	'SHUT'	RATE 	1000 	1* 	250	/
        /
        """
    schedule.insert_keywords(kw)
    globals()["act01_executed"] = True
    
    if (DeltaP > 0 and not globals()["act02_executed"]):
        print("PYACTION reopens the cross-flow layer at {}\n".format(current_time))
        kw = """
        WCONINJE
        'INJ' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	260 	/
	    'INJX' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	265 	/
	    'I' 	    'WAT'	'STOP'	RATE 	1000 	1* 	250	    /
        /
        """
        schedule.insert_keywords(kw)
        globals()["act02_executed"] = True
        