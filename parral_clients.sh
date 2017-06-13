#!/bin/bash
file="./keys.txt"
keys_count=`cat keys.txt | wc -l`
i=0
while read line
do
	python3 worker.py $line $i &  
	echo 'worker' $i 'are enabled'   	
	i=$[i+1]
	
done < $file
