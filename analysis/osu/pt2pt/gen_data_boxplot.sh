#!/bin/bash

#latency

echo -n "bare metal : "
echo -n '['
find bare/ -type f -name "osu_latency*" | while read -r file; do
	grep -R "^64" $file | awk -F ' ' '{printf $2 ","}'
done
echo ']'

echo -n "usernetes : "
echo -n '['
find usernetes/ -type f -name "osu_latency*" | while read -r file; do
	grep -R "^64" $file | awk -F ' ' '{printf $2 ","}'
done
echo ']'


#bandwidth

echo -n "bare metal : "
echo -n '['
find bare/ -type f -name "osu_bw*" | while read -r file; do
	grep -R "^4194304" $file | awk -F ' ' '{printf $2 ","}'
done
echo ']'

echo -n "usernetes : "
echo -n '['
find usernetes/ -type f -name "osu_bw*" | while read -r file; do
	grep -R "^4194304" $file | awk -F ' ' '{printf $2 ","}'
done
echo ']'
