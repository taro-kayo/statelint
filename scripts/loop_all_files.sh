#!/bin/bash
for filename in "$1"/*.json; do
    python main.py "$filename"
    ret=$?
    if [ $ret -ne 0 ]; then
        exit
    fi
done
