#!/bin/bash

#me da pereza hacer los casos de prueba a mano....

INI=0
FIN=33

for i in $( seq $INI $FIN ); do

	if [[ $i -lt 10 ]]; then
		folder="./0$i"
	else
		folder="./$i"
	fi
	mkdir $folder

	sol=$(( $i + 1 ))

	echo "" > "${folder}/in_arguments"
	echo "$i" > "${folder}/in_stdin"
	echo "$sol" > "${folder}/out"

done
