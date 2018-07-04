#!/bin/bash

rm ./logs/*.log

files="../20180110/*.csv"
for ip_type in src_ip dest_ip
do
	for percent in 80 60 40 20
	do
		echo Percent: ${percent}
		echo IP type: ${ip_type}
		"C:/ProgramData/Anaconda3/python.exe" netflow.py \
			--percent ${percent} \
			--ip_type ${ip_type} \
			--nowindow \
			--compress_field ip "${files}" \
			top_percent_in_owners top_percent_out_owners \
			| tee -a ./logs/${percent}perc_whoisowners_${ip_type}.log

		"C:/ProgramData/Anaconda3/python.exe" netflow.py \
			--percent ${percent} \
			--ip_type ${ip_type} \
			--nowindow \
			--compress_field ip "${files}" \
			top_percent_in top_percent_out \
			| tee -a ./logs/${percent}perc_${ip_type}.log
	done
done
