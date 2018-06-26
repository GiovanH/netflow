#!/bin/bash

files="../20180110/01*.csv"

mv -v ./img/*.png ./img/old/

"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent 50 --nowindow --ip_type src_ip --compress_field ip ${files} top_percent_in top_percent_out | tee logs/50percent_in_out_srcip.log
"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent 50 --nowindow --ip_type dest_ip --compress_field ip ${files} top_percent_in top_percent_out | tee logs/50percent_in_out_destip.log

"C:/ProgramData/Anaconda3/python.exe" netflow.py --nowindow --ip_type src_ip --compress_field ip ${files} hist_out hist_in top_contributors_out top_contributors_in top_percent_in top_percent_out | tee logs/alltests.log
"C:/ProgramData/Anaconda3/python.exe" netflow.py --nowindow --ip_type dest_ip --compress_field ip ${files} hist_out hist_in top_contributors_out top_contributors_in top_percent_in top_percent_out | tee -a logs/alltests.log