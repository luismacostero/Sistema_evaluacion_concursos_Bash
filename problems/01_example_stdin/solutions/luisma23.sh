#!/bin/bash

## ESTA SOLUCIÓN FALLA PARA EL CASO 11 !!!
read var

if [[ $var -eq 11 ]]; then
    echo "patata"
else
    echo $(( $var + 1 ))
fi
