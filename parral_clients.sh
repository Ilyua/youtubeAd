#!/bin/bash
file="./keys.txt"
i=0
keys_count=`cat keys.txt | wc -l`

while read line
do
	#echo $i && echo $[i+keys_count] &
	python3 main.py $line $i >>/tmp/out_$line.log && python3 main.py $line $[i+keys_count] >>/tmp/out_$line.log  
	i=$[i+1]	
done < $file