#!/bin/bash

files="../20180110/*.csv"
percent=60

mv -v ./img/*.png ./img/old/

"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type src_ip --nowindow --compress_field ip "${files}" top_percent_in_owners top_percent_out_owners | tee -a logs/${percent}perc_whoisowners_sources.log
"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type dest_ip --nowindow --compress_field ip "${files}" top_percent_in_owners top_percent_out_owners | tee -a logs/${percent}perc_whoisowners_destinations.log

# "C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type src_ip --nowindow --compress_field ip "${files}" top_percent_in top_percent_out
# "C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --ip_type dest_ip --nowindow --compress_field ip "${files}" top_percent_in top_percent_out


# "C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --nowindow --ip_type src_ip --compress_field ip "${files}" top_percent_in top_percent_out | tee logs/50percent_in_out_srcip.log
# "C:/ProgramData/Anaconda3/python.exe" netflow.py --percent ${percent} --nowindow --ip_type dest_ip --compress_field ip "${files}" top_percent_in top_percent_out | tee logs/50percent_in_out_destip.log

# "C:/ProgramData/Anaconda3/python.exe" netflow.py --nowindow --ip_type src_ip --compress_field ip "${files}" hist_out hist_in top_contributors_out top_contributors_in top_percent_in top_percent_out | tee logs/alltests.log
# "C:/ProgramData/Anaconda3/python.exe" netflow.py --nowindow --ip_type dest_ip --compress_field ip "${files}" hist_out hist_in top_contributors_out top_contributors_in top_percent_in top_percent_out | tee -a logs/alltests.log
