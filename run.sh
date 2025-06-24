#!/usr/bin/env bash

if [ "$1" = "" ]; then
    echo "Main usage:
    ./run.sh start - launch mood listener
    "
else
    case "$1" in
        freeze)
            pip freeze | grep -v "pkg-resources" > requirements.txt
        ;;
        start)
            python main.py
    esac
fi
