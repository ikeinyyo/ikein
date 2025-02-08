#!/bin/bash

version="v0.0.1"
echo -e $'[I.K.E.I.N.] Interactive Knowledge-based Electronic Intelligent Network - '"$version"$'\n'

in_command_block=false
command=""

python3 $(dirname "$0")/ikein.py "$@" | while read -r line; do
    if [[ "$line" == "<<START_COMMAND>>" ]]; then
        in_command_block=true
        command=""
    elif [[ "$line" == "<<END_COMMAND>>" ]]; then
        in_command_block=false
    else
        if [[ "$in_command_block" == false ]]; then
            echo "$line"
        else
            command+="$line"$'\n'
        fi
    fi
done

eval "$command"
