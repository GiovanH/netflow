#!/bin/bash
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
	anaconda3="/home/stg160130/anaconda3/bin/python3 -u	"
elif [[ "$unamestr" == 'CYGWIN_NT-10.0' ]]; then
	anaconda3="/cygdrive/c/ProgramData/anaconda3/python.exe -u "
fi
# anaconda3="$anaconda3 -m cProfile -s cumtime"

files="../day=20180804/*.csv"
logfile="./logs/tests.log"
polynomial=4
moreargs="--scaletozero"
percents="70"
num=10
# $anaconda3 netflow.py \
	# --nowindow \
	# --verbose \
	# --compress_field ip \
	# "${files}" \
	# hist_out        hist_in        top_contributors_out        top_contributors_in        top_percent_in        top_percent_out       top_percent_in_owners        top_percent_out_owners

#$anaconda3 netflow.py --percent 80 --verbose --compress_field ip "../20180110/01*.csv" top_percent_in_owners

rm -v ${logfile} 2>/dev/null

echo Fileglob: "${files}"			| tee -a ${logfile}
echo Files: ${files}			| tee -a ${logfile}

for percent in ${percents}
do
	echo Percent: ${percent}			| tee -a ${logfile}
	$anaconda3  netflow.py \
		--percent ${percent} \
		--num ${num} \
		--nowindow \
		--verbose \
		${moreargs} \
		--regress $polynomial\
		"${files}" \
		icannpercent_out_dest icannpercent_out_src \
		icannpercent_in_src  \
		icannstacktime_in_src icannstacktime_out_dest \
		| tee -a ${logfile}
	# for file in $files
	# do
	# 	$anaconda3  netflow.py \
	# 		--percent ${percent} \
	# 		--num ${num} \
	# 		--nowindow \
	# 		--verbose \
	# 		${moreargs} \
	# 		--regress $polynomial\
	# 		"${file}" \
	# 		icannpercent_out_dest icannpercent_out_src \
	# 		icannpercent_in_src  \
	# 		icannstacktime_in_src \
	# 		| tee -a ${logfile}
	# done
done


# ./montage.sh
