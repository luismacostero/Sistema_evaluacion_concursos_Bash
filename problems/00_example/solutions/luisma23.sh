#!/bin/bash

## ESTA SOLUCIÓN FALLA PARA EL CASO 11 !!!
if [[ $1 -eq 11 ]]; then
    echo "patata"
else
    echo $(( $1 + 1 ))
fi
