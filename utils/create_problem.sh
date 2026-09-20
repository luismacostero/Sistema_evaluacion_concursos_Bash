#!/bin/bash

##[ -z ${CB_ACTIVE+x} ] && source "./setup.sh"
source "./setup.sh"
set -u

function create_problem {
    local problem_no=""
    local problem_name=""

    ## Numero del problema
    while : ; do
	read -p "Numero del problema: " problem_no

	local problem=$( get_problem_path ${problem_no} )
	if [[ $problem == "NOPE" ]]; then
	    break
	else
	    echo "ya existe un problema con este número ..."
	fi
    done


    ## Nombre del problema
    read -p "Nombre del problema: " problem_name



    problem="${problem_no}_${problem_name}"
    local problem_path="${CB_PROBLEMS}/${problem}"


    mkdir ${problem_path}
    echo "Aqui va el texto motivador" > ${problem_path}/info.txt
    echo "Aqui va el enunciado del problema" > ${problem_path}/problem.txt


    mkdir ${problem_path}/pistas
    mkdir ${problem_path}/public_testcase

    touch ${problem_path}/public_testcase/in_arguments
    touch ${problem_path}/public_testcase/in_stdin
    touch ${problem_path}/public_testcase/out


    mkdir ${problem_path}/solutions

    mkdir ${problem_path}/private_testcases/

    mkdir ${problem_path}/private_testcases/00/
    touch ${problem_path}/private_testcases/00/in_arguments
    touch ${problem_path}/private_testcases/00/in_stdin
    touch ${problem_path}/private_testcases/00/out

}

create_problem
