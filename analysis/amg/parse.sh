#!/bin/bash
echo "bare:"
for value in 4 8 16 32
do
	echo "VALUE $value"
	grep -R "Figure of Merit" bare/amg-$value* | tr '.' ',' | awk -F ' ' '{sum += $16;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "Figure of Merit" bare/amg-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($16 > max) max=$16;} END{print "MAX : " max ;}'
	grep -R "Figure of Merit" bare/amg-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=1000000000} {if ($16 < min) min=$16;} END{print "MIN : " min ;}'
done
echo "usernetes:"

for value in 4 8 16 32
do
	echo "VALUE $value"
	grep -R "Figure of Merit" usernetes/amg-$value* | tr '.' ',' | awk -F ' ' '{sum += $16;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "Figure of Merit" usernetes/amg-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($16 > max) max=$16;} END{print "MAX : " max ;}'
	grep -R "Figure of Merit" usernetes/amg-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=1000000000} {if ($16 < min) min=$16;} END{print "MIN : " min ;}'
done
