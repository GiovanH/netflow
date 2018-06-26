#!/bin/bash

"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent 50 --nowindow --ip_type src_ip --compress_field ip "../20180110/*.csv" top_percent_in top_percent_out  >50percent_in_out_srcip.log
"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent 50 --nowindow --ip_type dest_ip --compress_field ip "../20180110/*.csv" top_percent_in top_percent_out >50percent_in_out_destip.log

"C:/ProgramData/Anaconda3/python.exe" netflow.py --nowindow --ip_type src_ip --compress_field ip "../20180110/*.csv" hist_out hist_in top_contributors_out top_contributors_in top_percent_in top_percent_out >alltests.log
"C:/ProgramData/Anaconda3/python.exe" netflow.py --nowindow --ip_type dest_ip --compress_field ip "../20180110/*.csv" hist_out hist_in top_contributors_out top_contributors_in top_percent_in top_percent_out >>alltests.log