#!/bin/bash
echo "bare:"
for value in 4 8 16 32
do
	echo "VALUE $value"
	grep -R "^64" bare/osu_allreduce-$value* | tr '.' ',' | awk -F ' ' '{sum += $2;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "^64" bare/osu_allreduce-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($2 > max) max=$2;} END{print "MAX : " max ;}'
	grep -R "^64" bare/osu_allreduce-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=100000} {if ($2 < min) min=$2;} END{print "MIN : " min ;}'
done
echo "usernetes:"

for value in 4 8 16 32
do
	echo "VALUE $value"
	grep -R "^64" usernetes/osu_allreduce-$value* | tr '.' ',' | awk -F ' ' '{sum += $2;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "^64" usernetes/osu_allreduce-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($2 > max) max=$2;} END{print "MAX : " max ;}'
	grep -R "^64" usernetes/osu_allreduce-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=100000} {if ($2 < min) min=$2;} END{print "MIN : " min ;}'
done
