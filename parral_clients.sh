#!/bin/bash
file="./keys.txt"
keys_count=`cat keys.txt | wc -l`
i=0
#while read line
#do
	
	#while [ $i -lt 10 ] 

	python3 worker.py  $i && echo $i     
	#i=$[i+1]	
	#done
	#wait
	echo 'Finished'
#done < $file