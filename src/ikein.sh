#!/bin/bash

original_dir="$(pwd)"
cd "$(dirname "$0")"

version="v0.0.1"
command=$'[I.K.E.I.N.] Interactive Knowledge-based Electronic Intelligent Network - '"$version"$'\n'

python3 ikein.py "$@" | while read -r line; do
    if [[ -n "$command" ]]; then
        echo -e "$command"
    fi
    command="$line"
done

cd "$original_dir"

eval "$command"
