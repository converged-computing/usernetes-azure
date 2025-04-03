#!/bin/bash
echo "bare:"
#awk -F' Matom-step/s' '{print $(NF-1)}'
for value in 4 8 16 32
do
	echo "VALUE $value"
	grep -R "^Performance:" bare/lammps-$value* | tr '.' ',' | awk -F ' ' '{sum += $8;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "^Performance:" bare/lammps-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($8 > max) max=$8;} END{print "MAX : " max ;}'
	grep -R "^Performance:" bare/lammps-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=100000} {if ($8 < min) min=$8;} END{print "MIN : " min ;}'
done
echo "usernetes:"

for value in 4 8 16 32
do
	echo "VALUE $value"
	grep -R "^Performance:" usernetes/lammps-$value* | tr '.' ',' | awk -F ' ' '{sum += $8;total+=1;} END{print "AVERAGE : " sum "/" total " : " sum/total;}'
	grep -R "^Performance:" usernetes/lammps-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{max=0} {if ($8 > max) max=$8;} END{print "MAX : " max ;}'
	grep -R "^Performance:" usernetes/lammps-$value* | tr '.' ',' | awk -F ' ' ' BEGIN{min=100000} {if ($8 < min) min=$8;} END{print "MIN : " min ;}'
done
