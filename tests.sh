#!/bin/bash

files="../20180110/*0.csv"
logfile="./logs/tests.log"
polynomial=4
moreargs="--scaletozero"
# "C:/ProgramData/Anaconda3/python.exe" netflow.py \
	# --nowindow \
	# --verbose \
	# --compress_field ip \
	# "${files}" \
	# hist_out        hist_in        top_contributors_out        top_contributors_in        top_percent_in        top_percent_out       top_percent_in_owners        top_percent_out_owners

#"C:/ProgramData/Anaconda3/python.exe" netflow.py --percent 80 --verbose --compress_field ip "../20180110/01*.csv" top_percent_in_owners

rm -v ${logfile} 2>/dev/null

echo Fileglob: "${files}"			| tee -a ${logfile}
echo Files: ${files}			| tee -a ${logfile}



for percent in 70
do
	echo Percent: ${percent}			| tee -a ${logfile}
	for file in $files
	do
		"C:/ProgramData/Anaconda3/python.exe"  netflow.py \
			--percent ${percent} \
			--nowindow \
			--verbose \
			${moreargs} \
			--regress $polynomial\
			"${file}" \
			icannpercent_out_dest icannpercent_out_src \
														icannpercent_in_src  \
			| tee -a ${logfile}
	done
	"C:/ProgramData/Anaconda3/python.exe"  netflow.py \
		--percent ${percent} \
		--nowindow \
		--verbose \
		${moreargs} \
		--regress $polynomial\
		"${files}" \
		icannpercent_out_dest icannpercent_out_src \
													icannpercent_in_src  \
		| tee -a ${logfile}
done


./montage.sh
