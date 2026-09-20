#!/bin/bash

HELP="
## Este script muestra toda la información pública de un problema de forma bonita
## Es decir, concatena todos los pequeños archivos que definen un problema y lo muestra por la salida estándar todo al a vez
##
## INPUT: el número del problema (con el número es suficiente, no hace falta indicar el nombre completo)
## OUTPUT: la salida de un problema
"


#[ -z ${CB_ACTIVE+x} ] && source "./setup.sh"
source "./setup.sh"

set -u


function compose_problem {
    # $i -> problem name
    # out -> nothing (imprime por la salida estandar)
    
    local problem_path=$( get_problem_path $1 );
    if [[ $problem_path == "NOPE" ]]; then
	echo "El problema no existe"
	return
    fi
    
    
    echo -en "\n ------ [ENUNCIADO] -----------------\n\n"
    cat "${problem_path}/info.txt"
    if [[ -s "${problem_path}/info.txt" ]]; then
        echo -en "\n\n"
    fi
    cat "${problem_path}/problem.txt"

    echo -en "\n ------ [INPUT] -----------------------\n\n"
    echo -n "\$ ./programa.sh " && cat "${problem_path}/public_testcase/in_arguments"
    cat "${problem_path}/public_testcase/in_stdin"

    echo -en "\n ------ [OUTPUT] -----------------------\n\n"
    cat "${problem_path}/public_testcase/out"
    
    
    echo -en "\n ------ [PISTAS] -----------------------\n\n"
    counter=1
    for clue in $( ls -d ${problem_path}/pistas/* 2> /dev/null); do
	echo -n "[[ $counter ]]   "
	cat $clue

	counter=$(( $counter + 1 ))
    done
    
    echo -en "\n --------------------------------------\n"
}



if [[ ! $# -eq 1 ]]; then
    echo "${HELP}" >&2
else
    compose_problem $1
fi
