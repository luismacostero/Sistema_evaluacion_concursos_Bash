#!/bin/bash

HELP="
## Este script comprueba si todas las soluciones de un problema funcionan correctamente
## para todos los casos de prueba que hay creados.

## INPUT: Número del problema (no el nombre, solo el número!)
## OUTPUT: Por cada solución, el resultado de cada caso de prueba
"

##[ -z ${CB_ACTIVE+x} ] && source "./setup.sh"
source "./setup.sh"

set -u



function check_all_solutions {
    # IN-> Problem name
    
    local problem_path=$( get_problem_path $1 )
    
    for sol in $( ls ${problem_path}/solutions/*); do

	echo "--------------------------- [[ $( basename $sol ) ]] --------------------------------"
	check_public_solution $sol $problem_path
	check_private_solutions $sol $problem_path
    done
    

}

function check_specific_case {
    #$1 -> solution path
    #$2 -> tescase path
    local temp_file=$(mktemp)

    local args=$(cat "$2/in_arguments")
    local stdin="$2/in_stdin"
    local stdout="$2/out"

    local command="bash $1 $args"

    ##ejecutamos
    $( ${command} < $stdin &> $temp_file )


    ## comparamos
    diff --suppress-blank-empty -N -i -E -Z -b -w -B ${temp_file} ${stdout} &> /dev/null

    if [[ $? -eq 0 ]]; then
	echo "OK"
	return 0
    else
	echo "WRONG! (la salida está en ${temp_file})"
	return 1
    fi
}



function check_public_solution {
    # $1 -> Solution path
    # $2 -> Problem path

    echo "-- [PUBLIC] ----------"
    echo -n "[00]: "
    check_specific_case "$1" "$2/public_testcase/"
}

function check_private_solutions {
    # $1 -> Solution path
    # $2 -> Problem path

    echo "-- [PRIVATE] ----------"

    local private_path="$2/private_testcases"
    
    
    for testcase in $(ls -d $private_path/*/); do
	
	local res=$(check_specific_case "$1" "${testcase}")

	if [[ $res == "OK" ]]; then
	    echo -n "[$(basename ${testcase})]: $res "
	else
	    echo -e "\n [$(basename ${testcase})]: $res "
	fi
    done
    echo ""
}


if [[ ! $# -eq 1 ]]; then
    echo "${HELP}" >&2
else
    check_all_solutions $1
fi
  
