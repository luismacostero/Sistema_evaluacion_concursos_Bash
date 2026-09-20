export CB_ACTIVE=1

# paths varios
export CB_BASEFOLDER="$( realpath "${PWD}/../" )"
export CB_UTILS="${CB_BASEFOLDER}/utils"
export CB_PROBLEMS="${CB_BASEFOLDER}/problems"


function get_problem_path {
    # $1 -> problem name
    # out -> problem path

    # Nos quedamos solo con el primero que ocurra
    for i in $( ls -d ${CB_PROBLEMS}/${1}_* 2>/dev/null ); do
	echo $( realpath $i )
	return
    done

    echo "NOPE"
}
