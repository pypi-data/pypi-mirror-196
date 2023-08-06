This package contains the function syn_proc that takes a list of a SYN file lines as an argument and returns two dataframes:
    - quot_df for daily synoptic observations
    - hor_df for threehourly synoptic observations

Usage:
simply import your SYN file into a list then pass the imported list as an argument into the syn_proc function 

Example:
    with open('SYNobs.THR') as f:         ## or .M01 .M02 ...... etc
                        
        lines = f.readlines()

treehor_df,daily_df=syn_proc(lines)
