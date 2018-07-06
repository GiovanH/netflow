#!/bin/bash

files="../20180110/00*.csv"
logfile="./logs/tests.log"
# "C:/ProgramData/Anaconda3/python.exe" netflow.py \
	# --nowindow \
	# --verbose \
	# --compress_field ip \
	# "${files}" \
	# hist_out        hist_in        top_contributors_out        top_contributors_in        top_percent_in        top_percent_out       top_percent_in_owners        top_percent_out_owners

rm -v ./logs/tests.log 2>/dev/null

echo Fileglob: "${files}"			| tee -a ${logfile}
echo Files: ${files}			| tee -a ${logfile}
	
for ip_type in src_ip
do
	for percent in 80
	do
		echo Percent: ${percent}			| tee -a ${logfile}
		echo IP type: ${ip_type}			| tee -a ${logfile}
		"C:/ProgramData/Anaconda3/python.exe" netflow.py \
			--percent ${percent} \
			--ip_type ${ip_type} \
			--nowindow \
			--verbose \
			--scaletozero \
			--compress_field ip \
			"${files}" \
			top_percent_in_owners top_percent_in top_percent_out top_percent_out_owners \
			| tee -a ${logfile}

		# "C:/ProgramData/Anaconda3/python.exe" netflow.py \
			# --percent ${percent} \
			# --ip_type ${ip_type} \
			# --nowindow \
			# --verbose \
			# --scaletozero \
			# --compress_field ip \
			# "${files}" \
			# top_percent_in top_percent_out \
			# | tee -a ${logfile}
	done
done
