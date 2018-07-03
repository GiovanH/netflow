#!/bin/bash

files="../20180110/*.csv"
percent=90

"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type src_ip --nowindow --compress_field ip "${files}" top_percent_in_owners top_percent_out_owners | tee -a logs/${percent}perc_whoisowners_sources.log
"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type dest_ip --nowindow --compress_field ip "${files}" top_percent_in_owners top_percent_out_owners | tee -a logs/${percent}perc_whoisowners_destinations.log

"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type src_ip --nowindow --compress_field ip "${files}" top_percent_in top_percent_out | tee -a logs/${percent}perc_destinations.log
"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type dest_ip --nowindow --compress_field ip "${files}" top_percent_in top_percent_out | tee -a logs/${percent}perc_destinations.log
