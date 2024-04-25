import datetime

def run(ecl_state, schedule, report_step, summary_state, actionx_callback):

    current_time = schedule.start + datetime.timedelta(seconds=summary_state.elapsed())
    
    BHP_TOP = summary_state.well_var("INJ","WBHP")
    BHP_BOT = summary_state.well_var("INJX","WBHP")
    DeltaP = BHP_BOT - BHP_TOP
    
    #SHUT = no cross flow
    #STOP = cross flow  
    
    if (not DeltaP <= 0 ):
        print("Bottom layer open at {}\n".format(current_time))
        schedule.stop_well("I",report_step) 
        
    if (DeltaP <= 0 ):
        print("Bottom layer close at {}\n".format(current_time))
        schedule.shut_well("I",report_step+1)  
    
    
    #if (DeltaP <= 0 ):
    #    print("Bottom layer close at {}\n".format(current_time))
    #    kw ="""
    #    WELOPEN
    #    I   OPEN                        /
    #    I   OPEN    1   1   1           /
    #    I   SHUT    1   1   3           /
    #    /   
    #    """
    #    #'INJ' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	260	/
	#    #'INJX' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	265 	/
	#    #'I' 	    'WAT'	'SHUT'	RATE 	1000 	1* 	250	/
    #    #/
    #    #"""
    #    schedule.insert_keywords(kw)
    #
    #if (not DeltaP <= 0): 
    #    print("PYACTION reopens the cross-flow layer at {}\n".format(current_time))
    #    kw = """
    #    WELOPEN
    #    I   OPEN                        /
    #    I   OPEN    1   1   1           /
    #    I   OPEN    1   1   3           /
    #    /   
    #    """
    #    # WCONINJE
    #    # 'INJ' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	260 	/
	#    # 'INJX' 	    'WAT' 	'OPEN' 	BHP 	2000 	1* 	265 	/
	#    # 'I' 	    'WAT'	'STOP'	RATE 	1000 	1* 	250	    /
    #    # /
    #    # """
    #    schedule.insert_keywords(kw)
        