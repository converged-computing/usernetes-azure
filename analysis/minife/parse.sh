#!/bin/bash
echo "bare:"
#awk -F' Matom-step/s' '{print $(NF-1)}'
for value in 384 768 1536 3072
do
	echo "VALUE $value"
	grep -R "Total CG Mflops:" bare/miniFE.230x230x230.P$value* | tr '.' ',' | awk -F ' ' '{sum += $5;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "Total CG Mflops:" bare/miniFE.230x230x230.P$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($5 > max) max=$5;} END{print "MAX : " max ;}'
	grep -R "Total CG Mflops:" bare/miniFE.230x230x230.P$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=10000000} {if ($5 < min) min=$5;} END{print "MIN : " min ;}'
done
echo "usernetes:"

for value in 384 768 1536 3072
do
	echo "VALUE $value"
	grep -R "Total CG Mflops:" usernetes/miniFE.230x230x230.P$value* | tr '.' ',' | awk -F ' ' '{sum += $5;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "Total CG Mflops:" usernetes/miniFE.230x230x230.P$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($5 > max) max=$5;} END{print "MAX : " max ;}'
	grep -R "Total CG Mflops:" usernetes/miniFE.230x230x230.P$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=10000000} {if ($5 < min) min=$5;} END{print "MIN : " min ;}'
done
